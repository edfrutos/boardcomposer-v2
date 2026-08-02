from PySide6.QtWidgets import QApplication

from studio.dialogs import CsvImportPreviewDialog
from studio.models import StudioPiece


def _app():
    return QApplication.instance() or QApplication([])


def test_dialog_populates_one_row_per_piece():
    _app()
    pieces = [
        StudioPiece("P-101", 700, 300, thickness_mm=19),
        StudioPiece("P-102", 520, 360, material="Melamina", thickness_mm=16),
    ]

    dialog = CsvImportPreviewDialog(pieces=pieces)
    table = dialog.layout().itemAt(0).widget()

    assert table.rowCount() == 2


def test_dialog_table_shows_piece_values():
    _app()
    pieces = [StudioPiece("P-101", 700, 300, material="Roble", thickness_mm=19)]

    dialog = CsvImportPreviewDialog(pieces=pieces)
    table = dialog.layout().itemAt(0).widget()

    assert table.rowCount() == 1
    assert table.item(0, 0).text() == "P-101"
    assert table.item(0, 1).text() == "700"
    assert table.item(0, 2).text() == "300"
    assert table.item(0, 3).text() == "Roble"
    assert table.item(0, 4).text() == "19"


def test_dialog_title_includes_the_piece_count():
    _app()
    pieces = [StudioPiece("P-101", 700, 300), StudioPiece("P-102", 520, 360)]

    dialog = CsvImportPreviewDialog(pieces=pieces)

    assert "2" in dialog.windowTitle()


def test_dialog_with_no_pieces_shows_an_empty_table():
    _app()

    dialog = CsvImportPreviewDialog(pieces=[])
    table = dialog.layout().itemAt(0).widget()

    assert table.rowCount() == 0
