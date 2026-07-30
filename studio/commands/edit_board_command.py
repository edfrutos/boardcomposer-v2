from studio.commands.command import Command
from studio.models import StudioBoard


class EditBoardCommand(Command):
    def __init__(self, services, old_board: StudioBoard, new_board: StudioBoard):
        self.services = services
        self.old_board = old_board
        self.new_board = new_board

    @property
    def name(self) -> str:
        return f"Tablero editado: {self.new_board.board_id}"

    def execute(self):
        self._replace(self.old_board, self.new_board)

    def undo(self):
        self._replace(self.new_board, self.old_board)

    def redo(self):
        self.execute()

    def _replace(self, current: StudioBoard, replacement: StudioBoard):
        project = self.services.projects.current_project
        if project is None:
            return

        index = project.boards.index(current)
        project.boards[index] = replacement
