from boardcomposer import BoardPlacement
from boardcomposer.layout.bounds import bounding_rectangle


def test_bounding_rectangle():
    placements = [
        BoardPlacement("A", 0, 0, 100, 100),
        BoardPlacement("B", 100, 50, 200, 100),
    ]

    bounds = bounding_rectangle(placements)

    assert bounds.x_mm == 0
    assert bounds.y_mm == 0
    assert bounds.length_mm == 300
    assert bounds.width_mm == 150
    assert bounds.area_mm2 == 45000


def test_bounding_rectangle_empty():
    bounds = bounding_rectangle([])

    assert bounds.x_mm == 0
    assert bounds.y_mm == 0
    assert bounds.length_mm == 0
    assert bounds.width_mm == 0
