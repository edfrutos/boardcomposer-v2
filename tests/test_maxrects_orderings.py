from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS


def test_maxrects_has_board_orderings():

    assert [name for name, _ in MAXRECTS_BOARD_ORDERINGS] == [
        "original",
        "largest_area",
        "longest_edge",
    ]
