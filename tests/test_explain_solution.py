from boardcomposer.ai import MockAIProvider, explain_solution
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    SolutionExplanation,
    SolutionScore,
)


def _solution() -> AssemblySolution:
    return AssemblySolution(
        placements=[
            BoardPlacement(board_id="A", x_mm=0, y_mm=0, length_mm=1000, width_mm=500),
        ],
        score=SolutionScore(waste_score=20, material_usage_score=30),
        explanation=SolutionExplanation(
            strengths=["usa todo el material"],
            weaknesses=["forma irregular"],
            notes=["SequentialSolver"],
        ),
    )


def test_explain_solution_returns_the_provider_response():
    provider = MockAIProvider(response="Esta solución aprovecha bien el material.")

    explanation = explain_solution(_solution(), provider)

    assert explanation == "Esta solución aprovecha bien el material."


def test_explain_solution_includes_solution_data_in_the_prompt():
    provider = MockAIProvider()

    explain_solution(_solution(), provider)

    prompt = provider.calls[0]
    assert "Tablas colocadas: 1" in prompt
    assert "usa todo el material" in prompt
    assert "forma irregular" in prompt
    assert "SequentialSolver" in prompt


def test_explain_solution_handles_empty_explanation():
    solution = AssemblySolution(placements=[])
    provider = MockAIProvider()

    explain_solution(solution, provider)

    prompt = provider.calls[0]
    assert "Tablas colocadas: 0" in prompt
    assert "ninguno registrado" in prompt
    assert "ninguna" in prompt
