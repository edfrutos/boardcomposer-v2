import pytest

from studio.models import StudioBoard, StudioPiece, StudioPlacement


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), 0, -500])
@pytest.mark.parametrize("field", ["length_mm", "width_mm", "thickness_mm"])
def test_studio_board_rejects_unusable_dimensions(field, value):
    dimensions = {"length_mm": 2000.0, "width_mm": 300.0, "thickness_mm": 19.0}
    dimensions[field] = value

    with pytest.raises(ValueError, match=field):
        StudioBoard(
            "TAB-001",
            length_mm=dimensions["length_mm"],
            width_mm=dimensions["width_mm"],
            thickness_mm=dimensions["thickness_mm"],
        )


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), 0, -500])
@pytest.mark.parametrize("field", ["length_mm", "width_mm", "thickness_mm"])
def test_studio_piece_rejects_unusable_dimensions(field, value):
    dimensions = {"length_mm": 700.0, "width_mm": 300.0, "thickness_mm": 19.0}
    dimensions[field] = value

    with pytest.raises(ValueError, match=field):
        StudioPiece(
            "P-001",
            length_mm=dimensions["length_mm"],
            width_mm=dimensions["width_mm"],
            thickness_mm=dimensions["thickness_mm"],
        )


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("field", ["x_mm", "y_mm"])
def test_studio_placement_rejects_non_finite_coordinates(field, value):
    coordinates = {"x_mm": 0.0, "y_mm": 0.0}
    coordinates[field] = value

    with pytest.raises(ValueError, match=field):
        StudioPlacement(
            "P-001",
            x_mm=coordinates["x_mm"],
            y_mm=coordinates["y_mm"],
            board_id="TAB-001",
        )


def test_studio_placement_allows_negative_coordinates():
    # Una pieza arrastrada fuera del tablero pasa por coordenadas negativas
    # antes de que la validación de encaje la recoloque: eso no es un error.
    placement = StudioPlacement("P-001", x_mm=-50, y_mm=-10, board_id="TAB-001")

    assert (placement.x_mm, placement.y_mm) == (-50, -10)
