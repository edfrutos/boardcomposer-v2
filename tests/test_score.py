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


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize(
    "field",
    [
        "waste_score",
        "material_usage_score",
        "cuts_score",
        "regularity_score",
        "grain_score",
    ],
)
def test_solution_score_rejects_non_finite_values(field, value):
    with pytest.raises(ValueError, match="número finito"):
        SolutionScore(**{field: value})
