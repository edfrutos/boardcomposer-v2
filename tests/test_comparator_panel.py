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

    assert "Solución A" in html
    assert "Solución B" in html
    assert f"#{solutions[0].solution_id}" in html
    assert f"#{solutions[1].solution_id}" in html
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
    assert "mecanizado" in html


def test_render_comparison_shows_fragmentation_and_cut_count():
    solutions = [
        _solution("A", 500, 500, 10.0, ["skyline"]),
        _solution("B", 500, 500, 10.0, ["maxrects"]),
    ]

    html = render_comparison(solutions)

    assert "Fragmentación" in html
    assert "Nº de cortes" in html
    # Single-piece solution: nothing to fragment, no interior cut line.
    assert "0.0%" in html


def test_render_comparison_marks_the_favorite_with_a_star():
    solutions = [
        _solution("A", 500, 500, 10.0, ["skyline"]),
        _solution("B", 500, 500, 10.0, ["maxrects"]),
    ]

    html = render_comparison(solutions, favorite_index=1)

    assert "⭐ Solución B" in html
    assert "⭐ Solución A" not in html


def test_render_comparison_without_a_favorite_has_no_star():
    html = render_comparison([_solution("A", 500, 500, 10.0, ["skyline"])])

    assert "⭐" not in html


def test_render_comparison_embeds_provided_thumbnails():
    solutions = [_solution("A", 500, 500, 10.0, ["skyline"])]

    html = render_comparison(solutions, thumbnails=["data:image/png;base64,AAAA"])

    assert 'src="data:image/png;base64,AAAA"' in html


def test_render_comparison_without_thumbnails_shows_a_placeholder():
    html = render_comparison([_solution("A", 500, 500, 10.0, ["skyline"])])

    assert "<td>—</td>" in html


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


def test_render_comparison_shows_piece_order():
    html = render_comparison([_solution("A", 500, 500, 10.0, ["skyline"])])

    assert "Orden de piezas" in html
    assert "A" in html


def test_render_comparison_distinguishes_tied_solutions_by_piece_order():
    # Same aggregate metrics (score, algorithm), different stacking order —
    # exactly the DT-0016 scenario: two genuinely different solutions that
    # would otherwise look identical in the table.
    tied_score = 92.4
    solution_1 = AssemblySolution(
        placements=[
            BoardPlacement(board_id="p1", x_mm=0, y_mm=0, length_mm=700, width_mm=300),
            BoardPlacement(
                board_id="p2", x_mm=0, y_mm=300, length_mm=520, width_mm=360
            ),
        ],
        score=SolutionScore(waste_score=tied_score),
        explanation=SolutionExplanation(notes=["vertical_permutation"]),
    )
    solution_2 = AssemblySolution(
        placements=[
            BoardPlacement(board_id="p2", x_mm=0, y_mm=0, length_mm=520, width_mm=360),
            BoardPlacement(
                board_id="p1", x_mm=0, y_mm=360, length_mm=700, width_mm=300
            ),
        ],
        score=SolutionScore(waste_score=tied_score),
        explanation=SolutionExplanation(notes=["vertical_permutation"]),
    )

    html = render_comparison([solution_1, solution_2])

    assert "p1 → p2" in html
    assert "p2 → p1" in html


def test_render_comparison_piece_order_handles_no_placements():
    solution = AssemblySolution(placements=[])

    html = render_comparison([solution])

    assert "Orden de piezas" in html
