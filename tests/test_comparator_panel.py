from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    SolutionExplanation,
    SolutionScore,
)
from studio.panels.comparator_panel import render_comparison


def _solution(
    board_id: str,
    length_mm: float,
    width_mm: float,
    score_total: float,
    notes: list[str],
    strengths: list[str] | None = None,
    weaknesses: list[str] | None = None,
) -> AssemblySolution:
    return AssemblySolution(
        placements=[
            BoardPlacement(
                board_id=board_id,
                x_mm=0,
                y_mm=0,
                length_mm=length_mm,
                width_mm=width_mm,
            )
        ],
        score=SolutionScore(waste_score=score_total),
        explanation=SolutionExplanation(
            notes=notes, strengths=strengths or [], weaknesses=weaknesses or []
        ),
    )


def test_render_comparison_with_no_solutions_explains_how_to_generate():
    html = render_comparison([])

    assert "No hay soluciones" in html
    assert "Comparar" in html


def test_render_comparison_shows_one_column_per_solution():
    solutions = [
        _solution("A", 500, 500, 40.0, ["skyline", "original"]),
        _solution("B", 500, 500, 35.0, ["maxrects", "best_area_fit", "largest_area"]),
    ]

    html = render_comparison(solutions)

    assert "Solución 1" in html
    assert "Solución 2" in html
    assert "skyline / original" in html
    assert "maxrects / best_area_fit / largest_area" in html
    assert "Piezas colocadas" in html
    assert "Aprovechamiento" in html
    assert "Desperdicio" in html
    assert "Puntuación" in html
    assert "40.0" in html
    assert "35.0" in html


def test_render_comparison_notes_missing_metrics_are_not_fabricated():
    html = render_comparison([_solution("A", 500, 500, 10.0, ["skyline"])])

    assert "no se calculan todavía" in html
    assert "cortes" in html
    assert "mecanizado" in html


def test_render_comparison_includes_strengths_and_weaknesses():
    solution = _solution(
        "A",
        500,
        500,
        10.0,
        ["skyline"],
        strengths=["Muy buen aprovechamiento del material"],
        weaknesses=["Composición alargada o poco compacta"],
    )

    html = render_comparison([solution])

    assert "Muy buen aprovechamiento del material" in html
    assert "Composición alargada o poco compacta" in html
