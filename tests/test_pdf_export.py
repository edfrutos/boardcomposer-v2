import sys

import pytest
from PySide6.QtWidgets import QApplication

from studio.export.pdf_export import export_project_to_pdf
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


@pytest.fixture(scope="session", autouse=True)
def qapp():
    return QApplication.instance() or QApplication(sys.argv)


def _project_with_piece() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 10, 20, board_id="A")],
    )


def test_export_project_to_pdf_writes_a_valid_pdf_file(tmp_path):
    path = tmp_path / "demo.pdf"

    result = export_project_to_pdf(_project_with_piece(), path)

    assert result is True
    assert path.read_bytes().startswith(b"%PDF")
    assert path.stat().st_size > 0


def test_export_project_to_pdf_returns_false_without_placements(tmp_path):
    project = StudioProject(project_id="proj-1", name="Demo")
    path = tmp_path / "empty.pdf"

    result = export_project_to_pdf(project, path)

    assert result is False
    assert not path.exists()
