from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_initial_free_rectangle():
    mr = MaxRects(3000, 1500)

    assert len(mr.free_rectangles) == 1

    rect = mr.free_rectangles[0]

    assert rect.length_mm == 3000
    assert rect.width_mm == 1500
