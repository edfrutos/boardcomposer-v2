from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_place_rotates_when_it_only_fits_rotated():
    skyline = Skyline(width_mm=500)

    placement = skyline.place(
        width_mm=800,
        height_mm=400,
        allow_rotation=True,
    )

    assert placement is not None
    assert placement.rotated is True
