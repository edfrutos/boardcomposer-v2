from dataclasses import dataclass


@dataclass
class MovePieceCommand:
    services: object
    piece_id: str

    old_x: float
    old_y: float

    new_x: float
    new_y: float

    name = "Move piece"

    def redo(self):
        self._apply(self.new_x, self.new_y)

    def undo(self):
        self._apply(self.old_x, self.old_y)

    def _apply(self, x: float, y: float):
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is None:
            return

        placement.x_mm = x
        placement.y_mm = y
