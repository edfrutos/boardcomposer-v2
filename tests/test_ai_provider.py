import pytest

from boardcomposer.ai import AIProvider, MockAIProvider, provider_by_name


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
