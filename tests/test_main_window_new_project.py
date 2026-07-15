import pytest
from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_new_project_creates_an_empty_project(window):
    window._new_project()

    project = window.services.projects.current_project

    assert project.name == "Nuevo proyecto"
    assert project.boards == []
    assert project.pieces == []
    assert project.placements == []


def test_new_project_does_not_reload_the_startup_demo_project(window):
    demo_project_id = window.services.projects.current_project.project_id

    window._new_project()

    assert window.services.projects.current_project.project_id != demo_project_id


def test_new_project_gets_a_fresh_id_each_time(window):
    window._new_project()
    first_id = window.services.projects.current_project.project_id

    window._new_project()
    second_id = window.services.projects.current_project.project_id

    assert first_id != second_id
