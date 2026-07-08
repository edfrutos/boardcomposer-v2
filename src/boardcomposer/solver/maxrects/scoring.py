from boardcomposer.solver.maxrects.state import MaxRectsState


def score_state(state: MaxRectsState) -> tuple[int, int, int]:
    return (
        len(state.placements),
        -state.packer.width_mm,
        -state.packer.length_mm,
    )
