from studio.commands.command import Command


class UnplacePieceCommand(Command):
    """Removes a piece's placement but keeps the piece itself in the
    project. "Eliminar pieza" (Backspace, on a piece selected on the
    workspace canvas) used to delete both together, which meant the piece
    also vanished from the Explorer's Piezas list — reported by the user:
    taking a piece off a board shouldn't erase it from the catalog, only
    the layout solver's own "sin colocar" pieces (main_window.py,
    _unplaced_piece_ids()) should ever be pieces without a placement, and
    now this is too. See DeletePieceCommand for actually removing a piece
    from the project (Explorer's "Eliminar del proyecto…").
    """

    def __init__(self, services, piece_id: str):
        self.services = services
        self.piece_id = piece_id
        self._placement = None

    @property
    def name(self) -> str:
        return f"Pieza quitada del tablero: {self.piece_id}"

    @property
    def category(self) -> str:
        return "pieza"

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        self._placement = project.placement_by_piece_id(self.piece_id)
        if self._placement is not None:
            project.placements.remove(self._placement)

    def undo(self):
        project = self.services.projects.current_project
        if project is None or self._placement is None:
            return

        project.placements.append(self._placement)

    def redo(self):
        self.execute()
