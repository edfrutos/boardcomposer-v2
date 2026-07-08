from abc import ABC, abstractmethod

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.strategies import OptimizationStrategy


class Presenter(ABC):
    @abstractmethod
    def render(
        self,
        project: Project,
        strategy: OptimizationStrategy | None,
        solutions: list[AssemblySolution],
        top: int,
    ) -> str:
        pass
