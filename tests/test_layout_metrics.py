import pytest

from boardcomposer.domain import AssemblySolution, BoardPlacement
from boardcomposer.solver.layout_metrics import cut_count, fragmentation_ratio


def test_no_placements_gives_zero_for_both_metrics():
    solution = AssemblySolution(placements=[])

    assert fragmentation_ratio(solution) == 0.0
    assert cut_count(solution) == 0


def test_single_piece_filling_the_bounds_has_no_fragmentation_or_cuts():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    assert fragmentation_ratio(solution) == 0.0
    assert cut_count(solution) == 0


def test_two_pieces_side_by_side_with_no_gap_is_one_cut_no_fragmentation():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 100),
            BoardPlacement("B", 100, 0, 100, 100),
        ]
    )

    # Fully packed bounds — nothing left to fragment.
    assert fragmentation_ratio(solution) == 0.0
    # One vertical line at x=100 serves both pieces (DEC-0016: N piezas en
    # fila = N-1 cortes).
    assert cut_count(solution) == 1


def test_fragmentation_and_cuts_with_uneven_gaps():
    # Three 50x50 pieces along a 300x50 bounding rectangle, at x=0, x=100,
    # x=250 — two free gaps of different sizes (50x50 and 100x50).
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 50, 50),
            BoardPlacement("B", 100, 0, 50, 50),
            BoardPlacement("C", 250, 0, 50, 50),
        ]
    )

    # total_free = 300*50 - 3*50*50 = 15000 - 7500 = 7500
    # largest free rectangle = the 100x50 gap = 5000
    # fragmentation = 1 - 5000/7500
    assert fragmentation_ratio(solution) == pytest.approx(1 - 5000 / 7500)
    # Four distinct interior x-lines: 50, 100, 150, 250. No y-lines (every
    # piece spans the full bounding height).
    assert cut_count(solution) == 4


def test_fragmentation_ratio_is_between_zero_and_one():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 50, 50),
            BoardPlacement("B", 100, 0, 50, 50),
            BoardPlacement("C", 250, 0, 50, 50),
        ]
    )

    assert 0.0 <= fragmentation_ratio(solution) <= 1.0
