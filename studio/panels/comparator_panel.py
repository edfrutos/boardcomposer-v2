"""Content builder for the Comparador panel (SCR-003 — Comparador de Soluciones).

Pure function, no Qt dependency, so it's unit-testable. Shows the metrics
AssemblySolution computes (aprovechamiento, desperdicio, piezas colocadas,
puntuación, algoritmo, explicación) plus, since IDE-0023,
fragmentación/nº de cortes (`solver/layout_metrics.py` — the latter is a
labelled approximation, not an exact count, see its docstring). Tiempo de
cálculo and tiempo estimado de mecanizado still aren't computed anywhere
in the domain, so they're called out as not-yet-available instead of
being filled with invented numbers.

Also shows "Orden de piezas" (DT-0016): several candidates from the same
generator family can tie on every aggregate metric above (e.g. stacking
the same pieces in a different order occupies the same total footprint),
which otherwise makes genuinely distinct solutions look identical in the
table. This row surfaces the one thing that actually differs between
them — the piece arrangement, read top-to-bottom then left-to-right.
"""

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.layout_metrics import cut_count, fragmentation_ratio
from studio.solution_labels import solution_label


def render_comparison(
    solutions: list[AssemblySolution],
    thumbnails: list[str] | None = None,
    favorite_index: int | None = None,
) -> str:
    if not solutions:
        return (
            '<table id="empty-state-table"><tr><td id="empty-state">'
            "<h3>Comparador</h3>"
            "<p>No hay soluciones para comparar. Usa "
            '"Comparar → Generar comparación".</p>'
            "</td></tr></table>"
        )

    thumbnails = thumbnails or []
    headers = "".join(
        f"<th>{'⭐ ' if i == favorite_index else ''}Solución {solution_label(i)}"
        f"<br><small>#{solutions[i].solution_id}</small></th>"
        for i in range(len(solutions))
    )
    thumbnail_cells = "".join(
        f'<td><img src="{thumbnails[i]}" width="120" height="90"></td>'
        if i < len(thumbnails) and thumbnails[i]
        else "<td>—</td>"
        for i in range(len(solutions))
    )
    rows = [
        _row("Algoritmo", [" / ".join(s.explanation.notes) or "—" for s in solutions]),
        _row("Piezas colocadas", [str(len(s.placements)) for s in solutions]),
        _row("Orden de piezas", [_piece_order(s) for s in solutions]),
        _row("Aprovechamiento", [f"{1 - s.waste_ratio:.1%}" for s in solutions]),
        _row("Desperdicio", [f"{s.waste_ratio:.1%}" for s in solutions]),
        _row(
            "Fragmentación",
            [f"{fragmentation_ratio(s):.1%}" for s in solutions],
        ),
        _row("Nº de cortes (aprox.)", [str(cut_count(s)) for s in solutions]),
        _row("Puntuación", [f"{s.score.total:.1f}" for s in solutions]),
    ]

    explanations = []
    for index, solution in enumerate(solutions):
        explanations.append(f"<h4>Explicación — Solución {solution_label(index)}</h4>")
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
        "<table>"
        f"<tr><th></th>{headers}</tr>"
        f"<tr><th></th>{thumbnail_cells}</tr>"
        f"{''.join(rows)}"
        "</table>"
        "<p><i>Nº de cortes es una aproximación (corte guillotina de línea "
        "completa, DEC-0016) — puede infracontar en layouts no-guillotina. "
        "Tiempo de cálculo y tiempo estimado de mecanizado no se calculan "
        "todavía (ver docs/masterplan/ui/SCR-003-Comparador.md).</i></p>"
        f"{''.join(explanations)}"
    )


def _row(label: str, values: list[str]) -> str:
    cells = "".join(f"<td>{value}</td>" for value in values)
    return f"<tr><th>{label}</th>{cells}</tr>"


def _piece_order(solution: AssemblySolution) -> str:
    if not solution.placements:
        return "—"

    ordered = sorted(solution.placements, key=lambda p: (p.y_mm, p.x_mm))
    return " → ".join(placement.board_id for placement in ordered)
