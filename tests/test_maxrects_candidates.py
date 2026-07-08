from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_find_candidates_returns_all_candidates():
    maxrects = MaxRects(3000, 1000)

    candidates = maxrects.find_candidates(
        1000,
        500,
    )

    assert len(candidates) == 1


def test_find_candidates_returns_multiple_candidates():
    maxrects = MaxRects()

    maxrects.free_rectangles = [
        FreeRectangle(0, 0, 3000, 1000),
        FreeRectangle(0, 1000, 1200, 600),
    ]

    candidates = maxrects.find_candidates(
        1000,
        500,
    )

    assert len(candidates) == 2


def test_place_candidate_updates_free_rectangles():
    maxrects = MaxRects(3000, 1000)

    candidate = maxrects.find_candidates(1000, 500)[0]

    maxrects.place_candidate(candidate)

    assert len(maxrects.free_rectangles) > 0
