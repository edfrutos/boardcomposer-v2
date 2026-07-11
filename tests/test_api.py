import json

import pytest

from boardcomposer.ai import MockAIProvider
from boardcomposer.api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def _client_with_json_response(payload) -> object:
    app = create_app(ai_provider=MockAIProvider(response=json.dumps(payload)))
    app.testing = True
    return app.test_client()


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_strategies_lists_known_names(client):
    response = client.get("/strategies")

    assert response.status_code == 200
    assert response.get_json()["strategies"] == ["balanced", "material", "compact"]


def test_solve_with_valid_boards_returns_solutions(client):
    response = client.post(
        "/solve",
        json={
            "boards": [
                {"id": "A", "length_mm": 500, "width_mm": 300, "thickness_mm": 20},
                {"id": "B", "length_mm": 400, "width_mm": 300, "thickness_mm": 20},
            ],
            "constraints": {"max_length_mm": 3000, "max_width_mm": 600},
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["strategy"] == "balanced"
    assert len(data["solutions"]) >= 1
    assert data["solutions"][0]["placed_boards"] >= 1


def test_solve_rejects_missing_boards(client):
    response = client.post("/solve", json={})

    assert response.status_code == 400
    assert "boards" in response.get_json()["error"]


def test_solve_rejects_empty_boards_list(client):
    response = client.post("/solve", json={"boards": []})

    assert response.status_code == 400


def test_solve_rejects_non_json_body(client):
    response = client.post("/solve", data="not json", content_type="text/plain")

    assert response.status_code == 400


def test_solve_rejects_invalid_board_fields(client):
    response = client.post(
        "/solve", json={"boards": [{"id": "A", "length_mm": "not-a-number"}]}
    )

    assert response.status_code == 400
    assert "Tabla inválida" in response.get_json()["error"]


def test_solve_rejects_unknown_strategy(client):
    response = client.post(
        "/solve",
        json={
            "boards": [{"id": "A", "length_mm": 500, "width_mm": 300}],
            "strategy": "does-not-exist",
        },
    )

    assert response.status_code == 400


def test_solve_rejects_invalid_top(client):
    response = client.post(
        "/solve",
        json={
            "boards": [{"id": "A", "length_mm": 500, "width_mm": 300}],
            "top": 0,
        },
    )

    assert response.status_code == 400


def test_solve_with_impossible_constraints_returns_a_degenerate_solution(client):
    # The Core never returns an empty solutions list here: a piece that
    # doesn't fit anywhere still yields an AssemblySolution with 0
    # placements (0 <= any max_length_mm, so respects_constraints() lets
    # it through) rather than the pipeline filtering it out entirely.
    response = client.post(
        "/solve",
        json={
            "boards": [{"id": "A", "length_mm": 5000, "width_mm": 5000}],
            "constraints": {"max_length_mm": 100, "max_width_mm": 100},
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["solutions"][0]["placed_boards"] == 0


def test_assist_project_builds_boards_from_text():
    client = _client_with_json_response(
        {"boards": [{"id": "A", "length_mm": 1200, "width_mm": 600}]}
    )

    response = client.post("/assist/project", json={"text": "una tabla de 1200x600"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["boards"] == [
        {"id": "A", "length_mm": 1200, "width_mm": 600, "thickness_mm": 1}
    ]
    assert data["constraints"] == {
        "max_length_mm": None,
        "max_width_mm": None,
        "allow_rotation": False,
        "allow_cutting": False,
    }


def test_assist_project_rejects_missing_text(client):
    response = client.post("/assist/project", json={})

    assert response.status_code == 400
    assert "text" in response.get_json()["error"]


def test_assist_project_returns_502_when_the_provider_reply_is_not_json(client):
    # create_app()'s default provider is a MockAIProvider with a plain-text
    # canned reply, not JSON — this is the real behaviour today, since
    # there's no AIProvider that actually produces JSON wired in yet.
    response = client.post("/assist/project", json={"text": "una tabla"})

    assert response.status_code == 502


def test_assist_strategy_solves_with_the_suggested_strategy():
    client = _client_with_json_response(
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

    response = client.post(
        "/assist/strategy",
        json={
            "boards": [
                {"id": "A", "length_mm": 2000, "width_mm": 300},
                {"id": "B", "length_mm": 1000, "width_mm": 300},
            ],
            "goal": "minimizar desperdicio",
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["strategy"] == "ai_suggested"
    assert len(data["solutions"]) >= 1


def test_assist_strategy_rejects_missing_boards(client):
    response = client.post("/assist/strategy", json={"goal": "algo"})

    assert response.status_code == 400
    assert "boards" in response.get_json()["error"]


def test_assist_strategy_returns_502_when_the_provider_reply_is_not_json(client):
    response = client.post(
        "/assist/strategy",
        json={"boards": [{"id": "A", "length_mm": 500, "width_mm": 300}]},
    )

    assert response.status_code == 502


def test_assist_explain_returns_solve_results_plus_an_explanation(client):
    response = client.post(
        "/assist/explain",
        json={"boards": [{"id": "A", "length_mm": 500, "width_mm": 300}]},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["solutions"][0]["placed_boards"] >= 1
    assert data["assistant_explanation"] == "Respuesta simulada del asistente IA."


def test_assist_explain_rejects_missing_boards(client):
    response = client.post("/assist/explain", json={})

    assert response.status_code == 400
