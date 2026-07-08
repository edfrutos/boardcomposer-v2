from boardcomposer.domain import Board, BoardPlacement

from .free_space_manager import FreeSpaceManager
from .rectangle import Rectangle


def place_board_in_first_space(
    board: Board,
    manager: FreeSpaceManager,
    board_id: str,
) -> BoardPlacement | None:
    rectangle = Rectangle(0, 0, board.length_mm, board.width_mm)
    space = manager.find_space_for(rectangle)

    if space is None:
        return None

    placed_rectangle = Rectangle(
        x_mm=space.rectangle.x_mm,
        y_mm=space.rectangle.y_mm,
        length_mm=board.length_mm,
        width_mm=board.width_mm,
    )

    manager.place(placed_rectangle)

    return BoardPlacement(
        board_id=board_id,
        x_mm=placed_rectangle.x_mm,
        y_mm=placed_rectangle.y_mm,
        length_mm=placed_rectangle.length_mm,
        width_mm=placed_rectangle.width_mm,
    )
