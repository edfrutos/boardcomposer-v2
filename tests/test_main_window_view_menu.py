import pytest
from PySide6.QtWidgets import QApplication, QDockWidget

from studio.main_window import MainWindow
from studio.services import StudioServices

BUILT_IN_DOCK_TITLES = {"Explorer", "Inspector", "Timeline", "Comparador", "Asistente"}


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _dock(window, title: str) -> QDockWidget:
    return next(d for d in window.findChildren(QDockWidget) if d.windowTitle() == title)


def test_every_built_in_dock_has_a_toggle_action_in_the_ver_menu(window):
    action_texts = {action.text() for action in window._menus["Ver"].actions()}

    assert BUILT_IN_DOCK_TITLES <= action_texts


def test_ver_menu_action_reopens_a_closed_built_in_dock(window):
    window.show()
    dock = _dock(window, "Inspector")
    dock.close()
    assert dock.isVisible() is False

    toggle = next(
        action
        for action in window._menus["Ver"].actions()
        if action.text() == "Inspector"
    )
    toggle.trigger()

    assert dock.isVisible() is True
