import json

import pytest

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project.project_io import (
    load_project_from_file,
    project_from_dict,
    project_to_dict,
    save_project_to_file,
)


def _sample_project() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard(board_id="A", length_mm=2000, width_mm=300)],
        pieces=[StudioPiece(piece_id="p1", length_mm=500, width_mm=200)],
        placements=[
            StudioPlacement(
                piece_id="p1", x_mm=10, y_mm=20, board_id="A", rotated=True, rotation=90
            )
        ],
    )


def test_project_to_dict_and_back_round_trips():
    project = _sample_project()

    restored = project_from_dict(project_to_dict(project))

    assert restored == project


def test_save_and_load_project_round_trips(tmp_path):
    project = _sample_project()
    path = tmp_path / "demo.bcstudio.json"

    save_project_to_file(project, path)
    restored = load_project_from_file(path)

    assert restored == project


def test_project_from_dict_defaults_missing_board_id_to_the_first_board():
    # Legacy .bcstudio.json files predate IDE-0013 (multi-board support) and
    # have no "board_id" key on placements at all.
    legacy_data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"board_id": "A", "length_mm": 2000, "width_mm": 300}],
        "pieces": [{"piece_id": "p1", "length_mm": 500, "width_mm": 200}],
        "placements": [{"piece_id": "p1", "x_mm": 10, "y_mm": 20}],
    }

    project = project_from_dict(legacy_data)

    assert project.placements[0].board_id == "A"


def test_project_from_dict_leaves_board_id_none_without_any_boards():
    legacy_data = {
        "project_id": "proj-1",
        "name": "Demo",
        "pieces": [{"piece_id": "p1", "length_mm": 500, "width_mm": 200}],
        "placements": [{"piece_id": "p1", "x_mm": 10, "y_mm": 20}],
    }

    project = project_from_dict(legacy_data)

    assert project.placements[0].board_id is None


def test_project_from_dict_defaults_missing_thickness_to_19mm():
    # Legacy .bcstudio.json files predate the thickness_mm field and have no
    # "thickness_mm" key on boards/pieces at all.
    legacy_data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"board_id": "A", "length_mm": 2000, "width_mm": 300}],
        "pieces": [{"piece_id": "p1", "length_mm": 500, "width_mm": 200}],
        "placements": [],
    }

    project = project_from_dict(legacy_data)

    assert project.boards[0].thickness_mm == 19.0
    assert project.pieces[0].thickness_mm == 19.0


def test_project_to_dict_and_back_round_trips_a_custom_kerf():
    project = _sample_project()
    project.kerf_mm = 3.5

    restored = project_from_dict(project_to_dict(project))

    assert restored.kerf_mm == 3.5


def test_project_from_dict_defaults_missing_kerf_to_zero():
    # Legacy .bcstudio.json files predate the kerf_mm field.
    legacy_data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [],
        "pieces": [],
        "placements": [],
    }

    project = project_from_dict(legacy_data)

    assert project.kerf_mm == 0.0


def test_project_from_dict_ignores_unknown_extra_keys():
    # Seen in the wild: a .bcstudio.json not written by Studio itself (an
    # AI-generated project spec) with a "quantity" key per board/piece that
    # StudioBoard/StudioPiece don't have — used to crash the whole app with
    # a raw TypeError instead of just being ignored.
    data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [
            {"board_id": "A", "length_mm": 2000, "width_mm": 300, "quantity": 2}
        ],
        "pieces": [
            {"piece_id": "p1", "length_mm": 500, "width_mm": 200, "quantity": 3}
        ],
        "placements": [{"piece_id": "p1", "x_mm": 10, "y_mm": 20, "quantity": 1}],
    }

    project = project_from_dict(data)

    assert project.boards[0].board_id == "A"
    assert project.pieces[0].piece_id == "p1"


def test_project_from_dict_drops_a_placement_of_an_unknown_piece():
    data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"board_id": "A", "length_mm": 2000, "width_mm": 300}],
        "pieces": [{"piece_id": "p1", "length_mm": 500, "width_mm": 200}],
        "placements": [
            {"piece_id": "p9", "x_mm": 10, "y_mm": 20, "board_id": "A"},
            {"piece_id": "p1", "x_mm": 30, "y_mm": 40, "board_id": "A"},
        ],
    }
    warnings = []

    project = project_from_dict(data, on_warning=warnings.append)

    assert [placement.piece_id for placement in project.placements] == ["p1"]
    assert len(warnings) == 1
    assert "pieza inexistente" in warnings[0]


def test_project_from_dict_drops_a_placement_on_an_unknown_board():
    data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"board_id": "A", "length_mm": 2000, "width_mm": 300}],
        "pieces": [{"piece_id": "p1", "length_mm": 500, "width_mm": 200}],
        "placements": [{"piece_id": "p1", "x_mm": 10, "y_mm": 20, "board_id": "Z"}],
    }
    warnings = []

    project = project_from_dict(data, on_warning=warnings.append)

    assert project.placements == []
    assert len(warnings) == 1
    assert "tablero inexistente" in warnings[0]


def test_project_from_dict_keeps_the_rest_of_the_project_when_dropping_placements():
    # Dropping only the dangling placements is what makes a damaged file
    # recoverable — boards, pieces and kerf survive untouched.
    data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"board_id": "A", "length_mm": 2000, "width_mm": 300}],
        "pieces": [{"piece_id": "p1", "length_mm": 500, "width_mm": 200}],
        "placements": [{"piece_id": "p9", "x_mm": 10, "y_mm": 20, "board_id": "A"}],
        "kerf_mm": 3.2,
    }

    project = project_from_dict(data)

    assert project.placements == []
    assert [board.board_id for board in project.boards] == ["A"]
    assert [piece.piece_id for piece in project.pieces] == ["p1"]
    assert project.kerf_mm == 3.2


def test_project_from_dict_rejects_a_board_with_a_non_finite_dimension():
    # json.loads acepta el token NaN, así que un fichero de proyecto puede
    # traerlo. Aquí sí se rechaza el fichero entero: un tablero sin
    # dimensiones usables no deja nada que dibujar, al contrario que un
    # placement colgante (que sólo se descarta).
    data = json.loads(
        '{"project_id": "proj-1", "name": "Demo",'
        ' "boards": [{"board_id": "A", "length_mm": NaN, "width_mm": 300}],'
        ' "pieces": [], "placements": []}'
    )

    with pytest.raises(ValueError, match="length_mm"):
        project_from_dict(data)


def test_project_from_dict_rejects_a_piece_with_a_negative_dimension():
    data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"board_id": "A", "length_mm": 2000, "width_mm": 300}],
        "pieces": [{"piece_id": "p1", "length_mm": -500, "width_mm": 200}],
        "placements": [],
    }

    with pytest.raises(ValueError, match="length_mm"):
        project_from_dict(data)


def test_project_from_dict_raises_value_error_on_missing_required_field():
    data = {
        "project_id": "proj-1",
        "name": "Demo",
        "boards": [{"length_mm": 2000, "width_mm": 300}],  # falta board_id
    }

    with pytest.raises(ValueError, match="formato de proyecto no reconocido"):
        project_from_dict(data)
