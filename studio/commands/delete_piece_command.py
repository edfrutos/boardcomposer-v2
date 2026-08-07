from studio.commands.command import Command


class DeletePieceCommand(Command):
    """Removes a piece and its placement together, mirroring what
    AddPieceCommand adds together — full removal from the project, not
    just off whichever board it's on (see UnplacePieceCommand for that;
    "Eliminar pieza" on the workspace canvas, Backspace, uses that one
    instead). Wired to Explorer's "Eliminar del proyecto…" (right-click on
    a piece), a deliberately separate, more explicit action from taking a
    piece off a board.
    """

    def __init__(self, services, piece_id: str):
        self.services = services
        self.piece_id = piece_id
        self._piece = None
        self._placement = None

    @property
    def name(self) -> str:
        return f"Pieza eliminada: {self.piece_id}"

    @property
    def category(self) -> str:
        return "pieza"

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        self._piece = next(
            (piece for piece in project.pieces if piece.piece_id == self.piece_id),
            None,
        )
        if self._piece is None:
            return

        self._placement = project.placement_by_piece_id(self.piece_id)

        project.pieces.remove(self._piece)
        if self._placement is not None:
            project.placements.remove(self._placement)

    def undo(self):
        project = self.services.projects.current_project
        if project is None or self._piece is None:
            return

        project.pieces.append(self._piece)
        if self._placement is not None:
            project.placements.append(self._placement)

    def redo(self):
        self.execute()
