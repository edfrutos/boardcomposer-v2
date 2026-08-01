"""DXF export for the current Studio workspace state (IDE-0022)."""

from pathlib import Path

from boardcomposer.export import solution_to_dxf

from studio.export.solution_bridge import studio_project_to_solution
from studio.models import StudioProject


def export_project_to_dxf(project: StudioProject, path: str | Path) -> bool:
    solution = studio_project_to_solution(project)
    if not solution.placements:
        return False

    Path(path).write_text(solution_to_dxf(solution), encoding="utf-8")
    return True
