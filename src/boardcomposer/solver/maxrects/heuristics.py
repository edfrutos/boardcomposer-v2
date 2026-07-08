from collections.abc import Callable

from boardcomposer.solver.maxrects.placement import MaxRectsPlacement

WasteAreaFn = Callable[[MaxRectsPlacement], float]
Heuristic = Callable[
    [list[MaxRectsPlacement], WasteAreaFn],
    MaxRectsPlacement | None,
]


def best_area_fit(
    candidates: list[MaxRectsPlacement],
    waste_area: WasteAreaFn,
) -> MaxRectsPlacement | None:
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda candidate: (
            waste_area(candidate),
            candidate.y_mm,
            candidate.x_mm,
        ),
    )


def best_short_side_fit(
    candidates: list[MaxRectsPlacement],
    waste_area: WasteAreaFn,
) -> MaxRectsPlacement | None:
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda candidate: (
            min(candidate.length_mm, candidate.width_mm),
            max(candidate.length_mm, candidate.width_mm),
            candidate.y_mm,
            candidate.x_mm,
        ),
    )


def best_long_side_fit(
    candidates: list[MaxRectsPlacement],
    waste_area: WasteAreaFn,
) -> MaxRectsPlacement | None:
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda candidate: (
            max(candidate.length_mm, candidate.width_mm),
            min(candidate.length_mm, candidate.width_mm),
            candidate.y_mm,
            candidate.x_mm,
        ),
    )


def best_bottom_left_fit(
    candidates: list[MaxRectsPlacement],
    waste_area: WasteAreaFn,
) -> MaxRectsPlacement | None:
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda candidate: (
            candidate.y_mm + candidate.width_mm,
            candidate.x_mm,
            waste_area(candidate),
        ),
    )
