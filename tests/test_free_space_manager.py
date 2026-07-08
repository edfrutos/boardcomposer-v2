from boardcomposer.layout import Rectangle
from boardcomposer.layout.free_space_manager import FreeSpaceManager


def test_free_space_manager_finds_space():
    manager = FreeSpaceManager.from_bounds(1000, 500)
    rect = Rectangle(0, 0, 600, 200)

    assert manager.find_space_for(rect) is not None


def test_free_space_manager_places_rectangle():
    manager = FreeSpaceManager.from_bounds(1000, 500)
    rect = Rectangle(0, 0, 600, 200)

    assert manager.place(rect) is True
    assert manager.free_area_mm2 == 380000


def test_free_space_manager_rejects_rectangle_that_does_not_fit():
    manager = FreeSpaceManager.from_bounds(1000, 500)
    rect = Rectangle(0, 0, 1200, 200)

    assert manager.place(rect) is False
    assert manager.free_area_mm2 == 500000
