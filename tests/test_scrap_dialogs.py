from PySide6.QtWidgets import QApplication

from studio.dialogs import AddScrapDialog, UseScrapDialog
from studio.project.scrap_inventory import ScrapRecord


def _app():
    return QApplication.instance() or QApplication([])


def test_add_scrap_dialog_defaults_and_values():
    _app()
    dialog = AddScrapDialog()
    dialog.id_edit.setText("R-001")
    dialog.length_spin.setValue(800)
    dialog.width_spin.setValue(400)

    assert dialog.values() == ("R-001", 800.0, 400.0, 19.0, "", "")


def test_add_scrap_dialog_strips_whitespace_from_the_id():
    _app()
    dialog = AddScrapDialog()
    dialog.id_edit.setText("  R-002  ")

    scrap_id, *_ = dialog.values()

    assert scrap_id == "R-002"


def test_add_scrap_dialog_rejects_an_id_already_in_the_inventory():
    _app()
    dialog = AddScrapDialog(existing_ids=frozenset({"R-001"}))
    dialog.id_edit.setText("R-001")

    dialog._try_accept()

    assert dialog.result() == 0
    assert "Ya existe" in dialog.error_label.text()


def test_use_scrap_dialog_selects_the_first_row_by_default():
    _app()
    scraps = [
        ScrapRecord("R-001", 800, 400, 19, "Roble", "Mueble X", "2026-08-09"),
        ScrapRecord("R-002", 500, 300, 19, "Pino", "", "2026-08-09"),
    ]
    dialog = UseScrapDialog(scraps=scraps)

    assert dialog.selected_scrap().scrap_id == "R-001"


def test_use_scrap_dialog_returns_the_selected_row():
    _app()
    scraps = [
        ScrapRecord("R-001", 800, 400, 19, "Roble", "Mueble X", "2026-08-09"),
        ScrapRecord("R-002", 500, 300, 19, "Pino", "", "2026-08-09"),
    ]
    dialog = UseScrapDialog(scraps=scraps)
    dialog.table.selectRow(1)

    assert dialog.selected_scrap().scrap_id == "R-002"


def test_use_scrap_dialog_with_no_scraps_rejects_accept():
    _app()
    dialog = UseScrapDialog(scraps=[])

    dialog._try_accept()

    assert dialog.result() == 0
    assert "Selecciona" in dialog.error_label.text()


def test_use_scrap_dialog_defaults_to_no_new_board_requested():
    _app()
    scraps = [ScrapRecord("R-001", 800, 400, 19, "Roble", "Mueble X", "2026-08-09")]
    dialog = UseScrapDialog(scraps=scraps)

    assert dialog.new_board_requested is False


def test_use_scrap_dialog_new_board_button_rejects_and_sets_the_flag():
    _app()
    scraps = [ScrapRecord("R-001", 800, 400, 19, "Roble", "Mueble X", "2026-08-09")]
    dialog = UseScrapDialog(scraps=scraps)

    dialog._request_new_board()

    assert dialog.new_board_requested is True
    assert dialog.result() == 0
