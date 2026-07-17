import pytest
from PySide6.QtCore import QPointF, QRectF
from PySide6.QtWidgets import QApplication, QGraphicsScene

from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.placement_validator import PlacementValidator

BOARD_RECT = QRectF(0, 0, 3000, 1000)


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


def _put_on_scene(*items):
    scene = QGraphicsScene()
    for item in items:
        scene.addItem(item)
    return scene


def test_snaps_to_the_right_of_a_neighbor(app):
    validator = PlacementValidator(BOARD_RECT)
    neighbor = BoardPieceItem("p1", 0, 0, 500, 300)
    dragged = BoardPieceItem("p2", 0, 0, 400, 300)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    result = validator.constrain_position(dragged, QPointF(510, 10), gap_mm=5.0)

    assert result.x() == 505.0
    assert result.y() == 10.0


def test_snaps_to_the_left_of_a_neighbor(app):
    validator = PlacementValidator(BOARD_RECT)
    neighbor = BoardPieceItem("p1", 1000, 0, 500, 300)
    dragged = BoardPieceItem("p2", 0, 0, 400, 300)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    result = validator.constrain_position(dragged, QPointF(595, 10), gap_mm=5.0)

    assert result.x() == 595.0  # 1000 (neighbor left) - 400 (width) - 5 (gap)
    assert result.y() == 10.0


def test_snaps_below_a_neighbor(app):
    validator = PlacementValidator(BOARD_RECT)
    neighbor = BoardPieceItem("p1", 0, 0, 500, 300)
    dragged = BoardPieceItem("p2", 0, 0, 500, 200)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    result = validator.constrain_position(dragged, QPointF(10, 310), gap_mm=5.0)

    assert result.x() == 10.0
    assert result.y() == 305.0  # 300 (neighbor bottom) + 5 (gap)


def test_snaps_above_a_neighbor(app):
    validator = PlacementValidator(BOARD_RECT)
    neighbor = BoardPieceItem("p1", 0, 300, 500, 300)
    dragged = BoardPieceItem("p2", 0, 0, 500, 200)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    result = validator.constrain_position(dragged, QPointF(10, 95), gap_mm=5.0)

    assert result.x() == 10.0
    assert result.y() == 95.0  # 300 (neighbor top) - 200 (height) - 5 (gap)


def test_does_not_snap_beyond_the_threshold(app):
    validator = PlacementValidator(BOARD_RECT)
    neighbor = BoardPieceItem("p1", 0, 0, 500, 300)
    dragged = BoardPieceItem("p2", 0, 0, 400, 300)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    far_pos = QPointF(600, 10)  # 100mm past the neighbor's right edge
    result = validator.constrain_position(dragged, far_pos, gap_mm=5.0)

    assert result.x() == 600.0
    assert result.y() == 10.0


def test_does_not_snap_without_a_shared_span(app):
    validator = PlacementValidator(BOARD_RECT)
    # Neighbor sits far below on the y-axis, so there is no vertical overlap
    # with the dragged piece even though it's horizontally close.
    neighbor = BoardPieceItem("p1", 0, 900, 500, 100)
    dragged = BoardPieceItem("p2", 0, 0, 400, 300)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    result = validator.constrain_position(dragged, QPointF(510, 0), gap_mm=5.0)

    assert result.x() == 510.0


def test_snaps_to_the_closest_of_several_neighbors(app):
    validator = PlacementValidator(BOARD_RECT)
    far_neighbor = BoardPieceItem("p1", 0, 0, 300, 300)
    near_neighbor = BoardPieceItem("p2", 500, 0, 200, 300)
    dragged = BoardPieceItem("p3", 0, 0, 100, 300)
    scene = _put_on_scene(far_neighbor, near_neighbor, dragged)  # noqa: F841

    # Sits between both neighbors, closer to near_neighbor's left edge (500).
    result = validator.constrain_position(dragged, QPointF(410, 0), gap_mm=0.0)

    assert result.x() == 400.0  # 500 (near_neighbor left) - 100 (width) - 0 (gap)


def test_zero_gap_snaps_pieces_flush(app):
    validator = PlacementValidator(BOARD_RECT)
    neighbor = BoardPieceItem("p1", 0, 0, 500, 300)
    dragged = BoardPieceItem("p2", 0, 0, 400, 300)
    scene = _put_on_scene(neighbor, dragged)  # noqa: F841 (keeps items alive)

    result = validator.constrain_position(dragged, QPointF(505, 10), gap_mm=0.0)

    assert result.x() == 500.0
