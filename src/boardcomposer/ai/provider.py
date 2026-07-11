from abc import ABC, abstractmethod


class AIProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass
