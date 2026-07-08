from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_engine import iter_maxrects_candidates


def _project() -> Project:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))
    return project


def test_iter_maxrects_candidates_uses_classic_candidates_by_default():
    candidates = list(iter_maxrects_candidates(_project()))

    assert candidates
    assert all("maxrects" in candidate.explanation.notes for candidate in candidates)


def test_iter_maxrects_candidates_can_use_beam():
    candidates = list(
        iter_maxrects_candidates(
            _project(),
            beam_width=2,
        )
    )

    assert len(candidates) == 12
    assert all("beam" in candidate.explanation.notes for candidate in candidates)
