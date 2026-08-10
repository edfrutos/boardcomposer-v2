from studio.commands.command import Command
from studio.models import StudioBoard, StudioPlacement


class DeleteBoardCommand(Command):
    """Removes a board and its placements — mirrors DeletePieceCommand, but
    for a board: the pieces that were on it stay in the project as "sin
    colocar" (unplace, not delete), same reasoning as UnplacePieceCommand
    keeping the piece itself. Wired to the workspace canvas's right-click
    context menu (IDE-0040), which is also the first place "eliminar
    tablero" exists at all.
    """

    def __init__(self, services, board: StudioBoard):
        self.services = services
        self.board = board
        self._placements: list[StudioPlacement] = []

    @property
    def name(self) -> str:
        return f"Tablero eliminado: {self.board.board_id}"

    @property
    def category(self) -> str:
        return "tablero"

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        self._placements = [
            placement
            for placement in project.placements
            if placement.board_id == self.board.board_id
        ]
        project.boards.remove(self.board)
        project.placements = [
            placement
            for placement in project.placements
            if placement.board_id != self.board.board_id
        ]

    def undo(self):
        project = self.services.projects.current_project
        if project is None:
            return

        project.boards.append(self.board)
        project.placements.extend(self._placements)

    def redo(self):
        self.execute()
