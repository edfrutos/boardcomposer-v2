from types import SimpleNamespace

from boardcomposer.ai.anthropic_provider import DEFAULT_MODEL, AnthropicProvider


class _FakeMessages:
    def __init__(self, response_text):
        self.response_text = response_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=self.response_text)]
        )


class _FakeClient:
    def __init__(self, response_text="respuesta de prueba"):
        self.messages = _FakeMessages(response_text)


def _patch_client(monkeypatch, fake_client):
    monkeypatch.setattr(
        "boardcomposer.ai.anthropic_provider.Anthropic", lambda: fake_client
    )


def test_complete_returns_the_response_text(monkeypatch):
    fake_client = _FakeClient(response_text="hola desde Claude")
    _patch_client(monkeypatch, fake_client)

    answer = AnthropicProvider().complete("una pregunta")

    assert answer == "hola desde Claude"


def test_complete_sends_the_prompt_as_a_user_message(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    AnthropicProvider().complete("¿cuántas piezas caben?")

    call = fake_client.messages.calls[0]
    assert call["messages"] == [
        {"role": "user", "content": "¿cuántas piezas caben?"}
    ]


def test_complete_uses_the_default_model_by_default(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    AnthropicProvider().complete("prompt")

    assert fake_client.messages.calls[0]["model"] == DEFAULT_MODEL


def test_a_custom_model_can_be_configured(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    AnthropicProvider(model="claude-opus-4-8").complete("prompt")

    assert fake_client.messages.calls[0]["model"] == "claude-opus-4-8"


def test_complete_ignores_non_text_content_blocks(monkeypatch):
    fake_client = _FakeClient()
    fake_client.messages.create = lambda **kwargs: SimpleNamespace(
        content=[
            SimpleNamespace(type="tool_use", text=None),
            SimpleNamespace(type="text", text="respuesta final"),
        ]
    )
    _patch_client(monkeypatch, fake_client)

    answer = AnthropicProvider().complete("prompt")

    assert answer == "respuesta final"
