import pytest

from boardcomposer.domain.score import SolutionScore


def test_solution_score_total():
    score = SolutionScore(
        waste_score=30,
        material_usage_score=25,
        cuts_score=20,
        regularity_score=15,
        grain_score=10,
    )

    assert score.total == 100


def test_solution_score_rejects_negative_values():
    with pytest.raises(ValueError):
        SolutionScore(waste_score=-1)
