"""Activity log for the Timeline dock's Actividad tab.

Wires up ADR-003's EventBus for real: until now it was built and
instantiated in StudioServices but nothing ever called publish() or
subscribe() on it (docs/studio.md). MainWindow publishes ACTIVITY_EVENT
with a ready-made Spanish message and a category at every meaningful
action — command execution, undo/redo, solving/applying a layout,
project open/save/new, CSV import — and this is the one subscriber,
keeping the last MAX_ENTRIES as ActivityEntry records for
timeline_panel.render_activity() to display (and filter by category,
IDE-0026).
"""

from collections import deque
from dataclasses import dataclass
from datetime import datetime

from studio.events import EventBus

ACTIVITY_EVENT = "studio.activity"
MAX_ENTRIES = 200

# Grounded in what actually happens in MainWindow (~17 call sites), not
# ADR-003's aspirational 9-name event catalog — that doesn't match the
# real granularity of the code. "deshacer" is its own bucket rather than
# inheriting the underlying command's category, so "show me everything
# that got undone" is a real filter regardless of what was undone.
CATEGORIES = ("proyecto", "tablero", "pieza", "deshacer", "layout", "import")


@dataclass(frozen=True)
class ActivityEntry:
    timestamp: str
    category: str
    message: str


class ActivityLog:
    def __init__(self, events: EventBus):
        self._entries: deque[ActivityEntry] = deque(maxlen=MAX_ENTRIES)
        events.subscribe(ACTIVITY_EVENT, self._on_activity)

    def _on_activity(self, _event_name: str, payload: dict) -> None:
        message = payload.get("message", "")
        category = payload.get("category", "")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._entries.appendleft(ActivityEntry(timestamp, category, message))

    @property
    def entries(self) -> list[ActivityEntry]:
        return list(self._entries)
