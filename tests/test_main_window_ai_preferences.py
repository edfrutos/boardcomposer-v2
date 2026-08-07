import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QDialog

from boardcomposer.ai import (
    AnthropicProvider,
    MockAIProvider,
    OllamaProvider,
    OpenAIProvider,
)
from studio.main_window import (
    AI_PROVIDER_SETTINGS_KEY,
    ANTHROPIC_API_KEY_SETTINGS_KEY,
    OLLAMA_HOST_SETTINGS_KEY,
    OLLAMA_MODEL_SETTINGS_KEY,
    OPENAI_API_KEY_SETTINGS_KEY,
    MainWindow,
)
from studio.services import StudioServices


@pytest.fixture
def window(monkeypatch):
    # _set_ai_preferences() (production code, exercised below) writes
    # straight to os.environ rather than going through monkeypatch, so a
    # previous test in this file leaves its env vars set for the rest of
    # the pytest session — scrub all of them up front, not just the one
    # each individual test cares about.
    for env_var in (
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "OLLAMA_HOST",
        "OLLAMA_MODEL",
        "BOARDCOMPOSER_AI_PROVIDER",
    ):
        monkeypatch.delenv(env_var, raising=False)
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _set_ai_preferences(window, **overrides):
    kwargs = dict(
        provider="anthropic",
        anthropic_api_key="",
        openai_api_key="",
        gemini_api_key="",
        ollama_host="",
        ollama_model="",
    )
    kwargs.update(overrides)
    window._set_ai_preferences(**kwargs)


def test_no_settings_stored_uses_the_mock_provider(window):
    assert isinstance(window.services.assistant.provider, MockAIProvider)


def test_setting_an_anthropic_key_persists_it_and_switches_the_provider(window):
    _set_ai_preferences(window, anthropic_api_key="sk-ant-abc123")

    assert QSettings().value(ANTHROPIC_API_KEY_SETTINGS_KEY) == "sk-ant-abc123"
    assert QSettings().value(AI_PROVIDER_SETTINGS_KEY) == "anthropic"
    assert isinstance(window.services.assistant.provider, AnthropicProvider)


def test_choosing_openai_persists_it_and_switches_the_provider(window, monkeypatch):
    monkeypatch.setattr("boardcomposer.ai.openai_provider.OpenAI", lambda: object())

    _set_ai_preferences(window, provider="openai", openai_api_key="sk-openai-abc")

    assert QSettings().value(AI_PROVIDER_SETTINGS_KEY) == "openai"
    assert QSettings().value(OPENAI_API_KEY_SETTINGS_KEY) == "sk-openai-abc"
    assert isinstance(window.services.assistant.provider, OpenAIProvider)


def test_choosing_ollama_persists_host_and_model_and_switches_the_provider(
    window, monkeypatch
):
    monkeypatch.setattr(
        "boardcomposer.ai.ollama_provider.OpenAI", lambda **kwargs: object()
    )

    _set_ai_preferences(
        window,
        provider="ollama",
        ollama_host="http://localhost:11434",
        ollama_model="llama3.1",
    )

    assert QSettings().value(OLLAMA_HOST_SETTINGS_KEY) == "http://localhost:11434"
    assert QSettings().value(OLLAMA_MODEL_SETTINGS_KEY) == "llama3.1"
    assert isinstance(window.services.assistant.provider, OllamaProvider)


def test_choosing_a_provider_without_its_key_falls_back_to_mock_without_crashing(
    window,
):
    # IDE-0036 safety net (AssistantService._resolve_provider): OpenAI's
    # client raises immediately when OPENAI_API_KEY is missing — picking
    # "OpenAI" in Preferences without a key must not crash Studio, it
    # should surface as a Mock response instead.
    _set_ai_preferences(window, provider="openai", openai_api_key="")

    assert isinstance(window.services.assistant.provider, MockAIProvider)


def test_open_preferences_saves_all_ai_fields(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.exec",
        lambda self: QDialog.DialogCode.Accepted,
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.theme_key", lambda self: "auto"
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.ai_provider", lambda self: "anthropic"
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.anthropic_api_key",
        lambda self: "sk-ant-from-dialog",
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.openai_api_key", lambda self: ""
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.gemini_api_key", lambda self: ""
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.ollama_host", lambda self: ""
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.ollama_model", lambda self: ""
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
