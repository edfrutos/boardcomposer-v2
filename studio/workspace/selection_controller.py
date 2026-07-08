from __future__ import annotations

from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.selection import apply_selection


class SelectionController:
    def __init__(self, services):
        self.services = services
        self._items: list[BoardPieceItem] = []
        self._selected_ids: set[str] = set()

    def bind_items(self, items: list[BoardPieceItem]) -> None:
        self._items = items

    def select(self, piece_id: str) -> None:
        self.select_many([piece_id])

    def select_many(self, piece_ids: list[str]) -> None:
        self._selected_ids = set(piece_ids)

        for item in self._items:
            apply_selection(item, item.piece_id in self._selected_ids)

        if len(self._selected_ids) == 1:
            self.services.selection.select_one(next(iter(self._selected_ids)))

    def clear(self) -> None:
        self._selected_ids.clear()

        for item in self._items:
            apply_selection(item, False)

    def current(self) -> str | None:
        if len(self._selected_ids) != 1:
            return None
        return next(iter(self._selected_ids))

    def selected(self) -> list[str]:
        return list(self._selected_ids)

    def sync_inspector(self, window) -> None:
        current = self.current()

        if current is None:
            if hasattr(window, "inspector"):
                window.inspector.setText("Inspector\n\nSin selección")
            return

        if hasattr(window, "refresh_inspector_for_piece"):
            window.refresh_inspector_for_piece(current)
