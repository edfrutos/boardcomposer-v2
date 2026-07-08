from boardcomposer.solver.skyline.node import SkylineNode


def test_skyline_node():
    node = SkylineNode(x_mm=0, y_mm=0, width_mm=3000)

    assert node.x_mm == 0
    assert node.y_mm == 0
    assert node.width_mm == 3000
