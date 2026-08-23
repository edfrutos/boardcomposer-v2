from PySide6.QtGui import QFontMetricsF
from PySide6.QtWidgets import QApplication, QGraphicsSimpleTextItem

from studio.models import StudioBoard
from studio.workspace.board_item import create_board_item


def test_create_board_item_matches_the_boards_dimensions():
    QApplication.instance() or QApplication([])
    board_model = StudioBoard("TAB-001", 3000, 1000)

    item = create_board_item(board_model)

    assert item.rect().width() == 3000
    assert item.rect().height() == 1000


def test_create_board_item_labels_itself_with_the_board_id():
    QApplication.instance() or QApplication([])
    board_model = StudioBoard("TAB-001", 3000, 1000)

    item = create_board_item(board_model)

    labels = [
        child
        for child in item.childItems()
        if isinstance(child, QGraphicsSimpleTextItem)
    ]
    assert len(labels) == 1
    assert labels[0].text() == "TAB-001"


def test_create_board_item_label_sits_above_the_rect_not_inside_it():
    QApplication.instance() or QApplication([])
    board_model = StudioBoard("TAB-001", 3000, 1000)

    item = create_board_item(board_model)

    label = next(
        child
        for child in item.childItems()
        if isinstance(child, QGraphicsSimpleTextItem)
    )
    # Above the board's own origin (y < 0) — never overlapping a piece
    # placed near (0, 0), unlike a label drawn inside the rect would.
    assert label.pos().y() < 0


def test_create_board_item_shrinks_the_label_for_a_thin_board():
    QApplication.instance() or QApplication([])
    thin_board = StudioBoard("TAB01", 460, 40)
    wide_board = StudioBoard("TAB-001", 3000, 1000)

    thin_item = create_board_item(thin_board)
    wide_item = create_board_item(wide_board)
    thin_label = next(
        child
        for child in thin_item.childItems()
        if isinstance(child, QGraphicsSimpleTextItem)
    )
    wide_label = next(
        child
        for child in wide_item.childItems()
        if isinstance(child, QGraphicsSimpleTextItem)
    )

    # A 460x40mm baton (reported: the label dwarfed the board) gets a
    # visibly smaller font than a normal-sized board, not the same fixed
    # 48pt regardless of how thin the board is.
    assert thin_label.font().pointSize() < wide_label.font().pointSize()


def test_create_board_item_label_never_overlaps_the_rect_regardless_of_size():
    QApplication.instance() or QApplication([])

    for board_model in (
        StudioBoard("TAB01", 460, 40),
        StudioBoard("TAB-SQUARE", 100, 100),
        StudioBoard("TAB-001", 3000, 1000),
    ):
        item = create_board_item(board_model)
        label = next(
            child
            for child in item.childItems()
            if isinstance(child, QGraphicsSimpleTextItem)
        )
        label_bottom = label.pos().y() + QFontMetricsF(label.font()).height()
        # The bottom of the label's bounding box must sit at or above the
        # rect's own top edge (y=0) — the exact overlap the user reported
        # for a thin board, now guarded for any board size.
        assert label_bottom <= 0
