from dataclasses import dataclass, field

from boardcomposer.ai.provider import AIProvider


@dataclass
class MockAIProvider(AIProvider):
    """AIProvider sin llamadas externas, para desarrollo y tests sin proveedor real."""

    response: str = "Respuesta simulada del asistente IA."
    calls: list[str] = field(default_factory=list)

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self.response
