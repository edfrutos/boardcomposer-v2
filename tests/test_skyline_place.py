from boardcomposer.solver.skyline.skyline import Skyline


def test_place_updates_skyline():
    skyline = Skyline(width_mm=3000)

    pos = skyline.place(
        width_mm=1000,
        height_mm=300,
    )

    assert pos is not None

    assert len(skyline.nodes) == 2

    assert skyline.nodes[0].x_mm == 0
    assert skyline.nodes[0].y_mm == 300
    assert skyline.nodes[0].width_mm == 1000

    assert skyline.nodes[1].x_mm == 1000
    assert skyline.nodes[1].y_mm == 0
    assert skyline.nodes[1].width_mm == 2000
