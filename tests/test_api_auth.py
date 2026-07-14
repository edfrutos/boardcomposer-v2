from boardcomposer.ai import MockAIProvider
from boardcomposer.api import API_KEY_HEADER, create_app


def _client(**kwargs):
    app = create_app(ai_provider=MockAIProvider(), **kwargs)
    app.testing = True
    return app.test_client()


def test_no_api_key_configured_allows_requests_without_a_header():
    client = _client()

    response = client.get("/strategies")

    assert response.status_code == 200


def test_configured_api_key_rejects_requests_without_a_header():
    client = _client(api_key="secreto")

    response = client.get("/strategies")

    assert response.status_code == 401


def test_configured_api_key_rejects_a_wrong_header():
    client = _client(api_key="secreto")

    response = client.get("/strategies", headers={API_KEY_HEADER: "otro"})

    assert response.status_code == 401


def test_configured_api_key_accepts_the_right_header():
    client = _client(api_key="secreto")

    response = client.get("/strategies", headers={API_KEY_HEADER: "secreto"})

    assert response.status_code == 200


def test_health_never_requires_an_api_key():
    client = _client(api_key="secreto")

    response = client.get("/health")

    assert response.status_code == 200
