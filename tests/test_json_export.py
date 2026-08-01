import json

from studio.export.json_export import export_project_to_json
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


def _project_with_piece() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 10, 20, board_id="A")],
    )


def test_export_project_to_json_writes_valid_json(tmp_path):
    path = tmp_path / "demo.json"

    result = export_project_to_json(_project_with_piece(), path)

    assert result is True
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["project_name"] == "Demo"
    assert data["placed_pieces"] == 1
    assert data["placements"] == [
        {
            "piece_id": "p1",
            "x_mm": 10,
            "y_mm": 20,
            "length_mm": 500,
            "width_mm": 200,
            "rotated": False,
        }
    ]


def test_export_project_to_json_returns_false_without_placements(tmp_path):
    project = StudioProject(project_id="proj-1", name="Demo")
    path = tmp_path / "empty.json"

    result = export_project_to_json(project, path)

    assert result is False
    assert not path.exists()
