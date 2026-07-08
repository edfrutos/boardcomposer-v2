from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS


def test_maxrects_registers_expected_heuristics():
    assert [name for name, _ in MAXRECTS_HEURISTICS] == [
        "best_area_fit",
        "best_short_side_fit",
        "best_long_side_fit",
        "best_bottom_left_fit",
    ]
