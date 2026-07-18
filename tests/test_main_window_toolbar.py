import pytest
from PySide6.QtWidgets import QApplication, QToolBar

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_main_window_has_a_toolbar(window):
    toolbars = window.findChildren(QToolBar)

    assert len(toolbars) == 1


def test_toolbar_includes_the_most_used_actions(window):
    toolbar = window.findChildren(QToolBar)[0]
    action_texts = {action.text() for action in toolbar.actions()}

    for expected in (
        "Nuevo proyecto",
        "Guardar",
        "Deshacer",
        "Añadir tablero…",
        "Calcular layout",
        "Generar comparación",
    ):
        assert expected in action_texts


ICONIFIED_ACTIONS = [
    "new_project",
    "open",
    "save",
    "undo",
    "redo",
    "rotate_piece",
    "delete_piece",
    "add_board",
    "edit_board",
    "add_piece",
    "edit_piece",
    "move_piece_to_board",
    "configure_kerf",
    "solve_layout",
    "apply_layout",
    "compare_solutions",
    "export_svg",
    "export_pdf",
]


@pytest.mark.parametrize("action_name", ICONIFIED_ACTIONS)
def test_action_has_a_non_null_icon(window, action_name):
    assert window._actions[action_name].icon().isNull() is False
