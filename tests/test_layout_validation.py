from boardcomposer import BoardPlacement
from boardcomposer.layout.validation import has_overlaps


def test_has_overlaps_detects_collision():
    placements = [
        BoardPlacement("A", 0, 0, 100, 100),
        BoardPlacement("B", 50, 50, 100, 100),
    ]

    assert has_overlaps(placements) is True


def test_has_overlaps_accepts_valid_layout():
    placements = [
        BoardPlacement("A", 0, 0, 100, 100),
        BoardPlacement("B", 100, 0, 100, 100),
    ]

    assert has_overlaps(placements) is False
