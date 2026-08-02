"""Studio modal dialogs (IDE-0013 Fase D)."""

from studio.dialogs.board_dialog import BoardDialog
from studio.dialogs.csv_import_preview_dialog import CsvImportPreviewDialog
from studio.dialogs.kerf_dialog import KerfDialog
from studio.dialogs.move_to_board_dialog import MoveToBoardDialog
from studio.dialogs.piece_dialog import PieceDialog
from studio.dialogs.preferences_dialog import PreferencesDialog

__all__ = [
    "BoardDialog",
    "CsvImportPreviewDialog",
    "KerfDialog",
    "MoveToBoardDialog",
    "PieceDialog",
    "PreferencesDialog",
]
