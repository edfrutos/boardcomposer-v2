from studio.commands.command import Command
from studio.models import StudioPiece, StudioPlacement


class AddPieceCommand(Command):
    """Adds a piece to the project along with an initial placement, so it's
    immediately visible on the active board and draggable — an unplaced
    piece would only show up in the Explorer, not on the canvas."""

    def __init__(self, services, piece: StudioPiece, placement: StudioPlacement):
        self.services = services
        self.piece = piece
        self.placement = placement

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        project.pieces.append(self.piece)
        project.placements.append(self.placement)

    def undo(self):
        project = self.services.projects.current_project
        if project is None:
            return

        project.pieces.remove(self.piece)
        project.placements.remove(self.placement)

    def redo(self):
        self.execute()
