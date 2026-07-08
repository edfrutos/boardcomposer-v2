from boardcomposer.domain import AssemblySolution


def material_utilization(solution: AssemblySolution) -> float:
    if solution.bounding_area_mm2 == 0:
        return 0.0
    return solution.used_area_mm2 / solution.bounding_area_mm2


def compactness(solution: AssemblySolution) -> float:
    if solution.total_length_mm == 0 or solution.total_width_mm == 0:
        return 0.0

    long_side = max(solution.total_length_mm, solution.total_width_mm)
    short_side = min(solution.total_length_mm, solution.total_width_mm)

    return short_side / long_side


def rotation_ratio(solution: AssemblySolution) -> float:
    if not solution.placements:
        return 0.0

    rotated = sum(1 for placement in solution.placements if placement.rotated)
    return rotated / len(solution.placements)


def placed_board_ratio(solution: AssemblySolution, total_boards: int) -> float:
    if total_boards == 0:
        return 0.0

    return len(solution.placements) / total_boards
