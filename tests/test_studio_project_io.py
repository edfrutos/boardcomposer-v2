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
            StudioPlacement(piece_id="p1", x_mm=10, y_mm=20, rotated=True, rotation=90)
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
