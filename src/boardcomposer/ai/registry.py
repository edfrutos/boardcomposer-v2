from boardcomposer.ai.mock_provider import MockAIProvider
from boardcomposer.ai.provider import AIProvider

PROVIDER_NAMES = ("mock",)


def provider_by_name(name: str) -> AIProvider:
    providers = {
        "mock": MockAIProvider,
    }

    try:
        return providers[name]()
    except KeyError as exc:
        valid = ", ".join(sorted(providers))
        raise ValueError(
            f"Proveedor de IA desconocido: {name}. Válidos: {valid}"
        ) from exc
