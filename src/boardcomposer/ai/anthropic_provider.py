from anthropic import Anthropic

from boardcomposer.ai.provider import AIProvider

DEFAULT_MODEL = "claude-haiku-4-5"
MAX_TOKENS = 4096


class AnthropicProvider(AIProvider):
    """AIProvider real sobre la API de Anthropic (Claude).

    Requiere la variable de entorno ANTHROPIC_API_KEY: el SDK la lee
    automáticamente al construir el cliente, no se gestiona aquí.
    """

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        self._client = Anthropic()

    def complete(self, prompt: str) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
