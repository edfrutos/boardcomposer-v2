import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QDialog

from boardcomposer.ai import AnthropicProvider, MockAIProvider
from studio.main_window import ANTHROPIC_API_KEY_SETTINGS_KEY, MainWindow
from studio.services import StudioServices


@pytest.fixture
def window(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_no_key_stored_uses_the_mock_provider(window):
    assert isinstance(window.services.assistant.provider, MockAIProvider)


def test_setting_a_key_persists_it_and_switches_the_provider(window):
    window._set_anthropic_api_key("sk-ant-abc123")

    assert QSettings().value(ANTHROPIC_API_KEY_SETTINGS_KEY) == "sk-ant-abc123"
    assert isinstance(window.services.assistant.provider, AnthropicProvider)


def test_open_preferences_saves_the_api_key(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.exec",
        lambda self: QDialog.DialogCode.Accepted,
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.theme_key", lambda self: "auto"
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.anthropic_api_key",
        lambda self: "sk-ant-from-dialog",
    )

    window._open_preferences()

    assert isinstance(window.services.assistant.provider, AnthropicProvider)
    assert QSettings().value(ANTHROPIC_API_KEY_SETTINGS_KEY) == "sk-ant-from-dialog"


def test_open_preferences_cancelled_leaves_the_provider_unchanged(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.exec",
        lambda self: QDialog.DialogCode.Rejected,
    )

    window._open_preferences()

    assert isinstance(window.services.assistant.provider, MockAIProvider)
