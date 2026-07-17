import pytest
from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


EXPECTED_SHORTCUTS = {
    "add_board": "Ctrl+Alt+B",
    "edit_board": "Ctrl+Alt+Shift+B",
    "add_piece": "Ctrl+Alt+P",
    "edit_piece": "Ctrl+Alt+Shift+P",
    "solve_layout": "Ctrl+Alt+L",
    "apply_layout": "Ctrl+Alt+Shift+L",
    "compare_solutions": "Ctrl+Alt+C",
}


@pytest.mark.parametrize("action_name,shortcut", EXPECTED_SHORTCUTS.items())
def test_action_has_expected_shortcut(window, action_name, shortcut):
    assert window._actions[action_name].shortcut().toString() == shortcut


def test_shortcuts_are_all_unique(window):
    shortcuts = [
        window._actions[name].shortcut().toString() for name in EXPECTED_SHORTCUTS
    ]

    assert len(shortcuts) == len(set(shortcuts))
