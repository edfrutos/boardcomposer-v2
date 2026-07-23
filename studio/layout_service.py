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

    def to_core_project(self, active_board_id: str | None = None) -> Project | None:
        studio_project = self.services.projects.current_project
        if studio_project is None:
            return None

        core_project = Project(
            constraints=ProjectConstraints(
                allow_rotation=True,
                allow_cutting=False,
            )
        )

        source_board = self._resolve_board(studio_project, active_board_id)

        if source_board is not None:
            core_project.constraints = ProjectConstraints(
                max_length_mm=source_board.length_mm,
                max_width_mm=source_board.width_mm,
                allow_rotation=True,
                allow_cutting=False,
            )

        target_board_id = source_board.board_id if source_board is not None else None

        for piece in studio_project.pieces:
            placement = studio_project.placement_by_piece_id(piece.piece_id)
            # A piece already placed on a DIFFERENT board is spoken for —
            # packing it again here would leave the project with two
            # placements for the same piece once the solution is applied.
            # Pieces with no placement yet, or already on the board being
            # solved, are fair game for (re)packing.
            if (
                placement is not None
                and target_board_id is not None
                and placement.board_id != target_board_id
            ):
                continue

            core_project.add_board(
                Board(
                    id=piece.piece_id,
                    length_mm=piece.length_mm,
                    width_mm=piece.width_mm,
                    thickness_mm=piece.thickness_mm,
                )
            )

        return core_project

    @staticmethod
    def _resolve_board(studio_project, active_board_id: str | None):
        if not studio_project.boards:
            return None

        if active_board_id is not None:
            for board in studio_project.boards:
                if board.board_id == active_board_id:
                    return board

        return studio_project.boards[0]

    def solve_current_project(self, active_board_id: str | None = None):
        project = self.to_core_project(active_board_id)
        if project is None:
            return None

        solutions = GeometrySolver(project).solve()
        if not solutions:
            return None

        self.last_solution = solutions[0]
        return self.last_solution

    def compare_solutions(
        self, active_board_id: str | None = None
    ) -> list[AssemblySolution]:
        """Run a richer strategy and keep up to MAX_COMPARISON_SOLUTIONS ranked
        candidates for side-by-side comparison (IDE-0002)."""
        project = self.to_core_project(active_board_id)
        if project is None:
            self.last_solutions = []
            return self.last_solutions

        solutions = GeometrySolver(project, strategy=material_first_strategy()).solve()
        self.last_solutions = solutions[:MAX_COMPARISON_SOLUTIONS]

        if self.last_solutions:
            self.last_solution = self.last_solutions[0]

        return self.last_solutions

    def apply_last_solution_to_current_project(
        self, active_board_id: str | None = None
    ) -> bool:
        if not self._apply_solution(self.last_solution, active_board_id):
            return False

        self._fill_other_empty_boards_with_leftovers(active_board_id)
        return True

    def apply_comparison_solution(
        self, index: int, active_board_id: str | None = None
    ) -> bool:
        if index < 0 or index >= len(self.last_solutions):
            return False

        if not self._apply_solution(self.last_solutions[index], active_board_id):
            return False

        self._fill_other_empty_boards_with_leftovers(active_board_id)
        return True

    def _fill_other_empty_boards_with_leftovers(
        self, solved_board_id: str | None
    ) -> None:
        """A project can have several boards, but a layout only ever solves
        for one of them — pieces that don't fit there aren't necessarily
        unplaceable if another board still has room. Tries each of the
        project's other boards, in order, for whatever's left; only boards
        that are still completely empty are candidates, so this never
        reshuffles a board someone (or a previous apply) already arranged.
        """
        studio_project = self.services.projects.current_project
        if studio_project is None:
            return

        solved_board = self._resolve_board(studio_project, solved_board_id)
        solved_board_id = solved_board.board_id if solved_board is not None else None

        def has_unplaced_pieces() -> bool:
            return any(
                studio_project.placement_by_piece_id(piece.piece_id) is None
                for piece in studio_project.pieces
            )

        occupied_board_ids = {p.board_id for p in studio_project.placements}
        original_last_solution = self.last_solution

        try:
            for board in studio_project.boards:
                if board.board_id == solved_board_id:
                    continue
                if board.board_id in occupied_board_ids:
                    continue
                if not has_unplaced_pieces():
                    break

                solution = self.solve_current_project(board.board_id)
                if solution is not None and solution.placements:
                    self._apply_solution(solution, board.board_id)
                    occupied_board_ids.add(board.board_id)
        finally:
            self.last_solution = original_last_solution

    def _apply_solution(
        self, solution: AssemblySolution | None, active_board_id: str | None = None
    ) -> bool:
        studio_project = self.services.projects.current_project
        if studio_project is None or solution is None:
            return False

        target_board = self._resolve_board(studio_project, active_board_id)
        if target_board is None:
            return False

        target_board_id = target_board.board_id

        # Only replace placements on the board being solved. A project can
        # have pieces placed on other boards; clearing the whole list (as
        # this used to) silently emptied every other board whenever a layout
        # was applied to one of them.
        studio_project.placements = [
            placement
            for placement in studio_project.placements
            if placement.board_id != target_board_id
        ]

        for placement in solution.placements:
            studio_project.placements.append(
                StudioPlacement(
                    piece_id=placement.board_id,
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    board_id=target_board_id,
                    rotated=placement.rotated,
                    rotation=90 if placement.rotated else 0,
                )
            )

        self.services.projects.mark_modified()
        return True
