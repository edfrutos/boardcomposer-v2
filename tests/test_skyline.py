from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_can_be_created():
    skyline = Skyline(3000)

    assert skyline.width_mm == 3000
    assert len(skyline.nodes) == 1

    node = skyline.nodes[0]

    assert node.x_mm == 0
    assert node.y_mm == 0
    assert node.width_mm == 3000
