from boardcomposer.solver.skyline.placement import SkylinePlacement


def test_skyline_placement_can_store_rotation():
    placement = SkylinePlacement(x_mm=0, y_mm=0, rotated=True)

    assert placement.rotated is True
