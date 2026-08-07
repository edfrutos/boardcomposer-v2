from types import SimpleNamespace

import pytest

from boardcomposer.ai.ollama_provider import DEFAULT_HOST, OllamaProvider


class _FakeCompletions:
    def __init__(self, response_text):
        self.response_text = response_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content=self.response_text))
            ]
        )


class _FakeClient:
    def __init__(self, response_text="respuesta de prueba"):
        self.chat = SimpleNamespace(completions=_FakeCompletions(response_text))


def _patch_client(monkeypatch, fake_client):
    calls = []

    def fake_openai(**kwargs):
        calls.append(kwargs)
        return fake_client

    monkeypatch.setattr("boardcomposer.ai.ollama_provider.OpenAI", fake_openai)
    return calls


def test_requires_a_model_from_argument_or_env_var(monkeypatch):
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    with pytest.raises(ValueError):
        OllamaProvider()


def test_model_can_come_from_the_env_var(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1")
    _patch_client(monkeypatch, _FakeClient())

    assert OllamaProvider().model == "llama3.1"


def test_model_argument_overrides_the_env_var(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1")
    _patch_client(monkeypatch, _FakeClient())

    assert OllamaProvider(model="mistral").model == "mistral"


def test_defaults_to_the_local_ollama_host(monkeypatch):
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    client_calls = _patch_client(monkeypatch, _FakeClient())

    OllamaProvider(model="llama3.1")

    assert client_calls[0]["base_url"] == f"{DEFAULT_HOST}/v1"


def test_host_can_come_from_the_env_var(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "http://192.168.1.10:11434")
    client_calls = _patch_client(monkeypatch, _FakeClient())

    OllamaProvider(model="llama3.1")

    assert client_calls[0]["base_url"] == "http://192.168.1.10:11434/v1"


def test_host_argument_overrides_the_env_var(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "http://192.168.1.10:11434")
    client_calls = _patch_client(monkeypatch, _FakeClient())

    OllamaProvider(model="llama3.1", host="http://otro-equipo:11434")

    assert client_calls[0]["base_url"] == "http://otro-equipo:11434/v1"


def test_complete_returns_the_response_text(monkeypatch):
    fake_client = _FakeClient(response_text="hola desde Ollama")
    _patch_client(monkeypatch, fake_client)

    answer = OllamaProvider(model="llama3.1").complete("una pregunta")

    assert answer == "hola desde Ollama"


def test_complete_sends_the_prompt_and_model(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    OllamaProvider(model="llama3.1").complete("¿cuántas piezas caben?")

    call = fake_client.chat.completions.calls[0]
    assert call["model"] == "llama3.1"
    assert call["messages"] == [{"role": "user", "content": "¿cuántas piezas caben?"}]


def test_complete_handles_an_empty_response(monkeypatch):
    fake_client = _FakeClient(response_text=None)
    _patch_client(monkeypatch, fake_client)

    assert OllamaProvider(model="llama3.1").complete("prompt") == ""
