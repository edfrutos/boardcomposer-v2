from types import SimpleNamespace

from boardcomposer.ai.openai_provider import DEFAULT_MODEL, OpenAIProvider


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
    monkeypatch.setattr("boardcomposer.ai.openai_provider.OpenAI", lambda: fake_client)


def test_complete_returns_the_response_text(monkeypatch):
    fake_client = _FakeClient(response_text="hola desde GPT")
    _patch_client(monkeypatch, fake_client)

    answer = OpenAIProvider().complete("una pregunta")

    assert answer == "hola desde GPT"


def test_complete_sends_the_prompt_as_a_user_message(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    OpenAIProvider().complete("¿cuántas piezas caben?")

    call = fake_client.chat.completions.calls[0]
    assert call["messages"] == [{"role": "user", "content": "¿cuántas piezas caben?"}]


def test_complete_uses_the_default_model_by_default(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    OpenAIProvider().complete("prompt")

    assert fake_client.chat.completions.calls[0]["model"] == DEFAULT_MODEL


def test_a_custom_model_can_be_configured(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    OpenAIProvider(model="gpt-4o").complete("prompt")

    assert fake_client.chat.completions.calls[0]["model"] == "gpt-4o"


def test_complete_handles_an_empty_response(monkeypatch):
    fake_client = _FakeClient(response_text=None)
    _patch_client(monkeypatch, fake_client)

    assert OpenAIProvider().complete("prompt") == ""
