from studio.commands.command import Command


class DeletePieceCommand(Command):
    def __init__(self, services, piece_id: str):
        self.services = services
        self.piece_id = piece_id
        self._placement = None

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        self._placement = project.placement_by_piece_id(self.piece_id)
        if self._placement is None:
            return

        project.placements.remove(self._placement)

    def undo(self):
        project = self.services.projects.current_project
        if project is None or self._placement is None:
            return

        project.placements.append(self._placement)

    def redo(self):
        self.execute()
