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


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("field", ["x_mm", "y_mm", "length_mm", "width_mm"])
def test_board_placement_rejects_non_finite_values(field, value):
    # `nan < 0` and `nan <= 0` are both False, so the plain comparisons let
    # NaN through — see Board.__post_init__.
    geometry = {"x_mm": 0.0, "y_mm": 0.0, "length_mm": 2000.0, "width_mm": 300.0}
    geometry[field] = value

    with pytest.raises(ValueError):
        BoardPlacement(
            board_id="A",
            x_mm=geometry["x_mm"],
            y_mm=geometry["y_mm"],
            length_mm=geometry["length_mm"],
            width_mm=geometry["width_mm"],
        )
