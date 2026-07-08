from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_find_best_rectangle():
    maxrects = MaxRects(3000, 1000)

    placement = maxrects.find_best_rectangle(1000, 500)

    assert placement is not None
    assert placement.x_mm == 0
    assert placement.y_mm == 0
    assert placement.length_mm == 1000
    assert placement.width_mm == 500


def test_find_best_rectangle_returns_none_when_it_does_not_fit():
    maxrects = MaxRects(3000, 1000)

    placement = maxrects.find_best_rectangle(4000, 500)

    assert placement is None


def test_find_best_rectangle_prefers_less_waste():
    maxrects = MaxRects(3000, 1000)
    maxrects.free_rectangles = [
        FreeRectangle(0, 0, 3000, 1000),
        FreeRectangle(0, 1000, 1000, 500),
    ]

    placement = maxrects.find_best_rectangle(900, 400)

    assert placement is not None
    assert placement.x_mm == 0
    assert placement.y_mm == 1000


def test_find_best_rectangle_can_rotate():
    maxrects = MaxRects(500, 1000)

    placement = maxrects.find_best_rectangle(
        800,
        400,
        allow_rotation=True,
    )

    assert placement is not None
    assert placement.rotated is True
    assert placement.length_mm == 400
    assert placement.width_mm == 800


def test_custom_heuristic_is_used():
    maxrects = MaxRects(3000, 1000)

    def select_last(candidates, waste_area):
        del waste_area
        return candidates[-1] if candidates else None

    # The first free rectangle is an exact fit (zero waste), so the default
    # heuristic (best_area_fit) would pick it. The second one fits with more
    # waste and comes last in candidate order, so select_last must pick it
    # instead. This proves find_best_rectangle actually delegates to the
    # injected heuristic rather than coincidentally agreeing with it.
    maxrects.free_rectangles = [
        FreeRectangle(0, 0, 900, 400),
        FreeRectangle(0, 1000, 3000, 1000),
    ]
    maxrects.heuristic = select_last

    placement = maxrects.find_best_rectangle(900, 400)

    candidates = maxrects.find_candidates(900, 400)
    assert placement == candidates[-1]
    assert placement.x_mm == 0
    assert placement.y_mm == 1000
