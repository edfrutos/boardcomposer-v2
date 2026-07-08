from boardcomposer.solver.maxrects.heuristics import (
    best_area_fit,
    best_bottom_left_fit,
    best_long_side_fit,
    best_short_side_fit,
)

MAXRECTS_HEURISTICS = (
    ("best_area_fit", best_area_fit),
    ("best_short_side_fit", best_short_side_fit),
    ("best_long_side_fit", best_long_side_fit),
    ("best_bottom_left_fit", best_bottom_left_fit),
)
