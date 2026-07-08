from boardcomposer.layout import Rectangle


def test_rectangle_area_and_bounds():
    rect = Rectangle(0, 0, 2000, 300)

    assert rect.area_mm2 == 600000
    assert rect.right_mm == 2000
    assert rect.top_mm == 300


def test_rectangle_overlap():
    a = Rectangle(0, 0, 100, 100)
    b = Rectangle(50, 50, 100, 100)

    assert a.overlaps(b) is True


def test_rectangle_no_overlap_when_touching_edges():
    a = Rectangle(0, 0, 100, 100)
    b = Rectangle(100, 0, 100, 100)

    assert a.overlaps(b) is False
