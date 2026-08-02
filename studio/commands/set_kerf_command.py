from dataclasses import dataclass


@dataclass
class SetKerfCommand:
    """Changes the project's saw kerf (cut width), used to space pieces
    apart when snapping them next to each other in the workspace."""

    services: object
    old_kerf_mm: float
    new_kerf_mm: float

    @property
    def name(self) -> str:
        return f"Ancho de sierra cambiado a {self.new_kerf_mm:g} mm"

    @property
    def category(self) -> str:
        return "proyecto"

    def redo(self):
        self._apply(self.new_kerf_mm)

    def undo(self):
        self._apply(self.old_kerf_mm)

    def _apply(self, kerf_mm: float):
        project = self.services.projects.current_project
        if project is None:
            return

        project.kerf_mm = kerf_mm
