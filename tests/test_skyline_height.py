from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_height_after_place():
    skyline = Skyline(width_mm=3000)

    skyline.place(width_mm=1000, height_mm=300)

    assert skyline.height_mm == 300
