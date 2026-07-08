from boardcomposer.domain import BoardPlacement
from boardcomposer.geometry.collision import placements_overlap


def has_overlaps(placements: list[BoardPlacement]) -> bool:
    for i, current in enumerate(placements):
        for other in placements[i + 1 :]:
            if placements_overlap(current, other):
                return True
    return False
