import json

from boardcomposer.domain import AssemblySolution, Project

from .base import Presenter
from boardcomposer.solver.strategies import OptimizationStrategy


class JsonPresenter(Presenter):
    def render(
        self,
        project: Project,
        strategy: OptimizationStrategy,
        solutions: list[AssemblySolution],
        top: int,
    ) -> str:
        return json.dumps(
            {
                "input_boards": len(project.boards),
                "strategy": strategy.name,
                "generators": list(strategy.generator_names),
                "top": top,
                "weights": {
                    "material_utilization": strategy.weights.material_utilization,
                    "placed_boards": strategy.weights.placed_boards,
                    "compactness": strategy.weights.compactness,
                    "rotation_penalty": strategy.weights.rotation_penalty,
                },
                "best_solution": {
                    "score": solutions[0].score.total,
                    "layout": solutions[0].explanation.notes,
                    "placed_boards": len(solutions[0].placements),
                    "total_length_mm": solutions[0].total_length_mm,
                    "total_width_mm": solutions[0].total_width_mm,
                },
                "solutions": [
                    {
                        "placed_boards": len(solution.placements),
                        "total_length_mm": solution.total_length_mm,
                        "total_width_mm": solution.total_width_mm,
                        "score": solution.score.total,
                        "layout": solution.explanation.notes,
                        "placements": [
                            {
                                "board_id": placement.board_id,
                                "x_mm": placement.x_mm,
                                "y_mm": placement.y_mm,
                                "length_mm": placement.length_mm,
                                "width_mm": placement.width_mm,
                                "rotated": placement.rotated,
                            }
                            for placement in solution.placements
                        ],
                    }
                    for solution in solutions[:top]
                ],
            },
            indent=2,
        )


def solutions_to_json(
    project: Project,
    strategy: OptimizationStrategy,
    solutions: list[AssemblySolution],
    top: int,
) -> str:
    return JsonPresenter().render(project, strategy, solutions, top)
