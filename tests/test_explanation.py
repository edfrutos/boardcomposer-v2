from boardcomposer import AssemblySolution, SolutionExplanation


def test_solution_explanation_defaults():
    solution = AssemblySolution(placements=[])

    assert solution.explanation.strengths == []
    assert solution.explanation.weaknesses == []
    assert solution.explanation.notes == []


def test_solution_explanation_accepts_values():
    explanation = SolutionExplanation(
        strengths=["usa todo el material"],
        weaknesses=["forma irregular"],
        notes=["SequentialSolver"],
    )

    solution = AssemblySolution(placements=[], explanation=explanation)

    assert solution.explanation.strengths == ["usa todo el material"]
    assert solution.explanation.weaknesses == ["forma irregular"]
    assert solution.explanation.notes == ["SequentialSolver"]
