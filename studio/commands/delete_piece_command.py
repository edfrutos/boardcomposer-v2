from studio.commands.command import Command


class DeletePieceCommand(Command):
    """Removes a piece and its placement, mirroring what AddPieceCommand
    adds together — otherwise the piece would keep showing up in the
    Explorer's piece list after "deleting" it from the board."""

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
