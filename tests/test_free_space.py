from boardcomposer.layout.free_space import FreeSpace
from boardcomposer.layout import Rectangle


def test_free_space_fits_rectangle():
    space = FreeSpace(Rectangle(0, 0, 1000, 500))
    rect = Rectangle(0, 0, 800, 300)

    assert space.fits(rect) is True


def test_free_space_rejects_large_rectangle():
    space = FreeSpace(Rectangle(0, 0, 1000, 500))
    rect = Rectangle(0, 0, 1200, 300)

    assert space.fits(rect) is False


def test_free_space_split():
    space = FreeSpace(Rectangle(0, 0, 1000, 500))
    used = Rectangle(0, 0, 600, 200)

    spaces = space.split(used)

    assert len(spaces) == 2
    assert sum(s.area_mm2 for s in spaces) == 380000
