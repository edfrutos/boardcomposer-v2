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
