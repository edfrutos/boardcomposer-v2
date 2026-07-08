from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_nodes_remain_ordered_after_place():
    skyline = Skyline(width_mm=3000)
    skyline.nodes = [
        SkylineNode(x_mm=1000, y_mm=0, width_mm=2000),
        SkylineNode(x_mm=0, y_mm=300, width_mm=1000),
    ]

    skyline.place(width_mm=500, height_mm=200)

    xs = [node.x_mm for node in skyline.nodes]

    assert xs == sorted(xs)
