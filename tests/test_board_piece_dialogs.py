from PySide6.QtWidgets import QApplication

from studio.dialogs import BoardDialog, PieceDialog


def _app():
    return QApplication.instance() or QApplication([])


def test_board_dialog_defaults_and_values():
    _app()
    dialog = BoardDialog(board_id="B1", length_mm=2000, width_mm=300)

    assert dialog.values() == ("B1", 2000.0, 300.0)


def test_board_dialog_id_editable_flag_disables_the_field():
    _app()
    dialog = BoardDialog(board_id="B1", id_editable=False)

    assert dialog.id_edit.isEnabled() is False


def test_board_dialog_strips_whitespace_from_the_id():
    _app()
    dialog = BoardDialog()
    dialog.id_edit.setText("  B2  ")

    board_id, _, _ = dialog.values()

    assert board_id == "B2"


def test_piece_dialog_defaults_and_values():
    _app()
    dialog = PieceDialog(piece_id="p1", length_mm=500, width_mm=200)

    assert dialog.values() == ("p1", 500.0, 200.0)


def test_piece_dialog_id_editable_flag_disables_the_field():
    _app()
    dialog = PieceDialog(piece_id="p1", id_editable=False)

    assert dialog.id_edit.isEnabled() is False
