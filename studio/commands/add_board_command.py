from studio.commands.command import Command
from studio.models import StudioBoard


class AddBoardCommand(Command):
    def __init__(self, services, board: StudioBoard):
        self.services = services
        self.board = board

    @property
    def name(self) -> str:
        return f"Tablero añadido: {self.board.board_id}"

    @property
    def category(self) -> str:
        return "tablero"

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        project.boards.append(self.board)

    def undo(self):
        project = self.services.projects.current_project
        if project is None:
            return

        project.boards.remove(self.board)

    def redo(self):
        self.execute()
