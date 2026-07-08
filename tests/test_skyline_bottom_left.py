from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.skyline import Skyline


def test_bottom_left_prefers_lowest_then_leftmost():
    skyline = Skyline(width_mm=3000)
    skyline.nodes = [
        SkylineNode(x_mm=0, y_mm=0, width_mm=1000),
        SkylineNode(x_mm=1000, y_mm=0, width_mm=1000),
        SkylineNode(x_mm=2000, y_mm=200, width_mm=1000),
    ]

    position = skyline.find_position(width_mm=500)

    assert position is not None
    assert position.x_mm == 0
    assert position.y_mm == 0
