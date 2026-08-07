import os

from openai import OpenAI

from boardcomposer.ai.provider import AIProvider

DEFAULT_HOST = "http://localhost:11434"


class OllamaProvider(AIProvider):
    """AIProvider real sobre un servidor Ollama local (o remoto en la red).

    Sin clave de API: Ollama no la exige. Reutiliza el SDK de OpenAI
    apuntado a la API de Ollama compatible con el formato de OpenAI
    (`/v1/chat/completions`) en vez de traer un SDK propio — el `api_key`
    es un valor cualquiera no vacío, exigido por el SDK pero ignorado por
    Ollama. A diferencia de Anthropic/OpenAI/Gemini, sin modelo por
    defecto razonable: depende de qué modelos tenga el usuario
    descargados localmente (OLLAMA_MODEL) — sin uno, no hay nada
    coherente que llamar.
    """

    def __init__(self, model: str | None = None, host: str | None = None) -> None:
        self.model = model or os.environ.get("OLLAMA_MODEL")
        if not self.model:
            raise ValueError(
                "OllamaProvider necesita un modelo: variable de entorno "
                "OLLAMA_MODEL (o el argumento model)."
            )
        host = host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST
        self._client = OpenAI(base_url=f"{host.rstrip('/')}/v1", api_key="ollama")

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""
