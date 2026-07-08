from boardcomposer import BoardPlacement
from boardcomposer.geometry.collision import placements_overlap


def test_placements_overlap():
    a = BoardPlacement("A", 0, 0, 100, 100)
    b = BoardPlacement("B", 50, 50, 100, 100)

    assert placements_overlap(a, b) is True


def test_placements_do_not_overlap_when_touching_edges():
    a = BoardPlacement("A", 0, 0, 100, 100)
    b = BoardPlacement("B", 100, 0, 100, 100)

    assert placements_overlap(a, b) is False
