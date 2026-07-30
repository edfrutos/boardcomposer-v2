from studio.commands.command import Command
from studio.models import StudioPiece


class EditPieceCommand(Command):
    def __init__(self, services, old_piece: StudioPiece, new_piece: StudioPiece):
        self.services = services
        self.old_piece = old_piece
        self.new_piece = new_piece

    @property
    def name(self) -> str:
        return f"Pieza editada: {self.new_piece.piece_id}"

    def execute(self):
        self._replace(self.old_piece, self.new_piece)

    def undo(self):
        self._replace(self.new_piece, self.old_piece)

    def redo(self):
        self.execute()

    def _replace(self, current: StudioPiece, replacement: StudioPiece):
        project = self.services.projects.current_project
        if project is None:
            return

        index = project.pieces.index(current)
        project.pieces[index] = replacement
