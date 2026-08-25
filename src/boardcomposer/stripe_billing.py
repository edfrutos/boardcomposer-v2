"""Stripe integration for the paid plans (IDE-0021, follow-up to billing.py's
IDE-0020): creates a Customer+Subscription when a básico/pro key is issued,
and reports overage usage against it. The free plan never touches Stripe —
there's nothing to bill.

Fully optional, same pattern as REDIS_URL in api.py: without
STRIPE_SECRET_KEY and the plan's Price IDs set, every function here is a
no-op, so billing.py/manage_keys.py work exactly as they did before this
module existed. `stripe` is imported lazily inside _client() so it's only
a hard dependency when actually configured — tests never need the package
installed, only api.py's `[prod]` extra does.

Two Price objects per plan, not one (DT-0038): `api.py` only calls
`report_overage()` once a request is past the plan's included quota
(`billing.check_quota()`), always `quantity=1` for that one request — it
never reports the in-quota usage at all. A single metered/tiered Price
keyed to the plan's own included quantity (300/1500) would then
systematically undercount: Stripe would see far fewer reported units than
that boundary and never actually cross into the paid tier, silently
under-billing every overage customer. Splitting the flat monthly fee (a
plain recurring Price, billed by Stripe on its own schedule, no metering
involved) from the overage-only metered Price (billed by exactly what
`report_overage()` reports, no tiers to fall out of sync with) sidesteps
that mismatch entirely — only the overage item's id needs tracking
app-side, matching the single `stripe_subscription_item_id` column
`billing.py` already had before this fix.
"""

from __future__ import annotations

import logging
import os

from boardcomposer.billing import PAID_PLANS

logger = logging.getLogger(__name__)

STRIPE_SECRET_KEY_ENV_VAR = "STRIPE_SECRET_KEY"
PLAN_PRICE_ENV_VARS = {
    "basico": {"base": "STRIPE_PRICE_BASICO", "overage": "STRIPE_PRICE_BASICO_OVERAGE"},
    "pro": {"base": "STRIPE_PRICE_PRO", "overage": "STRIPE_PRICE_PRO_OVERAGE"},
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
    price_vars = PLAN_PRICE_ENV_VARS[plan]
    return bool(os.environ.get(price_vars["base"])) and bool(
        os.environ.get(price_vars["overage"])
    )


def create_customer_and_subscription(
    customer_id: str, plan: str
) -> tuple[str, str] | None:
    """Returns (stripe_customer_id, overage_subscription_item_id) for a new
    Customer + two-item Subscription (flat base fee + metered overage) on
    the plan's Prices, or None if Stripe isn't configured for this plan
    (free plan, or missing env vars) — callers treat None as "issue the
    key without Stripe billing". Only the overage item's id is returned:
    the base item needs no app-side tracking, Stripe bills it
    automatically every period regardless of usage."""
    if not is_configured(plan):
        return None

    stripe = _client()
    assert stripe is not None  # is_configured() already checked STRIPE_SECRET_KEY
    price_vars = PLAN_PRICE_ENV_VARS[plan]
    base_price_id = os.environ.get(price_vars["base"])
    overage_price_id = os.environ.get(price_vars["overage"])

    customer = stripe.Customer.create(
        name=customer_id, metadata={"boardcomposer_customer_id": customer_id}
    )
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{"price": base_price_id}, {"price": overage_price_id}],
    )
    overage_item_id = next(
        item["id"]
        for item in subscription["items"]["data"]
        if item["price"]["id"] == overage_price_id
    )
    return customer.id, overage_item_id


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
