from PySide6.QtWidgets import QApplication, QHeaderView

from studio.dialogs import BoardCsvImportPreviewDialog
from studio.models import StudioBoard


def _app():
    return QApplication.instance() or QApplication([])


def test_dialog_populates_one_row_per_board():
    _app()
    boards = [
        StudioBoard("TAB-A01", 860, 490, thickness_mm=19),
        StudioBoard("TAB-A02", 460, 310, material="Melamina", thickness_mm=16),
    ]

    dialog = BoardCsvImportPreviewDialog(boards=boards)
    table = dialog.layout().itemAt(0).widget()

    assert table.rowCount() == 2


def test_dialog_table_shows_board_values():
    _app()
    boards = [StudioBoard("TAB-A01", 860, 490, material="Roble", thickness_mm=19)]

    dialog = BoardCsvImportPreviewDialog(boards=boards)
    table = dialog.layout().itemAt(0).widget()

    assert table.item(0, 0).text() == "TAB-A01"
    assert table.item(0, 1).text() == "860"
    assert table.item(0, 2).text() == "490"
    assert table.item(0, 3).text() == "Roble"
    assert table.item(0, 4).text() == "19"


def test_dialog_title_includes_the_board_count():
    _app()
    boards = [StudioBoard("TAB-A01", 860, 490), StudioBoard("TAB-A02", 460, 310)]

    dialog = BoardCsvImportPreviewDialog(boards=boards)

    assert "2" in dialog.windowTitle()


def test_id_and_material_columns_size_to_their_content_not_an_even_split():
    # Regression: an equal Stretch on every column squeezed a long board id
    # down to whatever an even split of the dialog's width happened to
    # leave it — same bug class as the pieces preview dialog and the move-
    # to-board combo box.
    _app()
    boards = [StudioBoard("TAB-A01", 860, 490, material="Roble", thickness_mm=19)]

    dialog = BoardCsvImportPreviewDialog(boards=boards)
    table = dialog.layout().itemAt(0).widget()
    header = table.horizontalHeader()

    assert header.sectionResizeMode(0) == QHeaderView.ResizeMode.ResizeToContents
    assert header.sectionResizeMode(3) == QHeaderView.ResizeMode.ResizeToContents
    assert header.sectionResizeMode(1) == QHeaderView.ResizeMode.Stretch
