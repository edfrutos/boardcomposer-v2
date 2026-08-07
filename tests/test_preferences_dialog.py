from PySide6.QtWidgets import QApplication, QLineEdit

from studio.dialogs import PreferencesDialog


def _app():
    return QApplication.instance() or QApplication([])


def test_preferences_dialog_defaults_to_an_empty_api_key():
    _app()
    dialog = PreferencesDialog()

    assert dialog.anthropic_api_key() == ""


def test_preferences_dialog_shows_the_given_api_key():
    _app()
    dialog = PreferencesDialog(anthropic_api_key="sk-ant-abc123")

    assert dialog.anthropic_api_key() == "sk-ant-abc123"


def test_preferences_dialog_masks_the_api_key_field():
    # A secret pasted into a plain preferences dialog shouldn't be readable
    # over someone's shoulder.
    _app()
    dialog = PreferencesDialog()

    assert dialog.anthropic_api_key_edit.echoMode() == QLineEdit.EchoMode.Password


def test_preferences_dialog_strips_whitespace_from_the_api_key():
    _app()
    dialog = PreferencesDialog()
    dialog.anthropic_api_key_edit.setText("  sk-ant-abc123  ")

    assert dialog.anthropic_api_key() == "sk-ant-abc123"


def test_preferences_dialog_defaults_to_the_given_theme():
    _app()
    dialog = PreferencesDialog(theme_key="dark")

    assert dialog.theme_key() == "dark"


def test_preferences_dialog_defaults_to_automatico_when_unset():
    _app()
    dialog = PreferencesDialog()

    assert dialog.theme_key() == "auto"


def test_preferences_dialog_theme_key_follows_the_combo_selection():
    _app()
    dialog = PreferencesDialog(theme_key="auto")

    dialog.theme_combo.setCurrentIndex(dialog.theme_combo.findData("light"))

    assert dialog.theme_key() == "light"


def test_preferences_dialog_defaults_to_anthropic_as_the_active_provider():
    _app()
    dialog = PreferencesDialog()

    assert dialog.ai_provider() == "anthropic"


def test_preferences_dialog_shows_the_given_active_provider():
    _app()
    dialog = PreferencesDialog(ai_provider="openai")

    assert dialog.ai_provider() == "openai"


def test_preferences_dialog_shows_and_strips_each_provider_field():
    _app()
    dialog = PreferencesDialog(
        openai_api_key="  sk-openai-abc  ",
        gemini_api_key="  AIza-gemini-abc  ",
        ollama_host="  http://localhost:11434  ",
        ollama_model="  llama3.1  ",
    )

    assert dialog.openai_api_key() == "sk-openai-abc"
    assert dialog.gemini_api_key() == "AIza-gemini-abc"
    assert dialog.ollama_host() == "http://localhost:11434"
    assert dialog.ollama_model() == "llama3.1"


def test_preferences_dialog_masks_the_openai_and_gemini_key_fields():
    _app()
    dialog = PreferencesDialog()

    assert dialog.openai_api_key_edit.echoMode() == QLineEdit.EchoMode.Password
    assert dialog.gemini_api_key_edit.echoMode() == QLineEdit.EchoMode.Password


def test_preferences_dialog_only_shows_the_active_providers_fields():
    _app()
    dialog = PreferencesDialog(ai_provider="anthropic")

    assert dialog.form.isRowVisible(dialog.anthropic_api_key_edit)
    assert not dialog.form.isRowVisible(dialog.openai_api_key_edit)
    assert not dialog.form.isRowVisible(dialog.gemini_api_key_edit)
    assert not dialog.form.isRowVisible(dialog.ollama_host_edit)
    assert not dialog.form.isRowVisible(dialog.ollama_model_edit)


def test_preferences_dialog_switches_visible_fields_with_the_provider_combo():
    _app()
    dialog = PreferencesDialog(ai_provider="anthropic")

    dialog.ai_provider_combo.setCurrentIndex(
        dialog.ai_provider_combo.findData("ollama")
    )

    assert not dialog.form.isRowVisible(dialog.anthropic_api_key_edit)
    assert dialog.form.isRowVisible(dialog.ollama_host_edit)
    assert dialog.form.isRowVisible(dialog.ollama_model_edit)
