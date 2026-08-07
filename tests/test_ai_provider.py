from types import SimpleNamespace

import pytest

from boardcomposer.ai import (
    AIProvider,
    AnthropicProvider,
    GeminiProvider,
    MockAIProvider,
    OllamaProvider,
    OpenAIProvider,
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
    monkeypatch.delenv("BOARDCOMPOSER_AI_PROVIDER", raising=False)

    assert isinstance(default_provider(), MockAIProvider)


def test_default_provider_is_anthropic_with_an_api_key(monkeypatch):
    monkeypatch.delenv("BOARDCOMPOSER_AI_PROVIDER", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        "boardcomposer.ai.anthropic_provider.Anthropic", lambda: object()
    )

    assert isinstance(default_provider(), AnthropicProvider)


def test_provider_by_name_returns_openai(monkeypatch):
    monkeypatch.setattr("boardcomposer.ai.openai_provider.OpenAI", lambda: object())

    provider = provider_by_name("openai")

    assert isinstance(provider, OpenAIProvider)


def test_provider_by_name_returns_gemini(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.ai.gemini_provider.genai",
        SimpleNamespace(Client=lambda: object()),
    )

    provider = provider_by_name("gemini")

    assert isinstance(provider, GeminiProvider)


def test_provider_by_name_returns_ollama(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1")
    monkeypatch.setattr(
        "boardcomposer.ai.ollama_provider.OpenAI", lambda **kwargs: object()
    )

    provider = provider_by_name("ollama")

    assert isinstance(provider, OllamaProvider)


def test_default_provider_honours_an_explicit_provider_choice(monkeypatch):
    # IDE-0036: BOARDCOMPOSER_AI_PROVIDER (bridged from Preferences' active-
    # provider dropdown) overrides the legacy anthropic-if-key-present
    # fallback, even when an ANTHROPIC_API_KEY happens to be set too.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("BOARDCOMPOSER_AI_PROVIDER", "openai")
    monkeypatch.setattr("boardcomposer.ai.openai_provider.OpenAI", lambda: object())

    assert isinstance(default_provider(), OpenAIProvider)


def test_default_provider_rejects_an_unknown_explicit_provider_choice(monkeypatch):
    monkeypatch.setenv("BOARDCOMPOSER_AI_PROVIDER", "not-a-real-provider")

    with pytest.raises(ValueError):
        default_provider()
