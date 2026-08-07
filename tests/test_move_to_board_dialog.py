import pytest
from PySide6.QtWidgets import QApplication, QComboBox

from studio.dialogs import MoveToBoardDialog


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


def test_combo_adjusts_to_its_widest_item_instead_of_a_fixed_width(app):
    # Regression: real board ids sharing a long prefix (TAB-A01, TAB-A02,
    # ...) all rendered as an indistinguishable "TAB-A0" — the combo's
    # default sizing goes off its own narrow starting width, not its widest
    # entry, and the dropdown popup inherits that same width.
    board_ids = ["TAB-A01", "TAB-A02", "TAB-A11", "TAB-A12"]
    dialog = MoveToBoardDialog(board_ids=board_ids)

    assert (
        dialog.board_combo.sizeAdjustPolicy()
        == QComboBox.SizeAdjustPolicy.AdjustToContents
    )

    metrics = dialog.board_combo.fontMetrics()
    widest_item_text_width = max(
        metrics.horizontalAdvance(board_id) for board_id in board_ids
    )
    # The combo box needs room for the arrow/frame beyond the text itself —
    # this only guards against it collapsing back to a width narrower than
    # the text needs, not an exact layout measurement.
    assert dialog.board_combo.sizeHint().width() > widest_item_text_width


def test_dialog_has_a_reasonable_minimum_width(app):
    dialog = MoveToBoardDialog(board_ids=["TAB-001"])

    assert dialog.minimumWidth() >= 320
