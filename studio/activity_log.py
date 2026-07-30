"""Activity log for the Timeline dock's Actividad tab.

Wires up ADR-003's EventBus for real: until now it was built and
instantiated in StudioServices but nothing ever called publish() or
subscribe() on it (docs/studio.md). MainWindow publishes ACTIVITY_EVENT
with a ready-made Spanish message at every meaningful action — command
execution, undo/redo, solving/applying a layout, project open/save/new,
CSV import — and this is the one subscriber, keeping the last MAX_ENTRIES
as timestamped strings for timeline_panel.render_activity() to display.
"""

from collections import deque
from datetime import datetime

from studio.events import EventBus

ACTIVITY_EVENT = "studio.activity"
MAX_ENTRIES = 200


class ActivityLog:
    def __init__(self, events: EventBus):
        self._entries: deque[str] = deque(maxlen=MAX_ENTRIES)
        events.subscribe(ACTIVITY_EVENT, self._on_activity)

    def _on_activity(self, _event_name: str, payload: dict) -> None:
        message = payload.get("message", "")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._entries.appendleft(f"{timestamp} — {message}")

    @property
    def entries(self) -> list[str]:
        return list(self._entries)
