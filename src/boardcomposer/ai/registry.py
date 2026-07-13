import os

from boardcomposer.ai.anthropic_provider import AnthropicProvider
from boardcomposer.ai.mock_provider import MockAIProvider
from boardcomposer.ai.provider import AIProvider

PROVIDER_NAMES = ("mock", "anthropic")


def provider_by_name(name: str) -> AIProvider:
    providers = {
        "mock": MockAIProvider,
        "anthropic": AnthropicProvider,
    }

    try:
        return providers[name]()
    except KeyError as exc:
        valid = ", ".join(sorted(providers))
        raise ValueError(
            f"Proveedor de IA desconocido: {name}. Válidos: {valid}"
        ) from exc


def default_provider() -> AIProvider:
    """Proveedor de IA por defecto: "anthropic" si hay una ANTHROPIC_API_KEY
    configurada en el entorno, "mock" en caso contrario."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return provider_by_name("anthropic")
    return provider_by_name("mock")
