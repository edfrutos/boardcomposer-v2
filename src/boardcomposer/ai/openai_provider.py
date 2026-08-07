from openai import OpenAI

from boardcomposer.ai.provider import AIProvider

DEFAULT_MODEL = "gpt-4o-mini"


class OpenAIProvider(AIProvider):
    """AIProvider real sobre la API de OpenAI (GPT).

    Requiere la variable de entorno OPENAI_API_KEY: el SDK la lee
    automáticamente al construir el cliente, no se gestiona aquí.
    """

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        self._client = OpenAI()

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""
