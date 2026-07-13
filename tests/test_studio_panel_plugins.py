import pytest
from PySide6.QtWidgets import QApplication, QDockWidget, QLabel, QWidget

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


def _dock_titles(window) -> list[str]:
    return [dock.windowTitle() for dock in window.findChildren(QDockWidget)]


def test_no_plugin_panels_leaves_the_window_unchanged(app, monkeypatch):
    monkeypatch.setattr("studio.main_window.discover_panel_plugins", lambda: ({}, []))

    window = MainWindow(services=StudioServices())

    assert "Explorer" in _dock_titles(window)


def test_a_plugin_panel_is_added_as_a_dock(app, monkeypatch):
    def _factory(services):
        return QLabel("hola desde el plugin")

    monkeypatch.setattr(
        "studio.main_window.discover_panel_plugins",
        lambda: ({"Métricas": _factory}, []),
    )

    window = MainWindow(services=StudioServices())

    assert "Métricas" in _dock_titles(window)


def test_a_plugin_panel_gets_a_toggle_action_in_the_ver_menu(app, monkeypatch):
    def _factory(services):
        return QLabel("hola")

    monkeypatch.setattr(
        "studio.main_window.discover_panel_plugins",
        lambda: ({"Métricas": _factory}, []),
    )

    window = MainWindow(services=StudioServices())

    action_texts = [action.text() for action in window._menus["Ver"].actions()]
    assert "Métricas" in action_texts


def test_a_plugin_panel_using_a_reserved_name_is_ignored(app, monkeypatch):
    def _factory(services):
        return QLabel("intento de duplicar Inspector")

    monkeypatch.setattr(
        "studio.main_window.discover_panel_plugins",
        lambda: ({"Inspector": _factory}, []),
    )

    window = MainWindow(services=StudioServices())

    assert _dock_titles(window).count("Inspector") == 1


def test_a_broken_panel_factory_does_not_crash_the_window(app, monkeypatch):
    def _broken_factory(services):
        raise RuntimeError("boom")

    monkeypatch.setattr(
        "studio.main_window.discover_panel_plugins",
        lambda: ({"Roto": _broken_factory}, []),
    )

    window = MainWindow(services=StudioServices())

    assert "Roto" not in _dock_titles(window)
    assert "Explorer" in _dock_titles(window)


def test_a_plugin_load_error_does_not_crash_the_window(app, monkeypatch):
    from boardcomposer.plugins import PluginLoadError

    monkeypatch.setattr(
        "studio.main_window.discover_panel_plugins",
        lambda: ({}, [PluginLoadError(name="roto", error="no se pudo importar")]),
    )

    window = MainWindow(services=StudioServices())

    assert "Explorer" in _dock_titles(window)


def test_plugin_panel_factory_receives_the_studio_services(app, monkeypatch):
    received = []

    def _factory(services):
        received.append(services)
        return QWidget()

    monkeypatch.setattr(
        "studio.main_window.discover_panel_plugins",
        lambda: ({"Custom": _factory}, []),
    )
    services = StudioServices()

    MainWindow(services=services)

    assert received == [services]
