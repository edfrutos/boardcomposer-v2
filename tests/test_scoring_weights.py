from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.solver.evaluation import evaluate
from boardcomposer.solver.scoring_weights import ScoringWeights


def test_custom_scoring_weights():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    score = evaluate(
        solution,
        total_boards=1,
        weights=ScoringWeights(
            material_utilization=100,
            placed_boards=0,
            compactness=0,
            rotation_penalty=0,
        ),
    ).score

    assert score.waste_score == 100
