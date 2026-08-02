from studio.commands.command import Command


class RotatePieceCommand(Command):
    """old_x/old_y/new_x/new_y are optional: a piece whose in-place rotation
    would collide with a neighbor gets relocated to free space on the same
    board instead (main_window._rotate_selected_piece) — passing the
    reposition alongside the rotation keeps it a single undoable step."""

    def __init__(
        self,
        services,
        piece_id: str,
        old_rotation: int,
        new_rotation: int,
        old_x: float | None = None,
        old_y: float | None = None,
        new_x: float | None = None,
        new_y: float | None = None,
    ):
        self.services = services
        self.piece_id = piece_id
        self.old_rotation = old_rotation
        self.new_rotation = new_rotation
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y

    @property
    def name(self) -> str:
        return f"Pieza rotada: {self.piece_id}"

    @property
    def category(self) -> str:
        return "pieza"

    def execute(self):
        self._apply(self.new_rotation, self.new_x, self.new_y)

    def undo(self):
        self._apply(self.old_rotation, self.old_x, self.old_y)

    def redo(self):
        self.execute()

    def _apply(self, rotation: int, x_mm: float | None, y_mm: float | None):
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is not None:
            placement.rotation = rotation
            # solution_bridge.py (SVG/PDF export) swaps a piece's length/width
            # off `rotated`, not `rotation` — without this, a manual rotate
            # looks right on the canvas but exports in the original,
            # unrotated orientation.
            placement.rotated = rotation == 90
            if x_mm is not None:
                placement.x_mm = x_mm
            if y_mm is not None:
                placement.y_mm = y_mm
