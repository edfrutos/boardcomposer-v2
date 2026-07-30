from studio.models import StudioBoard, StudioPiece, StudioPlacement
from studio.panels.board_metrics import board_utilization


def test_board_utilization_of_an_empty_board_is_zero():
    board = StudioBoard("A", 1000, 500)

    assert board_utilization(board, [], {}) == 0.0


def test_board_utilization_computes_the_placed_area_fraction():
    board = StudioBoard("A", 1000, 500)  # 500,000 mm²
    piece = StudioPiece("p1", 200, 250)  # 50,000 mm² — 10%
    placement = StudioPlacement("p1", 0, 0, board_id="A")

    assert board_utilization(board, [placement], {"p1": piece}) == 0.1


def test_board_utilization_ignores_a_placement_whose_piece_is_missing():
    board = StudioBoard("A", 1000, 500)
    placement = StudioPlacement("does-not-exist", 0, 0, board_id="A")

    assert board_utilization(board, [placement], {}) == 0.0
