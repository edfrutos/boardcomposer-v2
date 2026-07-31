"""API key issuance and usage quotas for the paid tiers of the HTTP API.

This sits alongside the legacy single shared-secret auth in api.py (kept
for backward compatibility) and adds per-customer keys tied to a plan with
a monthly request quota. Two pieces of state are involved:

- A key registry (SQLite): which keys exist, who they belong to, which
  plan they're on. This is the source of truth for billing.
- A quota counter (QuotaStore): how many metered requests a key has used
  in the current calendar month. This is disposable — losing it just
  resets a customer's count early, it isn't billing-critical the way the
  registry is.

Redis is the recommended QuotaStore in production, since it's shared
across gunicorn workers (the existing Flask-Limiter setup is documented as
NOT being shared across workers — see api.py's module docstring). For
local development and tests, InMemoryQuotaStore avoids requiring a Redis
instance, matching the same tradeoff the existing rate limiter already
makes with its "memory://" storage_uri.
"""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

PLAN_LIMITS = {
    "free": 20,
    "basico": 300,
    "pro": 1500,
}

PAID_PLANS = {"basico", "pro"}

METERED_ENDPOINTS = {"solve", "assist_project", "assist_strategy", "assist_explain"}


def generate_key() -> str:
    return f"bc_{secrets.token_urlsafe(32)}"


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def init_db(db_path: str) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS api_keys (
                key_hash TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                plan TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            )
            """
        )
        # Added for IDE-0021 (Stripe overage billing) after api_keys already
        # existed in production — ALTER instead of just relying on the
        # CREATE above, so the VPS's real keys.db picks them up too.
        for column in ("stripe_customer_id", "stripe_subscription_item_id"):
            try:
                conn.execute(f"ALTER TABLE api_keys ADD COLUMN {column} TEXT")
            except sqlite3.OperationalError:
                pass  # already migrated


def create_key(
    db_path: str,
    customer_id: str,
    plan: str,
    stripe_customer_id: str | None = None,
    stripe_subscription_item_id: str | None = None,
) -> str:
    if plan not in PLAN_LIMITS:
        raise ValueError(f"Plan desconocido: {plan!r}. Válidos: {sorted(PLAN_LIMITS)}")

    raw_key = generate_key()
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO api_keys "
            "(key_hash, customer_id, plan, active, created_at, "
            "stripe_customer_id, stripe_subscription_item_id) "
            "VALUES (?, ?, ?, 1, ?, ?, ?)",
            (
                hash_key(raw_key),
                customer_id,
                plan,
                datetime.now(timezone.utc).isoformat(),
                stripe_customer_id,
                stripe_subscription_item_id,
            ),
        )
    return raw_key


def revoke_key(db_path: str, raw_key: str) -> bool:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE api_keys SET active = 0 WHERE key_hash = ?", (hash_key(raw_key),)
        )
        return cursor.rowcount > 0


def lookup_key(db_path: str, key_hash: str) -> dict | None:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT key_hash, customer_id, plan, active, "
            "stripe_customer_id, stripe_subscription_item_id "
            "FROM api_keys WHERE key_hash = ?",
            (key_hash,),
        ).fetchone()
        return dict(row) if row else None


class QuotaStore(Protocol):
    def increment_and_get(self, bucket: str) -> int: ...


class InMemoryQuotaStore:
    """Per-process counters. Fine for tests and single-worker dev servers;
    NOT shared across gunicorn workers — use RedisQuotaStore in production."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}

    def increment_and_get(self, bucket: str) -> int:
        self._counts[bucket] = self._counts.get(bucket, 0) + 1
        return self._counts[bucket]


class RedisQuotaStore:
    """Shared counter backed by Redis, keyed per key_hash+month with a
    35-day expiry (a bit past one month, so it self-cleans without racing
    a client clock skew against the exact month boundary)."""

    _BUCKET_TTL_SECONDS = 35 * 24 * 60 * 60

    def __init__(self, redis_client) -> None:
        self._redis = redis_client

    def increment_and_get(self, bucket: str) -> int:
        pipeline = self._redis.pipeline()
        pipeline.incr(bucket)
        pipeline.expire(bucket, self._BUCKET_TTL_SECONDS)
        count, _ = pipeline.execute()
        return int(count)


def month_bucket(key_hash: str) -> str:
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    return f"usage:{key_hash}:{month}"


@dataclass(frozen=True)
class QuotaResult:
    plan: str
    used: int
    limit: int
    allowed: bool
    overage: int


def check_quota(store: QuotaStore, key_hash: str, plan: str) -> QuotaResult:
    limit = PLAN_LIMITS.get(plan, 0)
    used = store.increment_and_get(month_bucket(key_hash))
    overage = max(0, used - limit)
    # Free (and any unrecognized plan) hard-stops at the limit; paid plans
    # stay available past their limit and accrue billable overage instead
    # (pricing model: básico 0,05€/solve extra, pro 0,03€/solve extra).
    allowed = used <= limit if plan not in PAID_PLANS else True
    return QuotaResult(
        plan=plan, used=used, limit=limit, allowed=allowed, overage=overage
    )
