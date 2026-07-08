from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.scoring import score_state
from boardcomposer.solver.maxrects.state import MaxRectsState


def test_score_state_prefers_more_placements():
    state = MaxRectsState(
        packer=MaxRects(3000, 1000),
        placements=[],
        next_board=0,
    )

    assert score_state(state) == (0, -1000, -3000)
