from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle


def test_free_rectangle_area():
    rect = FreeRectangle(0, 0, 1000, 500)

    assert rect.area_mm2 == 500000


def test_free_rectangle_fits_piece():
    rect = FreeRectangle(0, 0, 1000, 500)

    assert rect.fits(800, 300) is True


def test_free_rectangle_rejects_large_piece():
    rect = FreeRectangle(0, 0, 1000, 500)

    assert rect.fits(1200, 300) is False
