import os

from boardcomposer.ai.anthropic_provider import AnthropicProvider
from boardcomposer.ai.gemini_provider import GeminiProvider
from boardcomposer.ai.mock_provider import MockAIProvider
from boardcomposer.ai.ollama_provider import OllamaProvider
from boardcomposer.ai.openai_provider import OpenAIProvider
from boardcomposer.ai.provider import AIProvider

PROVIDER_NAMES = ("mock", "anthropic", "openai", "gemini", "ollama")

_PROVIDERS = {
    "mock": MockAIProvider,
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "ollama": OllamaProvider,
}


def provider_by_name(name: str) -> AIProvider:
    try:
        return _PROVIDERS[name]()
    except KeyError as exc:
        valid = ", ".join(sorted(_PROVIDERS))
        raise ValueError(
            f"Proveedor de IA desconocido: {name}. Válidos: {valid}"
        ) from exc


def default_provider() -> AIProvider:
    """Proveedor de IA por defecto.

    BOARDCOMPOSER_AI_PROVIDER, si está definida, elige explícitamente el
    proveedor activo (IDE-0036: selección explícita en Preferencias de
    Studio, que la persiste vía QSettings y la vuelca aquí igual que ya
    hacía con ANTHROPIC_API_KEY — el Core sigue leyendo solo el entorno,
    ADR-001). Sin ella, se mantiene el comportamiento previo a IDE-0036:
    "anthropic" si hay ANTHROPIC_API_KEY en el entorno, si no "mock".
    """
    provider_name = os.environ.get("BOARDCOMPOSER_AI_PROVIDER")
    if provider_name:
        return provider_by_name(provider_name)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return provider_by_name("anthropic")
    return provider_by_name("mock")
