from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Project,
    SolutionExplanation,
    SolutionScore,
)

from .base_solver import BaseSolver


class SequentialSolver(BaseSolver):
    def __init__(self, project: Project) -> None:
        self.project = project

    def solve(self) -> list[AssemblySolution]:
        x = 0.0
        y = 0.0
        row_height = 0.0
        placements: list[BoardPlacement] = []

        for index, board in enumerate(self.project.boards):
            board_id = board.id or f"board-{index + 1}"

            length = board.length_mm
            width = board.width_mm
            rotated = False

            if (
                self.project.constraints.allow_rotation
                and self.project.constraints.max_length_mm is not None
                and x + length > self.project.constraints.max_length_mm
                and x + board.width_mm <= self.project.constraints.max_length_mm
            ):
                length = board.width_mm
                width = board.length_mm
                rotated = True

            if (
                self.project.constraints.max_length_mm is not None
                and x + length > self.project.constraints.max_length_mm
                and placements
            ):
                x = 0.0
                y += row_height
                row_height = 0.0

            if (
                self.project.constraints.max_length_mm is not None
                and x + length > self.project.constraints.max_length_mm
            ):
                continue

            if (
                self.project.constraints.max_width_mm is not None
                and y + width > self.project.constraints.max_width_mm
            ):
                continue

            placements.append(
                BoardPlacement(
                    board_id=board_id,
                    x_mm=x,
                    y_mm=y,
                    length_mm=length,
                    width_mm=width,
                    rotated=rotated,
                )
            )

            x += length
            row_height = max(row_height, width)

        temp_solution = AssemblySolution(placements=placements)

        usage_score = (
            len(placements) / len(self.project.boards) * 50
            if self.project.boards
            else 0
        )
        waste_score = max(0.0, (1.0 - temp_solution.waste_ratio) * 50)

        solution = AssemblySolution(
            placements=placements,
            score=SolutionScore(
                material_usage_score=usage_score,
                waste_score=waste_score,
            ),
            explanation=SolutionExplanation(notes=["SequentialSolver"]),
        )

        return [solution]
