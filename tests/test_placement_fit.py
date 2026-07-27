from studio.models import StudioBoard, StudioPiece, StudioPlacement
from studio.workspace.placement_fit import find_free_position, piece_fits_on_board


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


def test_find_free_position_on_an_empty_board_returns_the_origin():
    board = StudioBoard("B1", 1000, 500)

    assert find_free_position(board, 300, 200, [], {}) == (0, 0)


def test_find_free_position_returns_none_when_the_piece_is_too_big():
    board = StudioBoard("B1", 200, 200)

    assert find_free_position(board, 300, 200, [], {}) is None


def test_find_free_position_skips_past_an_occupying_placement():
    board = StudioBoard("B1", 1000, 500)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    position = find_free_position(
        board, 300, 200, [other_placement], {"p2": other_piece}
    )

    assert position is not None
    assert piece_fits_on_board(
        board,
        StudioPiece("p1", 300, 200),
        *position,
        False,
        [other_placement],
        {"p2": other_piece},
    )
    assert position != (0, 0)


def test_find_free_position_accounts_for_an_occupying_pieces_own_rotation():
    # p2 (300x200) sits rotated — 200 wide, 300 tall — so the free column
    # starts at x=200, not x=300.
    board = StudioBoard("B1", 1000, 500)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1", rotated=True)

    position = find_free_position(
        board, 100, 100, [other_placement], {"p2": other_piece}
    )

    assert position == (200, 0)


def test_find_free_position_returns_none_on_a_completely_full_board():
    board = StudioBoard("B1", 300, 200)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    assert (
        find_free_position(board, 50, 50, [other_placement], {"p2": other_piece})
        is None
    )


def test_a_piece_flush_against_a_neighbour_does_not_fit_once_a_kerf_is_set():
    # p2 ends at x=300. Butting p1 right up against it leaves no room for the
    # blade, so neither piece could actually come off the board.
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    assert (
        piece_fits_on_board(
            board,
            piece,
            300,
            0,
            False,
            [other_placement],
            {"p2": other_piece},
            kerf_mm=3,
        )
        is False
    )


def test_exactly_one_kerf_of_clearance_is_enough():
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 300, 200)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    assert (
        piece_fits_on_board(
            board,
            piece,
            303,
            0,
            False,
            [other_placement],
            {"p2": other_piece},
            kerf_mm=3,
        )
        is True
    )


def test_the_boards_own_edge_needs_no_kerf():
    # A piece as long as the board still fits: the board's edge is not a cut
    # between two pieces. Only neighbours demand clearance.
    board = StudioBoard("B1", 1000, 500)
    piece = StudioPiece("p1", 1000, 500)

    assert piece_fits_on_board(board, piece, 0, 0, False, [], {}, kerf_mm=3) is True


def test_find_free_position_leaves_room_for_the_cut():
    board = StudioBoard("B1", 1000, 500)
    other_piece = StudioPiece("p2", 300, 200)
    other_placement = StudioPlacement("p2", 0, 0, board_id="B1")

    position = find_free_position(
        board, 100, 100, [other_placement], {"p2": other_piece}, kerf_mm=3
    )

    # Without a kerf this would be (300, 0) — flush against p2's right edge.
    assert position == (303, 0)
