import pytest
from PySide6.QtWidgets import QApplication, QMessageBox

from studio.main_window import MainWindow
from studio.services import StudioServices
from studio.update_check import UpdateCheckResult


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_ayuda_menu_has_a_check_for_updates_action(window):
    action_texts = {action.text() for action in window._menus["Ayuda"].actions()}

    assert "Buscar actualizaciones…" in action_texts


def test_update_available_shows_an_information_dialog_with_the_link(
    window, monkeypatch
):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: UpdateCheckResult(
            checked_ok=True,
            update_available=True,
            current_version=current_version,
            latest_version="9.9.9",
            release_url="https://example.com/v9.9.9",
        ),
    )
    calls = []
    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args, **kwargs: calls.append((args, kwargs)) or None,
    )

    window._check_for_updates()

    assert len(calls) == 1
    message = calls[0][0][2]
    assert "9.9.9" in message
    assert "https://example.com/v9.9.9" in message


def test_already_latest_shows_an_information_dialog_without_offering_a_link(
    window, monkeypatch
):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: UpdateCheckResult(
            checked_ok=True,
            update_available=False,
            current_version=current_version,
        ),
    )
    calls = []
    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args, **kwargs: calls.append((args, kwargs)) or None,
    )

    window._check_for_updates()

    assert len(calls) == 1


def test_check_failure_shows_a_warning_not_an_information_dialog(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: UpdateCheckResult(
            checked_ok=False,
            update_available=False,
            current_version=current_version,
            error="sin conexión",
        ),
    )
    warnings = []
    infos = []
    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: warnings.append((args, kwargs)) or None,
    )
    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args, **kwargs: infos.append((args, kwargs)) or None,
    )

    window._check_for_updates()

    assert len(warnings) == 1
    assert infos == []
    assert "sin conexión" in warnings[0][0][2]
