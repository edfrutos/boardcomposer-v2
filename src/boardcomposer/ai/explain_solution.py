from boardcomposer.ai.provider import AIProvider
from boardcomposer.domain import AssemblySolution

PROMPT_TEMPLATE = (
    "Explica en lenguaje natural, en español y en un párrafo breve, la "
    "siguiente solución de corte de tableros: qué tan buena es y sus "
    "principales compensaciones (trade-offs). No inventes datos que no "
    "aparezcan a continuación.\n\n"
    "- Tablas colocadas: {placements}\n"
    "- Largo total: {total_length_mm} mm\n"
    "- Ancho total: {total_width_mm} mm\n"
    "- Desperdicio: {waste_ratio:.1%}\n"
    "- Puntuación total: {score_total}\n"
    "- Puntos fuertes: {strengths}\n"
    "- Puntos débiles: {weaknesses}\n"
    "- Notas: {notes}\n"
)


def explain_solution(solution: AssemblySolution, provider: AIProvider) -> str:
    prompt = PROMPT_TEMPLATE.format(
        placements=len(solution.placements),
        total_length_mm=solution.total_length_mm,
        total_width_mm=solution.total_width_mm,
        waste_ratio=solution.waste_ratio,
        score_total=solution.score.total,
        strengths=", ".join(solution.explanation.strengths) or "ninguno registrado",
        weaknesses=", ".join(solution.explanation.weaknesses) or "ninguno registrado",
        notes=", ".join(solution.explanation.notes) or "ninguna",
    )
    return provider.complete(prompt)
