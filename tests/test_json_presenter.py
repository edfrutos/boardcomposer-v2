import json

from boardcomposer import Board, Project
from boardcomposer.presenters import solutions_to_json
from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import compact_first_strategy


def test_solutions_to_json_contains_strategy_metadata():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    strategy = compact_first_strategy()
    solutions = GeometrySolver(project, strategy=strategy).solve()

    payload = json.loads(
        solutions_to_json(
            project=project,
            strategy=strategy,
            solutions=solutions,
            top=3,
        )
    )

    assert payload["strategy"] == "compact"
    assert payload["generators"] == ["vertical", "free_space"]
    assert "best_solution" in payload
    assert len(payload["solutions"]) <= 3
