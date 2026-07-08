import pytest

from boardcomposer import BoardPlacement


def test_board_placement_area():
    placement = BoardPlacement(
        board_id="A",
        x_mm=0,
        y_mm=0,
        length_mm=2000,
        width_mm=300,
    )

    assert placement.area_mm2 == 600000


def test_board_placement_bounds():
    placement = BoardPlacement(
        board_id="A",
        x_mm=100,
        y_mm=50,
        length_mm=2000,
        width_mm=300,
    )

    assert placement.right_mm == 2100
    assert placement.top_mm == 350


def test_board_placement_rejects_negative_position():
    with pytest.raises(ValueError):
        BoardPlacement(
            board_id="A",
            x_mm=-1,
            y_mm=0,
            length_mm=2000,
            width_mm=300,
        )
