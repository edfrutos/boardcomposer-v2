import pytest
from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.services import StudioServices


def _project_two_pieces_only_one_fits() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 100, 100)],
        pieces=[
            StudioPiece("p1", 80, 80),
            StudioPiece("p2", 80, 80),
        ],
    )


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    window = MainWindow(services=StudioServices())
    window.services.projects.new_project(_project_two_pieces_only_one_fits())
    window.workspace.reload_project()
    window.workspace.set_active_board("A")
    return window


def test_apply_layout_warns_about_pieces_left_unplaced(window):
    window.services.layout.solve_current_project("A")

    window._apply_layout()

    unplaced = window._unplaced_piece_ids()
    assert len(unplaced) == 1
    assert (
        window.statusBar()
        .currentMessage()
        .startswith("Layout aplicado — 1 pieza(s) sin colocar")
    )


def test_apply_comparison_solution_warns_about_pieces_left_unplaced(window):
    window.services.layout.compare_solutions("A")

    window._apply_comparison_solution(0)

    unplaced = window._unplaced_piece_ids()
    assert len(unplaced) == 1
    assert "sin colocar" in window.statusBar().currentMessage()
