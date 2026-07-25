import json

import pytest

from boardcomposer.ai import MockAIProvider, SuggestStrategyError, suggest_strategy
from boardcomposer.domain import Board, Project
from boardcomposer.solver import GeometrySolver


def _provider(response) -> MockAIProvider:
    if not isinstance(response, str):
        response = json.dumps(response)
    return MockAIProvider(response=response)


def _project() -> Project:
    return Project(boards=[Board(length_mm=1200, width_mm=600, thickness_mm=18)])


def test_suggest_strategy_builds_optimization_strategy():
    provider = _provider(
        {
            "weights": {
                "material_utilization": 70,
                "placed_boards": 20,
                "compactness": 5,
                "rotation_penalty": 5,
            },
            "generator_names": ["skyline", "maxrects"],
        }
    )

    strategy = suggest_strategy(_project(), provider, goal="minimizar desperdicio")

    assert strategy.name == "ai_suggested"
    assert strategy.weights.material_utilization == 70
    assert strategy.generator_names == ("skyline", "maxrects")


def test_suggest_strategy_strips_a_markdown_json_fence():
    # Real providers (e.g. AnthropicProvider) often wrap JSON replies in a
    # ```json ... ``` fence even when told not to; MockAIProvider normally
    # doesn't, so this exercises that response shape explicitly.
    payload = {
        "weights": {
            "material_utilization": 70,
            "placed_boards": 20,
            "compactness": 5,
            "rotation_penalty": 5,
        },
        "generator_names": ["skyline"],
    }
    provider = MockAIProvider(response=f"```json\n{json.dumps(payload)}\n```")

    strategy = suggest_strategy(_project(), provider)

    assert strategy.generator_names == ("skyline",)


def test_suggest_strategy_sends_goal_and_board_count_in_the_prompt():
    provider = _provider(
        {
            "weights": {
                "material_utilization": 40,
                "placed_boards": 30,
                "compactness": 20,
                "rotation_penalty": 10,
            },
            "generator_names": ["horizontal"],
        }
    )

    suggest_strategy(_project(), provider, goal="pocos cortes")

    prompt = provider.calls[0]
    assert "pocos cortes" in prompt
    assert "1 tablas a colocar" in prompt


def test_suggest_strategy_rejects_invalid_json():
    provider = _provider("no json")

    with pytest.raises(SuggestStrategyError):
        suggest_strategy(_project(), provider)


def test_suggest_strategy_rejects_missing_weights():
    provider = _provider({"generator_names": ["horizontal"]})

    with pytest.raises(SuggestStrategyError):
        suggest_strategy(_project(), provider)


def test_suggest_strategy_rejects_negative_weight():
    provider = _provider(
        {
            "weights": {
                "material_utilization": -1,
                "placed_boards": 30,
                "compactness": 20,
                "rotation_penalty": 10,
            },
            "generator_names": ["horizontal"],
        }
    )

    with pytest.raises(SuggestStrategyError):
        suggest_strategy(_project(), provider)


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_suggest_strategy_rejects_a_non_finite_weight(token):
    # La respuesta del asistente se parsea con json.loads, que acepta los
    # tokens NaN/Infinity: un peso NaN pasaba el `< 0` y contaminaba cada
    # puntuación, dejando la ordenación de soluciones al azar.
    provider = _provider(
        '{"weights": {"material_utilization": ' + token + ', "placed_boards": 30,'
        ' "compactness": 20, "rotation_penalty": 10},'
        ' "generator_names": ["horizontal"]}'
    )

    with pytest.raises(SuggestStrategyError, match="número finito"):
        suggest_strategy(_project(), provider)


def test_suggest_strategy_rejects_missing_generator_names():
    provider = _provider(
        {
            "weights": {
                "material_utilization": 40,
                "placed_boards": 30,
                "compactness": 20,
                "rotation_penalty": 10,
            }
        }
    )

    with pytest.raises(SuggestStrategyError):
        suggest_strategy(_project(), provider)


def test_suggest_strategy_result_works_with_geometry_solver():
    provider = _provider(
        {
            "weights": {
                "material_utilization": 70,
                "placed_boards": 20,
                "compactness": 5,
                "rotation_penalty": 5,
            },
            "generator_names": ["horizontal", "vertical"],
        }
    )
    project = Project(
        boards=[
            Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"),
            Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"),
        ]
    )

    strategy = suggest_strategy(project, provider)
    solutions = GeometrySolver(project, strategy=strategy).solve()

    assert len(solutions) > 0


def test_suggest_strategy_rejects_unknown_generator():
    provider = _provider(
        {
            "weights": {
                "material_utilization": 40,
                "placed_boards": 30,
                "compactness": 20,
                "rotation_penalty": 10,
            },
            "generator_names": ["not_a_real_generator"],
        }
    )

    with pytest.raises(SuggestStrategyError):
        suggest_strategy(_project(), provider)


def test_suggest_strategy_accepts_a_plugin_generator(monkeypatch):
    def _custom(project):
        return []

    monkeypatch.setattr(
        "boardcomposer.solver.generators.discover_plugins",
        lambda group: ({"custom": _custom}, []),
    )
    provider = _provider(
        {
            "weights": {
                "material_utilization": 40,
                "placed_boards": 30,
                "compactness": 20,
                "rotation_penalty": 10,
            },
            "generator_names": ["custom"],
        }
    )

    strategy = suggest_strategy(_project(), provider)

    assert strategy.generator_names == ("custom",)
