from __future__ import annotations

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.strategies import material_first_strategy

from studio.models import StudioPlacement

MAX_COMPARISON_SOLUTIONS = 4


class LayoutService:
    """Bridge between BoardComposer Studio and the core layout engine."""

    def __init__(self, services):
        self.services = services
        self.last_solution = None
        self.last_solutions: list[AssemblySolution] = []

    def to_core_project(self) -> Project | None:
        studio_project = self.services.projects.current_project
        if studio_project is None:
            return None

        core_project = Project(
            constraints=ProjectConstraints(
                allow_rotation=True,
                allow_cutting=False,
            )
        )

        source_board = studio_project.boards[0] if studio_project.boards else None

        if source_board is not None:
            core_project.constraints = ProjectConstraints(
                max_length_mm=source_board.length_mm,
                max_width_mm=source_board.width_mm,
                allow_rotation=True,
                allow_cutting=False,
            )

        for piece in studio_project.pieces:
            core_project.add_board(
                Board(
                    id=piece.piece_id,
                    length_mm=piece.length_mm,
                    width_mm=piece.width_mm,
                    thickness_mm=19,
                )
            )

        return core_project

    def solve_current_project(self):
        project = self.to_core_project()
        if project is None:
            return None

        solutions = GeometrySolver(project).solve()
        if not solutions:
            return None

        self.last_solution = solutions[0]
        return self.last_solution

    def compare_solutions(self) -> list[AssemblySolution]:
        """Run a richer strategy and keep up to MAX_COMPARISON_SOLUTIONS ranked
        candidates for side-by-side comparison (IDE-0002)."""
        project = self.to_core_project()
        if project is None:
            self.last_solutions = []
            return self.last_solutions

        solutions = GeometrySolver(project, strategy=material_first_strategy()).solve()
        self.last_solutions = solutions[:MAX_COMPARISON_SOLUTIONS]

        if self.last_solutions:
            self.last_solution = self.last_solutions[0]

        return self.last_solutions

    def apply_last_solution_to_current_project(self) -> bool:
        return self._apply_solution(self.last_solution)

    def apply_comparison_solution(self, index: int) -> bool:
        if index < 0 or index >= len(self.last_solutions):
            return False

        return self._apply_solution(self.last_solutions[index])

    def _apply_solution(self, solution: AssemblySolution | None) -> bool:
        studio_project = self.services.projects.current_project
        if studio_project is None or solution is None:
            return False

        studio_project.placements.clear()

        for placement in solution.placements:
            studio_project.placements.append(
                StudioPlacement(
                    piece_id=placement.board_id,
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    rotated=placement.rotated,
                    rotation=90 if placement.rotated else 0,
                )
            )

        self.services.projects.mark_modified()
        return True
