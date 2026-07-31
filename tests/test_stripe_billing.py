import sys
from unittest.mock import MagicMock

import pytest

from boardcomposer import stripe_billing


@pytest.fixture(autouse=True)
def _no_real_stripe_env(monkeypatch):
    """Every test starts unconfigured; individual tests opt in."""
    monkeypatch.delenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, raising=False)
    monkeypatch.delenv("STRIPE_PRICE_BASICO", raising=False)
    monkeypatch.delenv("STRIPE_PRICE_PRO", raising=False)


def test_is_configured_false_without_any_env_vars():
    assert stripe_billing.is_configured("basico") is False


def test_is_configured_false_for_free_plan_even_with_env_vars(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO", "price_x")

    assert stripe_billing.is_configured("free") is False


def test_is_configured_false_missing_price_for_plan(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")

    assert stripe_billing.is_configured("basico") is False


def test_is_configured_true_when_secret_and_price_both_set(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_BASICO", "price_x")

    assert stripe_billing.is_configured("basico") is True


def test_create_customer_and_subscription_none_when_unconfigured():
    assert stripe_billing.create_customer_and_subscription("taller-1", "pro") is None


def test_create_customer_and_subscription_none_for_free_plan(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")

    assert stripe_billing.create_customer_and_subscription("taller-1", "free") is None


def test_create_customer_and_subscription_calls_stripe_when_configured(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    monkeypatch.setenv("STRIPE_PRICE_PRO", "price_pro")

    fake_stripe = MagicMock()
    fake_stripe.Customer.create.return_value = MagicMock(id="cus_123")
    fake_stripe.Subscription.create.return_value = {
        "items": {"data": [{"id": "si_123"}]}
    }
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    result = stripe_billing.create_customer_and_subscription("taller-1", "pro")

    assert result == ("cus_123", "si_123")
    fake_stripe.Customer.create.assert_called_once_with(
        name="taller-1", metadata={"boardcomposer_customer_id": "taller-1"}
    )
    fake_stripe.Subscription.create.assert_called_once_with(
        customer="cus_123", items=[{"price": "price_pro"}]
    )


def test_report_overage_noop_without_subscription_item_id(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    stripe_billing.report_overage(None)

    fake_stripe.SubscriptionItem.create_usage_record.assert_not_called()


def test_report_overage_noop_when_stripe_unconfigured():
    # No STRIPE_SECRET_KEY set — must not raise even with a real-looking id.
    stripe_billing.report_overage("si_123")


def test_report_overage_calls_stripe_when_configured(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    stripe_billing.report_overage("si_123", quantity=2)

    fake_stripe.SubscriptionItem.create_usage_record.assert_called_once_with(
        "si_123", quantity=2, action="increment"
    )


def test_report_overage_swallows_stripe_errors(monkeypatch):
    monkeypatch.setenv(stripe_billing.STRIPE_SECRET_KEY_ENV_VAR, "sk_test_x")
    fake_stripe = MagicMock()
    fake_stripe.SubscriptionItem.create_usage_record.side_effect = RuntimeError("boom")
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)

    # Must not raise — a failed usage report shouldn't break the request.
    stripe_billing.report_overage("si_123")
