"""Stripe integration for the paid plans (IDE-0021, follow-up to billing.py's
IDE-0020): creates a Customer+Subscription when a básico/pro key is issued,
and reports overage usage against it. The free plan never touches Stripe —
there's nothing to bill.

Fully optional, same pattern as REDIS_URL in api.py: without
STRIPE_SECRET_KEY and the plan's Price ID set, every function here is a
no-op, so billing.py/manage_keys.py work exactly as they did before this
module existed. `stripe` is imported lazily inside _client() so it's only
a hard dependency when actually configured — tests never need the package
installed, only api.py's `[prod]` extra does.
"""

from __future__ import annotations

import logging
import os

from boardcomposer.billing import PAID_PLANS

logger = logging.getLogger(__name__)

STRIPE_SECRET_KEY_ENV_VAR = "STRIPE_SECRET_KEY"
PLAN_PRICE_ENV_VARS = {
    "basico": "STRIPE_PRICE_BASICO",
    "pro": "STRIPE_PRICE_PRO",
}


def _client():
    secret_key = os.environ.get(STRIPE_SECRET_KEY_ENV_VAR)
    if not secret_key:
        return None

    import stripe

    stripe.api_key = secret_key
    return stripe


def is_configured(plan: str) -> bool:
    if plan not in PAID_PLANS:
        return False
    if not os.environ.get(STRIPE_SECRET_KEY_ENV_VAR):
        return False
    return bool(os.environ.get(PLAN_PRICE_ENV_VARS[plan]))


def create_customer_and_subscription(
    customer_id: str, plan: str
) -> tuple[str, str] | None:
    """Returns (stripe_customer_id, subscription_item_id) for a new
    Customer + Subscription on the plan's Price, or None if Stripe isn't
    configured for this plan (free plan, or missing env vars) — callers
    treat None as "issue the key without Stripe billing"."""
    if not is_configured(plan):
        return None

    stripe = _client()
    assert stripe is not None  # is_configured() already checked STRIPE_SECRET_KEY
    price_id = os.environ.get(PLAN_PRICE_ENV_VARS[plan])

    customer = stripe.Customer.create(
        name=customer_id, metadata={"boardcomposer_customer_id": customer_id}
    )
    subscription = stripe.Subscription.create(
        customer=customer.id, items=[{"price": price_id}]
    )
    subscription_item_id = subscription["items"]["data"][0]["id"]
    return customer.id, subscription_item_id


def report_overage(subscription_item_id: str | None, quantity: int = 1) -> None:
    """Best-effort: never raises. A failed usage report shouldn't break the
    customer's actual /solve request — worst case that unit of overage
    isn't billed this cycle, which is a smaller problem than a 500."""
    if not subscription_item_id:
        return

    stripe = _client()
    if stripe is None:
        return

    try:
        stripe.SubscriptionItem.create_usage_record(
            subscription_item_id, quantity=quantity, action="increment"
        )
    except Exception:
        logger.exception(
            "Fallo al reportar overage a Stripe (subscription_item=%s)",
            subscription_item_id,
        )
