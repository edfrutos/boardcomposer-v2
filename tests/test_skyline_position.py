from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_finds_position_for_piece_that_fits():
    skyline = Skyline(width_mm=3000)

    position = skyline.find_position(width_mm=1000)

    assert position is not None
    assert position.x_mm == 0
    assert position.y_mm == 0


def test_skyline_returns_none_when_piece_does_not_fit():
    skyline = Skyline(width_mm=1000)

    position = skyline.find_position(width_mm=1200)

    assert position is None
