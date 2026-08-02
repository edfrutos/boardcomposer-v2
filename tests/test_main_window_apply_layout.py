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


def test_apply_comparison_solution_logs_the_readable_label_and_id(window):
    solutions = window.services.layout.compare_solutions("A")
    solution_id = solutions[0].solution_id

    window._apply_comparison_solution(0)

    entry = window.services.activity.entries[0]
    assert entry.message.startswith(f"Solución A (#{solution_id})")
    assert entry.category == "layout"


def _project_two_boards_leftover_fits_the_other():
    return StudioProject(
        project_id="proj-2",
        name="Demo",
        boards=[
            StudioBoard("A", 2000, 300),
            StudioBoard("B", 600, 300),
        ],
        pieces=[
            StudioPiece("p1", 500, 300),  # fits on B
            StudioPiece("p2", 700, 300),  # too long for B, fits only A
        ],
    )


def test_apply_layout_places_leftover_on_another_empty_board():
    QApplication.instance() or QApplication([])
    leftover_window = MainWindow(services=StudioServices())
    leftover_window.services.projects.new_project(
        _project_two_boards_leftover_fits_the_other()
    )
    leftover_window.workspace.reload_project()
    leftover_window.workspace.set_active_board("B")

    leftover_window.services.layout.solve_current_project("B")
    leftover_window._apply_layout()

    project = leftover_window.services.projects.current_project
    assert not leftover_window._unplaced_piece_ids()
    assert project.placement_by_piece_id("p1").board_id == "B"
    assert project.placement_by_piece_id("p2").board_id == "A"
    assert leftover_window.statusBar().currentMessage() == "Layout aplicado al proyecto"
