from boardcomposer import Board
from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.state import MaxRectsState


def test_state_can_be_created():
    state = MaxRectsState(
        packer=None,  # type: ignore[arg-type]
        placements=[],
        next_board=0,
    )

    assert state.next_board == 0


def test_clone_creates_independent_state():
    state = MaxRectsState(
        packer=MaxRects(),
        placements=[],
        next_board=0,
    )

    clone = state.clone()

    assert clone is not state
    assert clone.packer is not state.packer
    assert clone.placements is not state.placements
    assert clone.next_board == state.next_board


def test_expand_creates_child_states():
    state = MaxRectsState(
        packer=MaxRects(3000, 1000),
        placements=[],
        next_board=0,
    )

    children = state.expand(
        boards=[Board(1000, 500, 20, "A")],
        allow_rotation=False,
    )

    assert len(children) == 1
    assert children[0].next_board == 1
    assert len(children[0].placements) == 1


def test_expand_returns_one_child_per_candidate():
    state = MaxRectsState(
        packer=MaxRects(),
        placements=[],
        next_board=0,
    )
    state.packer.free_rectangles = [
        FreeRectangle(0, 0, 3000, 1000),
        FreeRectangle(0, 1000, 1200, 600),
    ]

    children = state.expand(
        boards=[Board(1000, 500, 20, "A")],
        allow_rotation=False,
    )

    assert len(children) == 2
