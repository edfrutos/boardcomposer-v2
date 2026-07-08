"""Selection manager for BoardComposer Studio."""

from dataclasses import dataclass, field


@dataclass
class SelectionManager:
    """Tracks selected Studio object identifiers."""

    _selected_ids: set[str] = field(default_factory=set)

    @property
    def selected_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._selected_ids))

    @property
    def has_selection(self) -> bool:
        return bool(self._selected_ids)

    def select_one(self, object_id: str) -> None:
        self._selected_ids = {object_id}

    def add(self, object_id: str) -> None:
        self._selected_ids.add(object_id)

    def remove(self, object_id: str) -> None:
        self._selected_ids.discard(object_id)

    def toggle(self, object_id: str) -> None:
        if object_id in self._selected_ids:
            self._selected_ids.remove(object_id)
            return

        self._selected_ids.add(object_id)

    def clear(self) -> None:
        self._selected_ids.clear()
