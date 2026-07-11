import json

from boardcomposer.ai.provider import AIProvider
from boardcomposer.domain import Project
from boardcomposer.solver.generators import GENERATOR_REGISTRY
from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.strategies import OptimizationStrategy

PROMPT_TEMPLATE = (
    "Eres un asistente que ajusta los parámetros del solver de "
    "BoardComposer para un proyecto de corte de tableros. Los pesos de "
    "puntuación disponibles son material_utilization, placed_boards, "
    "compactness y rotation_penalty (números no negativos). Los "
    "generadores de disposición disponibles son: {generators}.\n\n"
    "Responde EXCLUSIVAMENTE con un objeto JSON, sin texto adicional, con "
    "esta forma:\n"
    '{{"weights": {{"material_utilization": numero, "placed_boards": '
    'numero, "compactness": numero, "rotation_penalty": numero}}, '
    '"generator_names": ["..."]}}\n\n'
    "Proyecto: {board_count} tablas a colocar.\n"
    "Objetivo del usuario: {goal}\n"
)


class SuggestStrategyError(ValueError):
    """El proveedor de IA no devolvió una estrategia interpretable."""


def suggest_strategy(
    project: Project, provider: AIProvider, goal: str = ""
) -> OptimizationStrategy:
    prompt = PROMPT_TEMPLATE.format(
        generators=", ".join(sorted(GENERATOR_REGISTRY)),
        board_count=len(project.boards),
        goal=goal or "sin especificar; usa un equilibrio razonable.",
    )
    raw = provider.complete(prompt)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SuggestStrategyError(
            f"La respuesta del asistente no es JSON válido: {error}"
        ) from error

    if not isinstance(payload, dict):
        raise SuggestStrategyError(
            "La respuesta del asistente debe ser un objeto JSON."
        )

    weights_data = payload.get("weights")
    if not isinstance(weights_data, dict):
        raise SuggestStrategyError("La respuesta del asistente no incluye 'weights'.")

    try:
        weights = ScoringWeights(
            material_utilization=float(weights_data["material_utilization"]),
            placed_boards=float(weights_data["placed_boards"]),
            compactness=float(weights_data["compactness"]),
            rotation_penalty=float(weights_data["rotation_penalty"]),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise SuggestStrategyError(
            f"Pesos inválidos en la respuesta del asistente: {error}"
        ) from error

    for name, value in weights.__dict__.items():
        if value < 0:
            raise SuggestStrategyError(f"'{name}' no puede ser negativo.")

    generator_names = payload.get("generator_names")
    if not isinstance(generator_names, list) or not generator_names:
        raise SuggestStrategyError(
            "La respuesta del asistente no incluye 'generator_names'."
        )

    unknown = [name for name in generator_names if name not in GENERATOR_REGISTRY]
    if unknown:
        valid = ", ".join(sorted(GENERATOR_REGISTRY))
        raise SuggestStrategyError(
            f"Generadores desconocidos: {', '.join(unknown)}. Válidos: {valid}"
        )

    return OptimizationStrategy(
        name="ai_suggested",
        weights=weights,
        generator_names=tuple(generator_names),
    )
