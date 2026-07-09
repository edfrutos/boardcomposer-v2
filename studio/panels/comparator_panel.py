"""Content builder for the Comparador panel (SCR-003 — Comparador de Soluciones).

Pure function, no Qt dependency, so it's unit-testable. Shows only the
metrics AssemblySolution actually computes today (aprovechamiento,
desperdicio, piezas colocadas, puntuación, algoritmo, explicación) — the
spec also lists número de cortes, tiempo de cálculo, fragmentación del
material and tiempo estimado de mecanizado, none of which the domain
model tracks yet, so they're called out as not-yet-available instead of
being filled with invented numbers.
"""

from boardcomposer.domain import AssemblySolution


def render_comparison(solutions: list[AssemblySolution]) -> str:
    if not solutions:
        return (
            "<h3>Comparador</h3>"
            "<p>No hay soluciones para comparar. Usa "
            '"Comparar → Generar comparación".</p>'
        )

    headers = "".join(f"<th>Solución {i + 1}</th>" for i in range(len(solutions)))
    rows = [
        _row("Algoritmo", [" / ".join(s.explanation.notes) or "—" for s in solutions]),
        _row("Piezas colocadas", [str(len(s.placements)) for s in solutions]),
        _row("Aprovechamiento", [f"{1 - s.waste_ratio:.1%}" for s in solutions]),
        _row("Desperdicio", [f"{s.waste_ratio:.1%}" for s in solutions]),
        _row("Puntuación", [f"{s.score.total:.1f}" for s in solutions]),
    ]

    explanations = []
    for index, solution in enumerate(solutions):
        explanations.append(f"<h4>Explicación — Solución {index + 1}</h4>")
        if solution.explanation.strengths:
            explanations.append(
                "<p><b>Fortalezas:</b> "
                + "; ".join(solution.explanation.strengths)
                + "</p>"
            )
        if solution.explanation.weaknesses:
            explanations.append(
                "<p><b>Debilidades:</b> "
                + "; ".join(solution.explanation.weaknesses)
                + "</p>"
            )

    return (
        "<h3>Comparador de Soluciones</h3>"
        f"<table border='1' cellpadding='4' cellspacing='0'>"
        f"<tr><th></th>{headers}</tr>"
        f"{''.join(rows)}"
        "</table>"
        "<p><i>Número de cortes, tiempo de cálculo, fragmentación del material y "
        "tiempo estimado de mecanizado no se calculan todavía "
        "(ver docs/masterplan/ui/SCR-003-Comparador.md).</i></p>"
        f"{''.join(explanations)}"
    )


def _row(label: str, values: list[str]) -> str:
    cells = "".join(f"<td>{value}</td>" for value in values)
    return f"<tr><td><b>{label}</b></td>{cells}</tr>"
