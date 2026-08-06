import pytest
from PySide6.QtWidgets import QApplication

from studio.workspace.board_piece_item import BoardPieceItem

LONG_ID = "caja_simple-lateral-izquierdo"


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


def test_short_label_on_a_wide_piece_is_shown_in_full(app):
    item = BoardPieceItem("p1", 0, 0, 2000, 500)

    assert item._label.text() == "p1"
    assert item._label.toolTip() == ""


def test_long_label_on_a_narrow_piece_is_elided_not_overflowing(app):
    # Regression: a long auto-generated id (container generator output) on a
    # narrow piece used to render past the piece's own rect, unclipped, into
    # neighboring pieces or empty board space — confirmed against a real
    # screenshot. The elided text's own rendered width must fit inside the
    # piece, and the full id must still be reachable via tooltip.
    item = BoardPieceItem(LONG_ID, 0, 0, 90, 60)

    assert item._label.text() != LONG_ID
    assert len(item._label.text()) < len(LONG_ID)
    assert item._label.toolTip() == LONG_ID

    available_width = item.rect().width() - 24 - 12
    assert item._label.boundingRect().width() <= available_width + 1  # AA slack


def test_rotating_a_piece_re_elides_the_label_for_the_new_width(app):
    # A piece long enough to show its id fully in one orientation but not
    # the other — rotation must re-run elision, not just resize the rect.
    item = BoardPieceItem(LONG_ID, 0, 0, 800, 60)
    assert item._label.text() == LONG_ID

    item.set_rotation(90)  # swaps to (0, 0, 60, 800): now the narrow side

    assert item._label.text() != LONG_ID
    assert item._label.toolTip() == LONG_ID

    item.set_rotation(0)  # back to the wide side

    assert item._label.text() == LONG_ID
    assert item._label.toolTip() == ""


def test_a_piece_too_narrow_for_any_text_shows_an_empty_label_not_overflow(app):
    item = BoardPieceItem(LONG_ID, 0, 0, 20, 20)

    assert item._label.boundingRect().width() <= item.rect().width()
