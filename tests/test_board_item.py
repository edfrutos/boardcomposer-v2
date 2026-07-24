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
