from PySide6.QtWidgets import QApplication

from studio.dialogs import BoardDialog, MoveToBoardDialog, PieceDialog


def _app():
    return QApplication.instance() or QApplication([])


def test_board_dialog_defaults_and_values():
    _app()
    dialog = BoardDialog(board_id="B1", length_mm=2000, width_mm=300)

    assert dialog.values() == ("B1", 2000.0, 300.0, "Demo")


def test_board_dialog_id_editable_flag_disables_the_field():
    _app()
    dialog = BoardDialog(board_id="B1", id_editable=False)

    assert dialog.id_edit.isEnabled() is False


def test_board_dialog_strips_whitespace_from_the_id():
    _app()
    dialog = BoardDialog()
    dialog.id_edit.setText("  B2  ")

    board_id, _, _, _ = dialog.values()

    assert board_id == "B2"


def test_board_dialog_accepts_a_custom_material():
    _app()
    dialog = BoardDialog(board_id="B1", material="Melamina")

    _, _, _, material = dialog.values()

    assert material == "Melamina"


def test_piece_dialog_defaults_and_values():
    _app()
    dialog = PieceDialog(piece_id="p1", length_mm=500, width_mm=200)

    assert dialog.values() == ("p1", 500.0, 200.0, "Demo")


def test_piece_dialog_id_editable_flag_disables_the_field():
    _app()
    dialog = PieceDialog(piece_id="p1", id_editable=False)

    assert dialog.id_edit.isEnabled() is False


def test_piece_dialog_accepts_a_custom_material():
    _app()
    dialog = PieceDialog(piece_id="p1", material="MDF")

    _, _, _, material = dialog.values()

    assert material == "MDF"


def test_board_dialog_rejects_a_duplicate_id_without_closing():
    _app()
    dialog = BoardDialog(existing_ids=frozenset({"B1"}))
    dialog.id_edit.setText("B1")

    dialog._try_accept()

    assert dialog.result() == 0
    assert dialog.error_label.isHidden() is False


def test_board_dialog_rejects_an_empty_id_without_closing():
    _app()
    dialog = BoardDialog()
    dialog.id_edit.setText("   ")

    dialog._try_accept()

    assert dialog.result() == 0
    assert dialog.error_label.isHidden() is False


def test_board_dialog_accepts_a_unique_id():
    _app()
    dialog = BoardDialog(existing_ids=frozenset({"B1"}))
    dialog.id_edit.setText("B2")

    dialog._try_accept()

    assert dialog.result() == int(dialog.DialogCode.Accepted)


def test_piece_dialog_rejects_a_duplicate_id_without_closing():
    _app()
    dialog = PieceDialog(existing_ids=frozenset({"p1"}))
    dialog.id_edit.setText("p1")

    dialog._try_accept()

    assert dialog.result() == 0
    assert dialog.error_label.isHidden() is False


def test_piece_dialog_accepts_a_unique_id():
    _app()
    dialog = PieceDialog(existing_ids=frozenset({"p1"}))
    dialog.id_edit.setText("p2")

    dialog._try_accept()

    assert dialog.result() == int(dialog.DialogCode.Accepted)


def test_move_to_board_dialog_lists_the_given_boards():
    _app()
    dialog = MoveToBoardDialog(board_ids=["A", "B"])

    assert [
        dialog.board_combo.itemText(i) for i in range(dialog.board_combo.count())
    ] == [
        "A",
        "B",
    ]


def test_move_to_board_dialog_returns_the_selected_board():
    _app()
    dialog = MoveToBoardDialog(board_ids=["A", "B"])
    dialog.board_combo.setCurrentText("B")

    assert dialog.selected_board_id() == "B"
