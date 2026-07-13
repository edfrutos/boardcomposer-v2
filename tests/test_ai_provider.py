import pytest

from boardcomposer.ai import (
    AIProvider,
    AnthropicProvider,
    MockAIProvider,
    default_provider,
    provider_by_name,
)


def test_mock_provider_returns_configured_response():
    provider = MockAIProvider(response="hola")

    assert provider.complete("cualquier prompt") == "hola"


def test_mock_provider_records_prompts():
    provider = MockAIProvider()

    provider.complete("primero")
    provider.complete("segundo")

    assert provider.calls == ["primero", "segundo"]


def test_mock_provider_is_an_ai_provider():
    assert isinstance(MockAIProvider(), AIProvider)


def test_provider_by_name_returns_mock():
    provider = provider_by_name("mock")

    assert isinstance(provider, MockAIProvider)


def test_provider_by_name_rejects_unknown_provider():
    with pytest.raises(ValueError):
        provider_by_name("unknown")


def test_provider_by_name_returns_anthropic(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.ai.anthropic_provider.Anthropic", lambda: object()
    )

    provider = provider_by_name("anthropic")

    assert isinstance(provider, AnthropicProvider)


def test_default_provider_is_mock_without_an_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    assert isinstance(default_provider(), MockAIProvider)


def test_default_provider_is_anthropic_with_an_api_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        "boardcomposer.ai.anthropic_provider.Anthropic", lambda: object()
    )

    assert isinstance(default_provider(), AnthropicProvider)
