from boardcomposer import AssemblySolution
from boardcomposer.solver.evaluation import evaluate


def test_evaluation_returns_score():
    solution = evaluate(AssemblySolution(placements=[]))

    assert solution.score.total >= 0
