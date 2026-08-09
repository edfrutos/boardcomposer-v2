import json

import pytest

from boardcomposer import Board, Project


def test_board_area():
    board = Board(length_mm=2000, width_mm=300, thickness_mm=20)
    assert board.area_mm2 == 600000


def test_board_material_defaults_to_empty_string():
    board = Board(length_mm=2000, width_mm=300, thickness_mm=20)
    assert board.material == ""


def test_board_material_is_a_passive_label():
    board = Board(length_mm=2000, width_mm=300, thickness_mm=20, material="Roble")
    assert board.material == "Roble"


def test_board_requires_positive_dimensions():
    with pytest.raises(ValueError):
        Board(length_mm=0, width_mm=300, thickness_mm=20)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("field", ["length_mm", "width_mm", "thickness_mm"])
def test_board_rejects_non_finite_dimensions(field, value):
    dimensions = {"length_mm": 2000.0, "width_mm": 300.0, "thickness_mm": 20.0}
    dimensions[field] = value

    with pytest.raises(ValueError):
        Board(
            length_mm=dimensions["length_mm"],
            width_mm=dimensions["width_mm"],
            thickness_mm=dimensions["thickness_mm"],
        )


def test_board_rejects_non_finite_dimensions_parsed_from_json():
    # Python's json.loads accepts the bare tokens NaN/Infinity, so these reach
    # the domain straight from an API payload or a project file.
    payload = json.loads('{"length_mm": NaN, "width_mm": Infinity}')

    with pytest.raises(ValueError):
        Board(
            length_mm=payload["length_mm"],
            width_mm=payload["width_mm"],
            thickness_mm=20,
        )


def test_project_total_area():
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20))
    project.add_board(Board(length_mm=1000, width_mm=200, thickness_mm=20))

    assert project.total_area_mm2 == 800000
