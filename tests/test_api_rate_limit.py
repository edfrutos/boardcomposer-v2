from boardcomposer.ai import MockAIProvider
from boardcomposer.api import create_app


def _client(rate_limit):
    app = create_app(ai_provider=MockAIProvider(), rate_limit=rate_limit)
    app.testing = True
    return app.test_client()


def test_requests_within_the_limit_all_succeed():
    client = _client(rate_limit="5 per minute")

    for _ in range(5):
        assert client.get("/strategies").status_code == 200


def test_requests_over_the_limit_are_rejected():
    client = _client(rate_limit="2 per minute")

    for _ in range(2):
        assert client.get("/strategies").status_code == 200

    response = client.get("/strategies")

    assert response.status_code == 429
    assert "error" in response.get_json()


def test_health_is_exempt_from_the_rate_limit():
    client = _client(rate_limit="1 per minute")

    for _ in range(5):
        assert client.get("/health").status_code == 200
