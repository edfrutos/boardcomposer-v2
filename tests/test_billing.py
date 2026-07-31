import pytest

from boardcomposer import billing


def test_generate_key_has_stable_prefix_and_is_unique():
    a, b = billing.generate_key(), billing.generate_key()

    assert a.startswith("bc_")
    assert a != b


def test_hash_key_is_deterministic_and_not_the_raw_value():
    raw = "bc_something"

    assert billing.hash_key(raw) == billing.hash_key(raw)
    assert billing.hash_key(raw) != raw


def test_create_key_then_lookup_by_hash(tmp_path):
    db_path = str(tmp_path / "keys.db")

    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="pro")
    record = billing.lookup_key(db_path, billing.hash_key(raw_key))

    assert record["customer_id"] == "taller-1"
    assert record["plan"] == "pro"
    assert record["active"] == 1


def test_lookup_unknown_key_returns_none(tmp_path):
    db_path = str(tmp_path / "keys.db")
    billing.init_db(db_path)

    assert billing.lookup_key(db_path, "nope") is None


def test_create_key_rejects_unknown_plan(tmp_path):
    db_path = str(tmp_path / "keys.db")

    with pytest.raises(ValueError):
        billing.create_key(db_path, customer_id="taller-1", plan="enterprise")


def test_revoke_key_deactivates_it(tmp_path):
    db_path = str(tmp_path / "keys.db")
    raw_key = billing.create_key(db_path, customer_id="taller-1", plan="free")

    assert billing.revoke_key(db_path, raw_key) is True

    record = billing.lookup_key(db_path, billing.hash_key(raw_key))
    assert record["active"] == 0


def test_revoke_unknown_key_returns_false(tmp_path):
    db_path = str(tmp_path / "keys.db")
    billing.init_db(db_path)

    assert billing.revoke_key(db_path, "bc_never-issued") is False


def test_in_memory_quota_store_increments_per_bucket():
    store = billing.InMemoryQuotaStore()

    assert store.increment_and_get("a") == 1
    assert store.increment_and_get("a") == 2
    assert store.increment_and_get("b") == 1


def test_check_quota_free_plan_blocks_once_limit_reached():
    store = billing.InMemoryQuotaStore()
    key_hash = "somehash"

    for _ in range(billing.PLAN_LIMITS["free"]):
        result = billing.check_quota(store, key_hash, "free")
        assert result.allowed is True

    over_limit = billing.check_quota(store, key_hash, "free")

    assert over_limit.allowed is False
    assert over_limit.used == billing.PLAN_LIMITS["free"] + 1
    assert over_limit.overage == 1


def test_check_quota_paid_plan_stays_allowed_past_limit_and_tracks_overage():
    store = billing.InMemoryQuotaStore()
    key_hash = "somehash"

    results = [
        billing.check_quota(store, key_hash, "basico")
        for _ in range(billing.PLAN_LIMITS["basico"] + 3)
    ]

    assert results[-1].allowed is True
    assert results[-1].overage == 3


def test_check_quota_unknown_plan_has_zero_limit_and_blocks_immediately():
    store = billing.InMemoryQuotaStore()

    result = billing.check_quota(store, "somehash", "unknown")

    assert result.limit == 0
    assert result.allowed is False
