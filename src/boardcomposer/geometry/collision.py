from boardcomposer.domain import BoardPlacement
from boardcomposer.geometry import Rectangle


def placement_to_rectangle(placement: BoardPlacement) -> Rectangle:
    return Rectangle(
        x_mm=placement.x_mm,
        y_mm=placement.y_mm,
        length_mm=placement.length_mm,
        width_mm=placement.width_mm,
    )


def placements_overlap(a: BoardPlacement, b: BoardPlacement) -> bool:
    return placement_to_rectangle(a).overlaps(placement_to_rectangle(b))
