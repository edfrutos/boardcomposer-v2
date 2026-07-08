from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_prune_removes_contained_rectangles():
    mr = MaxRects()

    mr.free_rectangles = [
        FreeRectangle(0, 0, 3000, 3000),
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(1000, 1000, 500, 500),
    ]

    mr._prune_free_rectangles()

    assert len(mr.free_rectangles) == 1
