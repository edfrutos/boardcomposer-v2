from boardcomposer.domain import Board
from boardcomposer.solver.beam_search import BeamSearchConfig, beam_search
from boardcomposer.solver.maxrects.scoring import score_state
from boardcomposer.solver.maxrects.state import MaxRectsState


def search_states(
    initial: MaxRectsState,
    boards: list[Board],
    allow_rotation: bool,
    width: int,
) -> list[MaxRectsState]:
    return beam_search(
        initial=[initial],
        expand=lambda state: state.expand(
            boards=boards,
            allow_rotation=allow_rotation,
        ),
        score=score_state,
        config=BeamSearchConfig(
            width=width,
            depth=len(boards),
        ),
    )
