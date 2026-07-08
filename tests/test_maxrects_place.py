from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_place_piece_splits_free_rectangles():
    maxrects = MaxRects(3000, 1000)

    placement = maxrects.place(1000, 500)

    assert placement is not None
    assert len(maxrects.free_rectangles) >= 1


def test_place_piece_returns_none_when_it_does_not_fit():
    maxrects = MaxRects(3000, 1000)

    placement = maxrects.place(4000, 500)

    assert placement is None
