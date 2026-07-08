from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.skyline import Skyline


def test_place_uses_best_node():
    skyline = Skyline(width_mm=3000)
    skyline.nodes = [
        SkylineNode(x_mm=0, y_mm=300, width_mm=1000),
        SkylineNode(x_mm=1000, y_mm=0, width_mm=2000),
    ]

    position = skyline.place(width_mm=500, height_mm=200)

    assert position is not None
    assert position.x_mm == 1000
    assert position.y_mm == 0
