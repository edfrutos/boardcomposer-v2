from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.strategies import (
    OptimizationStrategy,
    balanced_strategy,
)

from .base_solver import BaseSolver


class GeometrySolver(BaseSolver):
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy | None = None,
    ) -> None:
        self.project = project
        self.strategy = strategy or balanced_strategy()

    def solve(self) -> list[AssemblySolution]:
        return CandidatePipeline(
            project=self.project,
            strategy=self.strategy,
        ).run()
