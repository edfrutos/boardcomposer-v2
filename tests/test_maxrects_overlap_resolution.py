from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_split_overlap_removes_intersection_area():
    mr = MaxRects()

    fragments = mr._split_overlap(
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(250, 250, 500, 500),
    )

    assert fragments
    assert all(
        not mr._intersect(fragment, FreeRectangle(250, 250, 500, 500))
        for fragment in fragments
    )


def test_resolve_overlaps_removes_free_rectangle_intersections():
    mr = MaxRects()
    mr.free_rectangles = [
        FreeRectangle(0, 0, 1000, 1000),
        FreeRectangle(250, 250, 500, 500),
    ]

    mr._resolve_overlaps()

    assert len(mr.free_rectangles) == 1
