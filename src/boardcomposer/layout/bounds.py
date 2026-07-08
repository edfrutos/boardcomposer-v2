from boardcomposer.domain import BoardPlacement
from boardcomposer.layout import Rectangle


def bounding_rectangle(placements: list[BoardPlacement]) -> Rectangle:
    if not placements:
        return Rectangle(0, 0, 0, 0)

    min_x = min(p.x_mm for p in placements)
    min_y = min(p.y_mm for p in placements)
    max_x = max(p.right_mm for p in placements)
    max_y = max(p.top_mm for p in placements)

    return Rectangle(
        x_mm=min_x,
        y_mm=min_y,
        length_mm=max_x - min_x,
        width_mm=max_y - min_y,
    )
