"""Studio modal dialogs (IDE-0013 Fase D)."""

from studio.dialogs.board_csv_import_preview_dialog import BoardCsvImportPreviewDialog
from studio.dialogs.board_dialog import BoardDialog
from studio.dialogs.container_generator_dialog import ContainerGeneratorDialog
from studio.dialogs.csv_import_preview_dialog import CsvImportPreviewDialog
from studio.dialogs.kerf_dialog import KerfDialog
from studio.dialogs.materials_dialogs import (
    MaterialDialog,
    MaterialsLibraryDialog,
    MatchingScrapsDialog,
)
from studio.dialogs.move_to_board_dialog import MoveToBoardDialog
from studio.dialogs.piece_dialog import PieceDialog
from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.dialogs.scrap_dialogs import AddScrapDialog, UseScrapDialog

__all__ = [
    "AddScrapDialog",
    "BoardCsvImportPreviewDialog",
    "BoardDialog",
    "ContainerGeneratorDialog",
    "CsvImportPreviewDialog",
    "KerfDialog",
    "MaterialDialog",
    "MaterialsLibraryDialog",
    "MatchingScrapsDialog",
    "MoveToBoardDialog",
    "PieceDialog",
    "PreferencesDialog",
    "UseScrapDialog",
]
