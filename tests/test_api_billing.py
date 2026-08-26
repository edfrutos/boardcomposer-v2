from unittest.mock import patch

from boardcomposer import billing
from boardcomposer.ai import MockAIProvider
from boardcomposer.api import API_KEY_HEADER, create_app

SOLVE_PAYLOAD = {"boards": [{"length_mm": 2000, "width_mm": 300}]}


def _client(db_path, **kwargs):
    app = create_app(ai_provider=MockAIProvider(), db_path=db_path, **kwargs)
    app.testing = True
    return app.test_client()


def test_unknown_key_rejected_when_billing_db_configured(tmp_path):
    db_path = str(tmp_path / "keys.db")
    client = _client(db_path)

    response = client.get("/strategies", headers={API_KEY_HEADER: "bc_nope"})

    assert response.status_code == 401


def test_missing_key_rejected_when_billing_db_configured(tmp_path):
    db_path = str(tmp_path / "keys.db")
    client = _client(db_path)

    response = client.get("/strategies")

    assert response.status_code == 401


def test_valid_billing_key_grants_access_to_unmetered_endpoint(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="free")
    client = _client(db_path)

    response = client.get("/strategies", headers={API_KEY_HEADER: raw_key})

    assert response.status_code == 200


def test_revoked_key_is_rejected(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="free")
    billing.revoke_key(db_path, raw_key)
    client = _client(db_path)

    response = client.get("/strategies", headers={API_KEY_HEADER: raw_key})

    assert response.status_code == 401


def test_free_plan_blocked_with_402_once_quota_exhausted(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="free")
    store = billing.InMemoryQuotaStore()
    client = _client(db_path, quota_store=store)
    headers = {API_KEY_HEADER: raw_key}

    for _ in range(billing.PLAN_LIMITS["free"]):
        response = client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)
        assert response.status_code == 200

    response = client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)

    assert response.status_code == 402
    body = response.get_json()
    assert body["plan"] == "free"
    assert body["limit"] == billing.PLAN_LIMITS["free"]


def test_paid_plan_stays_available_past_its_quota(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="basico")
    store = billing.InMemoryQuotaStore()
    client = _client(db_path, quota_store=store, rate_limit="10000 per minute")
    headers = {API_KEY_HEADER: raw_key}

    for _ in range(billing.PLAN_LIMITS["basico"] + 5):
        response = client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)
        assert response.status_code == 200


def test_metadata_endpoints_are_not_metered(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="free")
    store = billing.InMemoryQuotaStore()
    client = _client(db_path, quota_store=store)
    headers = {API_KEY_HEADER: raw_key}

    # Well past the free plan's monthly solve quota, purely on metadata
    # endpoints — none of these should ever be counted or blocked.
    for _ in range(billing.PLAN_LIMITS["free"] + 10):
        assert client.get("/strategies", headers=headers).status_code == 200
        assert client.get("/plugins", headers=headers).status_code == 200


def test_legacy_shared_key_bypasses_billing_entirely(tmp_path):
    db_path = str(tmp_path / "keys.db")
    store = billing.InMemoryQuotaStore()
    client = _client(db_path, api_key="admin-secret", quota_store=store)
    headers = {API_KEY_HEADER: "admin-secret"}

    for _ in range(billing.PLAN_LIMITS["free"] + 5):
        response = client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)
        assert response.status_code == 200


def test_health_never_requires_a_billing_key(tmp_path):
    db_path = str(tmp_path / "keys.db")
    client = _client(db_path)

    assert client.get("/health").status_code == 200


def test_overage_reported_to_stripe_once_paid_plan_exceeds_quota(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(
        db_path,
        customer_id="taller-1",
        plan="basico",
        stripe_customer_id="cus_123",
    )
    store = billing.InMemoryQuotaStore()
    client = _client(db_path, quota_store=store, rate_limit="10000 per minute")
    headers = {API_KEY_HEADER: raw_key}

    with patch("boardcomposer.api.stripe_billing.report_overage") as report_overage:
        for _ in range(billing.PLAN_LIMITS["basico"]):
            client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)
        report_overage.assert_not_called()

        client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)
        report_overage.assert_called_once_with("cus_123", "basico")


def test_no_overage_report_while_within_quota(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(
        db_path,
        customer_id="taller-1",
        plan="free",
        stripe_customer_id=None,
    )
    store = billing.InMemoryQuotaStore()
    client = _client(db_path, quota_store=store)
    headers = {API_KEY_HEADER: raw_key}

    with patch("boardcomposer.api.stripe_billing.report_overage") as report_overage:
        client.post("/solve", json=SOLVE_PAYLOAD, headers=headers)
        report_overage.assert_not_called()
