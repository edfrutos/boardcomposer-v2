from dataclasses import dataclass


@dataclass
class MoveToBoardCommand:
    """Reassigns an existing piece's placement to a different board.

    old_x/old_y/new_x/new_y are optional: a piece that doesn't fit the
    destination board at its old position gets relocated to free space
    there (main_window._move_piece_to_board) — passing the reposition
    alongside the board change keeps it a single undoable step instead of
    two, so one Ctrl+Z fully reverts both.
    """

    services: object
    piece_id: str
    old_board_id: str
    new_board_id: str
    old_x: float | None = None
    old_y: float | None = None
    new_x: float | None = None
    new_y: float | None = None

    @property
    def name(self) -> str:
        return f"Pieza movida de tablero: {self.piece_id} → {self.new_board_id}"

    def redo(self):
        self._apply(self.new_board_id, self.new_x, self.new_y)

    def undo(self):
        self._apply(self.old_board_id, self.old_x, self.old_y)

    def _apply(self, board_id: str, x_mm: float | None, y_mm: float | None):
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is None:
            return

        placement.board_id = board_id
        if x_mm is not None:
            placement.x_mm = x_mm
        if y_mm is not None:
            placement.y_mm = y_mm
