from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar

State = TypeVar("State")
Score = tuple[int, ...]


@dataclass(frozen=True)
class BeamSearchConfig:
    width: int
    depth: int


def beam_search(
    initial: Iterable[State],
    expand: Callable[[State], Iterable[State]],
    score: Callable[[State], Score],
    config: BeamSearchConfig,
) -> list[State]:
    beam = list(initial)

    for _ in range(config.depth):
        candidates = [next_state for state in beam for next_state in expand(state)]

        if not candidates:
            break

        beam = sorted(
            candidates,
            key=score,
            reverse=True,
        )[: config.width]

    return beam
