import json

from boardcomposer.ai.json_response import strip_json_fence
from boardcomposer.ai.provider import AIProvider
from boardcomposer.domain import Board, Project, ProjectConstraints

PROMPT_TEMPLATE = (
    "Extrae del siguiente texto en lenguaje natural las tablas a cortar y "
    "las restricciones del proyecto. Responde EXCLUSIVAMENTE con un objeto "
    "JSON, sin texto adicional, con esta forma:\n"
    '{{"boards": [{{"id": "string o null", "length_mm": numero, '
    '"width_mm": numero, "thickness_mm": numero}}], '
    '"constraints": {{"max_length_mm": numero o null, '
    '"max_width_mm": numero o null, "allow_rotation": booleano, '
    '"allow_cutting": booleano}}}}\n\n'
    "Texto:\n{text}"
)


class ProjectFromTextError(ValueError):
    """El proveedor de IA no devolvió un proyecto interpretable."""


def project_from_text(text: str, provider: AIProvider) -> Project:
    raw = provider.complete(PROMPT_TEMPLATE.format(text=text))

    try:
        payload = json.loads(strip_json_fence(raw))
    except json.JSONDecodeError as error:
        raise ProjectFromTextError(
            f"La respuesta del asistente no es JSON válido: {error}"
        ) from error

    if not isinstance(payload, dict):
        raise ProjectFromTextError(
            "La respuesta del asistente debe ser un objeto JSON."
        )

    boards_data = payload.get("boards")
    if not isinstance(boards_data, list) or not boards_data:
        raise ProjectFromTextError(
            "La respuesta del asistente no incluye tablas ('boards')."
        )

    try:
        boards = [
            Board(
                id=board.get("id"),
                length_mm=float(board["length_mm"]),
                width_mm=float(board["width_mm"]),
                # .get(..., 1) only covers a missing key: real providers (e.g.
                # AnthropicProvider) often include the key with an explicit
                # null when the input text doesn't mention a thickness.
                thickness_mm=float(
                    thickness
                    if (thickness := board.get("thickness_mm")) is not None
                    else 1
                ),
            )
            for board in boards_data
        ]
    except (KeyError, TypeError, ValueError) as error:
        raise ProjectFromTextError(
            f"Tabla inválida en la respuesta del asistente: {error}"
        ) from error

    constraints_data = payload.get("constraints") or {}
    if not isinstance(constraints_data, dict):
        raise ProjectFromTextError(
            "'constraints' debe ser un objeto en la respuesta del asistente."
        )

    try:
        constraints = ProjectConstraints(
            max_length_mm=constraints_data.get("max_length_mm"),
            max_width_mm=constraints_data.get("max_width_mm"),
            allow_rotation=bool(constraints_data.get("allow_rotation", False)),
            allow_cutting=bool(constraints_data.get("allow_cutting", False)),
        )
    except (TypeError, ValueError) as error:
        raise ProjectFromTextError(
            f"Restricciones inválidas en la respuesta del asistente: {error}"
        ) from error

    return Project(boards=boards, constraints=constraints)
