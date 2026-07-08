from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.strategies import OptimizationStrategy

from .base import Presenter


class TextPresenter(Presenter):
    def render(
        self,
        project: Project,
        strategy: OptimizationStrategy,
        solutions: list[AssemblySolution],
        top: int,
    ) -> str:
        best = solutions[0]

        return "\n".join(
            [
                "BoardComposer",
                f"Tablas entrada: {len(project.boards)}",
                f"Soluciones válidas: {len(solutions)}",
                f"Tablas colocadas: {len(best.placements)}",
                f"Largo total: {best.total_length_mm} mm",
                f"Ancho total: {best.total_width_mm} mm",
                f"Puntuación: {best.score.total}",
                f"Layout: {', '.join(best.explanation.notes)}",
            ]
        )


def solution_to_text(
    project: Project,
    solutions: list[AssemblySolution],
) -> str:
    return TextPresenter().render(
        project=project,
        strategy=None,
        solutions=solutions,
        top=1,
    )
