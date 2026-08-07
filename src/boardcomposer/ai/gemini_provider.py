from google import genai

from boardcomposer.ai.provider import AIProvider

DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiProvider(AIProvider):
    """AIProvider real sobre la API de Google Gemini.

    Requiere la variable de entorno GEMINI_API_KEY (o GOOGLE_API_KEY): el
    SDK la lee automáticamente al construir el cliente, no se gestiona
    aquí.
    """

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        self._client = genai.Client()

    def complete(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text or ""
