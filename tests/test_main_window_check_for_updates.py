import subprocess

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox, QProgressDialog

from studio.main_window import MainWindow
from studio.services import StudioServices
from studio.update_check import UpdateCheckResult
from studio.update_installer import DownloadError


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


def _update_result_with_dmg(**overrides):
    defaults = dict(
        checked_ok=True,
        update_available=True,
        current_version="9.8.7",
        latest_version="9.9.9",
        release_url="https://example.com/v9.9.9",
        dmg_url="https://example.com/releases/BoardComposerStudio-macos.dmg",
    )
    defaults.update(overrides)
    return UpdateCheckResult(**defaults)


def test_declining_the_prompt_never_calls_download(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: _update_result_with_dmg(),  # noqa: ARG005
    )
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.No
    )
    download_calls = []
    monkeypatch.setattr(
        "studio.main_window.download_dmg",
        lambda *a, **k: download_calls.append((a, k)),
    )

    window._check_for_updates()

    assert download_calls == []


def test_confirming_the_prompt_downloads_and_opens_the_dmg(
    window, monkeypatch, tmp_path
):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: _update_result_with_dmg(),  # noqa: ARG005
    )
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes
    )
    monkeypatch.setattr(QProgressDialog, "show", lambda self: None)
    monkeypatch.setattr(QProgressDialog, "close", lambda self: None)
    monkeypatch.setattr(QApplication, "processEvents", staticmethod(lambda: None))

    dmg_path = tmp_path / "BoardComposerStudio-macos.dmg"
    download_calls = []

    def _fake_download_dmg(
        url, dest_dir, *, progress_callback=None, should_cancel=None
    ):
        download_calls.append((url, dest_dir))
        if progress_callback is not None:
            progress_callback(100, 100)
        return dmg_path

    monkeypatch.setattr("studio.main_window.download_dmg", _fake_download_dmg)
    open_calls = []
    monkeypatch.setattr(
        "studio.main_window.open_in_finder", lambda path: open_calls.append(path)
    )

    window._check_for_updates()

    assert len(download_calls) == 1
    assert (
        download_calls[0][0]
        == "https://example.com/releases/BoardComposerStudio-macos.dmg"
    )
    assert open_calls == [dmg_path]


def test_download_failure_shows_a_warning_not_a_crash(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: _update_result_with_dmg(),  # noqa: ARG005
    )
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes
    )
    monkeypatch.setattr(QProgressDialog, "show", lambda self: None)
    monkeypatch.setattr(QProgressDialog, "close", lambda self: None)

    def _raise(*a, **k):
        raise DownloadError("no se pudo descargar")

    monkeypatch.setattr("studio.main_window.download_dmg", _raise)
    warnings = []
    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: warnings.append((args, kwargs)) or None,
    )

    window._check_for_updates()

    assert len(warnings) == 1
    assert "no se pudo descargar" in warnings[0][0][2]


def test_open_failure_after_a_successful_download_shows_a_warning(
    window, monkeypatch, tmp_path
):
    monkeypatch.setattr(
        "studio.main_window.check_for_update",
        lambda current_version: _update_result_with_dmg(),  # noqa: ARG005
    )
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes
    )
    monkeypatch.setattr(QProgressDialog, "show", lambda self: None)
    monkeypatch.setattr(QProgressDialog, "close", lambda self: None)

    dmg_path = tmp_path / "BoardComposerStudio-macos.dmg"
    monkeypatch.setattr("studio.main_window.download_dmg", lambda *a, **k: dmg_path)

    def _raise(path):  # noqa: ARG001
        raise subprocess.CalledProcessError(1, ["open"])

    monkeypatch.setattr("studio.main_window.open_in_finder", _raise)
    warnings = []
    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: warnings.append((args, kwargs)) or None,
    )

    window._check_for_updates()

    assert len(warnings) == 1
    assert str(dmg_path) in warnings[0][0][2]


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
