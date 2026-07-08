from studio.workspace.board_piece_item import BoardPieceItem


def create_piece_item(piece, placement) -> BoardPieceItem:
    item = BoardPieceItem(
        piece.piece_id,
        placement.x_mm,
        placement.y_mm,
        piece.length_mm,
        piece.width_mm,
    )
    item.set_rotation(placement.rotation)
    return item
