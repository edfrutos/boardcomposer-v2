import sys
from unittest.mock import MagicMock

import pytest

from boardcomposer import stripe_billing


@pytest.fixture(autouse=True)
def _no_real_stripe_env(monkeypatch):
    """Every test starts unconfigured; individual tests opt in."""
    monkeypatch.delenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, raising=False)
    monkeypatch.delenv("STRIPE_PRICE_BASICO", raising=False)
    monkeypatch.delenv("STRIPE_PRICE_BASICO_OVERAGE", raising=False)
    monkeypatch.delenv("STRIPE_PRICE_PRO", raising=False)
    monkeypatch.delenv("STRIPE_PRICE_PRO_OVERAGE", raising=False)


def test_is_configured_false_without_any_env_vars():
    assert stripe_billing.is_configured("basico") is False


def test_is_configured_false_for_free_plan_even_with_env_vars(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO", "price_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO_OVERAGE", "price_x_overage")

    assert stripe_billing.is_configured("free") is False


def test_is_configured_false_missing_price_for_plan(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")

    assert stripe_billing.is_configured("basico") is False


def test_is_configured_false_missing_only_overage_price(monkeypatch):
    # Reported as unconfigured, not "half configured" — creating a
    # Subscription with only the base item would silently drop overage
    # billing instead of failing loudly.
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO", "price_x")

    assert stripe_billing.is_configured("basico") is False


def test_is_configured_true_when_secret_and_both_prices_set(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO", "price_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO_OVERAGE", "price_x_overage")

    assert stripe_billing.is_configured("basico") is True


def test_create_customer_and_subscription_none_when_unconfigured():
    assert stripe_billing.create_customer_and_subscription("taller-1", "pro") is None


def test_create_customer_and_subscription_none_for_free_plan(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")

    assert stripe_billing.create_customer_and_subscription("taller-1", "free") is None


def test_create_customer_and_subscription_calls_stripe_when_configured(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_PRO", "price_pro")
    monkeypatch.setenv("STRIPE_PRICE_PRO_OVERAGE", "price_pro_overage")

    fake_stripe = MagicMock()
    fake_stripe.Customer.create.return_value = MagicMock(id="cus_123")
    fake_stripe.Subscription.create.return_value = {
        "items": {
            "data": [
                {"id": "si_base", "price": {"id": "price_pro"}},
                {"id": "si_overage", "price": {"id": "price_pro_overage"}},
            ]
        }
    }
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    result = stripe_billing.create_customer_and_subscription("taller-1", "pro")

    # Only the overage item's id comes back — report_overage() must never
    # report usage against the flat base-fee item.
    assert result == ("cus_123", "si_overage")
    fake_stripe.Customer.create.assert_called_once_with(
        name="taller-1", metadata={"boardcomposer_customer_id": "taller-1"}
    )
    fake_stripe.Subscription.create.assert_called_once_with(
        customer="cus_123",
        items=[{"price": "price_pro"}, {"price": "price_pro_overage"}],
    )


def test_create_customer_and_subscription_finds_overage_item_regardless_of_order(
    monkeypatch,
):
    # Stripe doesn't guarantee the order of items[].data matches the order
    # they were requested in — the lookup must key off the price id, not
    # a fixed index.
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_PRO", "price_pro")
    monkeypatch.setenv("STRIPE_PRICE_PRO_OVERAGE", "price_pro_overage")

    fake_stripe = MagicMock()
    fake_stripe.Customer.create.return_value = MagicMock(id="cus_123")
    fake_stripe.Subscription.create.return_value = {
        "items": {
            "data": [
                {"id": "si_overage", "price": {"id": "price_pro_overage"}},
                {"id": "si_base", "price": {"id": "price_pro"}},
            ]
        }
    }
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    result = stripe_billing.create_customer_and_subscription("taller-1", "pro")

    assert result == ("cus_123", "si_overage")


def test_report_overage_noop_without_customer_id(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    stripe_billing.report_overage(None, "basico")

    fake_stripe.billing.MeterEvent.create.assert_not_called()


def test_report_overage_noop_for_unknown_plan(monkeypatch):
    # No meter event name mapped for this plan — must not guess one.
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    stripe_billing.report_overage("cus_123", "free")

    fake_stripe.billing.MeterEvent.create.assert_not_called()


def test_report_overage_noop_when_stripe_unconfigured():
    # No STRIPE_SECRET_KEY set — must not raise even with a real-looking id.
    stripe_billing.report_overage("cus_123", "basico")


def test_report_overage_calls_stripe_when_configured(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    stripe_billing.report_overage("cus_123", "pro", quantity=2)

    fake_stripe.billing.MeterEvent.create.assert_called_once_with(
        event_name="boardcomposer_pro_overage",
        payload={"value": 2, "stripe_customer_id": "cus_123"},
    )


def test_report_overage_swallows_stripe_errors(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    fake_stripe.billing.MeterEvent.create.side_effect = RuntimeError("boom")
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    # Must not raise — a failed usage report shouldn't break the request.
    stripe_billing.report_overage("cus_123", "basico")
