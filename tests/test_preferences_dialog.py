from PySide6.QtWidgets import QApplication

from studio.dialogs import PreferencesDialog


def _app():
    return QApplication.instance() or QApplication([])


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
