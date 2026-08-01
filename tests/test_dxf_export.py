from studio.export.dxf_export import export_project_to_dxf
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


def _project_with_piece() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 10, 20, board_id="A")],
    )


def test_export_project_to_dxf_writes_a_valid_dxf_file(tmp_path):
    path = tmp_path / "demo.dxf"

    result = export_project_to_dxf(_project_with_piece(), path)

    assert result is True
    content = path.read_text(encoding="utf-8")
    assert "SECTION" in content
    assert "ENDSEC" in content
    assert "p1" in content


def test_export_project_to_dxf_returns_false_without_placements(tmp_path):
    project = StudioProject(project_id="proj-1", name="Demo")
    path = tmp_path / "empty.dxf"

    result = export_project_to_dxf(project, path)

    assert result is False
    assert not path.exists()
