from studio.commands.command import Command
from studio.models import StudioBoard


class AddBoardCommand(Command):
    def __init__(self, services, board: StudioBoard):
        self.services = services
        self.board = board

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
