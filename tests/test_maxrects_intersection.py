from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_intersection_detected():
    mr = MaxRects()

    assert mr._intersect(
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(500, 500, 1000, 1000),
    )


def test_intersection_not_detected():
    mr = MaxRects()

    assert not mr._intersect(
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(1500, 0, 1000, 1000),
    )
