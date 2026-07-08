from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_merges_adjacent_nodes_with_same_height():
    skyline = Skyline(width_mm=3000)
    skyline.nodes = [
        SkylineNode(x_mm=0, y_mm=0, width_mm=1000),
        SkylineNode(x_mm=1000, y_mm=0, width_mm=2000),
    ]

    skyline._merge_adjacent_nodes()

    assert len(skyline.nodes) == 1
    assert skyline.nodes[0].x_mm == 0
    assert skyline.nodes[0].width_mm == 3000
