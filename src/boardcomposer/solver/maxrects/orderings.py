from boardcomposer.solver.board_ordering import (
    largest_area_first,
    longest_edge_first,
    original_order,
)

MAXRECTS_BOARD_ORDERINGS = (
    ("original", original_order),
    ("largest_area", largest_area_first),
    ("longest_edge", longest_edge_first),
)
