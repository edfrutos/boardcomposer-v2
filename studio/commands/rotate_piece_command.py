from studio.commands.command import Command


class RotatePieceCommand(Command):
    def __init__(self, services, piece_id: str, old_rotation: int, new_rotation: int):
        self.services = services
        self.piece_id = piece_id
        self.old_rotation = old_rotation
        self.new_rotation = new_rotation

    def execute(self):
        self._apply(self.new_rotation)

    def undo(self):
        self._apply(self.old_rotation)

    def redo(self):
        self.execute()

    def _apply(self, rotation: int):
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is not None:
            placement.rotation = rotation
