from boardcomposer.solver.maxrects.placement import MaxRectsPlacement


def contact_score(
    placement: MaxRectsPlacement,
    placed: list[MaxRectsPlacement],
    board_length_mm: float,
    board_width_mm: float,
    edge_weight: float = 1.0,
    board_weight: float = 1.0,
) -> float:
    score = (
        _contact_with_edges(
            placement,
            board_length_mm,
            board_width_mm,
        )
        * edge_weight
    )

    score += (
        _contact_with_placements(
            placement,
            placed,
        )
        * board_weight
    )

    return score


def _contact_with_edges(
    placement: MaxRectsPlacement,
    board_length_mm: float,
    board_width_mm: float,
) -> float:
    score = 0.0

    if placement.x_mm == 0:
        score += placement.width_mm

    if placement.y_mm == 0:
        score += placement.length_mm

    if placement.x_mm + placement.length_mm == board_length_mm:
        score += placement.width_mm

    if placement.y_mm + placement.width_mm == board_width_mm:
        score += placement.length_mm

    return score


def _contact_with_placements(
    placement: MaxRectsPlacement,
    placed: list[MaxRectsPlacement],
) -> float:
    return sum(_shared_edge(placement, other) for other in placed)


def _shared_edge(
    first: MaxRectsPlacement,
    second: MaxRectsPlacement,
) -> float:
    vertical_contact = 0.0

    if first.x_mm + first.length_mm == second.x_mm:
        vertical_contact = _overlap(
            first.y_mm,
            first.y_mm + first.width_mm,
            second.y_mm,
            second.y_mm + second.width_mm,
        )

    if second.x_mm + second.length_mm == first.x_mm:
        vertical_contact = _overlap(
            first.y_mm,
            first.y_mm + first.width_mm,
            second.y_mm,
            second.y_mm + second.width_mm,
        )

    horizontal_contact = 0.0

    if first.y_mm + first.width_mm == second.y_mm:
        horizontal_contact = _overlap(
            first.x_mm,
            first.x_mm + first.length_mm,
            second.x_mm,
            second.x_mm + second.length_mm,
        )

    if second.y_mm + second.width_mm == first.y_mm:
        horizontal_contact = _overlap(
            first.x_mm,
            first.x_mm + first.length_mm,
            second.x_mm,
            second.x_mm + second.length_mm,
        )

    return vertical_contact + horizontal_contact


def _overlap(
    first_start: float,
    first_end: float,
    second_start: float,
    second_end: float,
) -> float:
    return max(
        0.0,
        min(first_end, second_end) - max(first_start, second_start),
    )
