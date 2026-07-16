from dataclasses import dataclass


@dataclass
class MoveToBoardCommand:
    """Reassigns an existing piece's placement to a different board."""

    services: object
    piece_id: str
    old_board_id: str
    new_board_id: str

    name = "Move piece to board"

    def redo(self):
        self._apply(self.new_board_id)

    def undo(self):
        self._apply(self.old_board_id)

    def _apply(self, board_id: str):
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is None:
            return

        placement.board_id = board_id
