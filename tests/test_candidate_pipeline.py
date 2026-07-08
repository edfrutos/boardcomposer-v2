from boardcomposer import Board, Project
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.strategies import compact_first_strategy


def test_candidate_pipeline_returns_ranked_solutions():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    pipeline = CandidatePipeline(
        project=project,
        strategy=compact_first_strategy(),
    )

    solutions = pipeline.run()

    assert len(solutions) > 0
    assert solutions[0].score.total >= solutions[-1].score.total
