from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_places_across_multiple_nodes():
    skyline = Skyline(width_mm=3000)
    skyline.nodes = [
        SkylineNode(x_mm=0, y_mm=100, width_mm=1000),
        SkylineNode(x_mm=1000, y_mm=200, width_mm=1000),
        SkylineNode(x_mm=2000, y_mm=100, width_mm=1000),
    ]

    position = skyline.place(width_mm=2500, height_mm=300)

    assert position is not None
    assert position.x_mm == 0
    assert position.y_mm == 200
    assert skyline.height_mm == 500
