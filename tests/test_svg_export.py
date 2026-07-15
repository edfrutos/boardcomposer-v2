from studio.export.svg_export import export_project_to_svg
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


def _project_with_piece() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 10, 20, board_id="A")],
    )


def test_export_project_to_svg_writes_a_valid_svg_file(tmp_path):
    path = tmp_path / "demo.svg"

    result = export_project_to_svg(_project_with_piece(), path)

    assert result is True
    content = path.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert 'x="10.0"' in content or 'x="10"' in content
    assert "p1" in content


def test_export_project_to_svg_returns_false_without_placements(tmp_path):
    project = StudioProject(project_id="proj-1", name="Demo")
    path = tmp_path / "empty.svg"

    result = export_project_to_svg(project, path)

    assert result is False
    assert not path.exists()
