from abc import ABC, abstractmethod

from boardcomposer.domain import AssemblySolution


class BaseSolver(ABC):
    @abstractmethod
    def solve(self) -> list[AssemblySolution]:
        pass
