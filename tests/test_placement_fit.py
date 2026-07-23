from studio.models import StudioBoard, StudioPiece, StudioPlacement
from studio.workspace.placement_fit import piece_fits_on_board


def test_fits_within_an_empty_board():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)

    assert piece_fits_on_board(board, piece, 0, 0, False, [], {}) is True


def test_does_not_fit_past_the_boards_length():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)

    assert piece_fits_on_board(board, piece, 800, 0, False, [], {}) is False


def test_does_not_fit_past_the_boards_width():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)

    assert piece_fits_on_board(board, piece, 0, 400, False, [], {}) is False


def test_negative_position_does_not_fit():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)

    assert piece_fits_on_board(board, piece, -10, 0, False, [], {}) is False


def test_rotation_swaps_length_and_width_for_the_bounds_check():
    board = StudioBoard("B1", 400, 350)
    piece = StudioPiece("p1", 300, 200)

    # At x=150: unrotated needs 300mm of length (150+300=450 > board's 400,
    # doesn't fit); rotated needs only 200mm (150+200=350 <= 400, fits).
    assert piece_fits_on_board(board, piece, 150, 0, False, [], {}) is False
    assert piece_fits_on_board(board, piece, 150, 0, True, [], {}) is True


def test_overlapping_an_existing_placement_does_not_fit():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    assert (
        piece_fits_on_board(
            board, piece, 100, 100, False, [other_placement], {"p2": other_piece}
        )
        is False
    )


def test_next_to_an_existing_placement_without_overlap_fits():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    assert (
        piece_fits_on_board(
            board, piece, 300, 0, False, [other_placement], {"p2": other_piece}
        )
        is True
    )


def test_ignores_a_placement_whose_piece_is_missing_from_the_lookup():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)
    other_placement = StudioPlacement("does-not-exist", 0, 0, board_id="B1")

    assert piece_fits_on_board(board, piece, 0, 0, False, [other_placement], {}) is True
