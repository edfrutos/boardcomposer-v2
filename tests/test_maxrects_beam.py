from boardcomposer import Board
from boardcomposer.solver.maxrects.beam import search_states
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.state import MaxRectsState


def test_search_states_places_board():
    initial = MaxRectsState(
        packer=MaxRects(3000, 1000),
        placements=[],
        next_board=0,
    )

    states = search_states(
        initial=initial,
        boards=[Board(1000, 500, 20, "A")],
        allow_rotation=False,
        width=2,
    )

    assert len(states) == 1
    assert len(states[0].placements) == 1
