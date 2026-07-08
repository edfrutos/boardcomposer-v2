from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_split_overlap_center_creates_four_fragments():
    mr = MaxRects()

    fragments = mr._split_overlap(
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(250, 250, 500, 500),
    )

    assert len(fragments) == 4


def test_split_overlap_identical_rectangle_returns_empty():
    mr = MaxRects()

    fragments = mr._split_overlap(
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(0, 0, 1000, 1000),
    )

    assert fragments == []


def test_split_overlap_without_intersection_returns_original():
    mr = MaxRects()

    original = FreeRectangle(0, 0, 1000, 1000)

    fragments = mr._split_overlap(
        original,
        FreeRectangle(1500, 0, 500, 500),
    )

    assert fragments == [original]
