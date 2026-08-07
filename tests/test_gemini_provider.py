from types import SimpleNamespace

from boardcomposer.ai.gemini_provider import DEFAULT_MODEL, GeminiProvider


class _FakeModels:
    def __init__(self, response_text):
        self.response_text = response_text
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(text=self.response_text)


class _FakeClient:
    def __init__(self, response_text="respuesta de prueba"):
        self.models = _FakeModels(response_text)


def _patch_client(monkeypatch, fake_client):
    monkeypatch.setattr(
        "boardcomposer.ai.gemini_provider.genai",
        SimpleNamespace(Client=lambda: fake_client),
    )


def test_complete_returns_the_response_text(monkeypatch):
    fake_client = _FakeClient(response_text="hola desde Gemini")
    _patch_client(monkeypatch, fake_client)

    answer = GeminiProvider().complete("una pregunta")

    assert answer == "hola desde Gemini"


def test_complete_sends_the_prompt_as_contents(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    GeminiProvider().complete("¿cuántas piezas caben?")

    call = fake_client.models.calls[0]
    assert call["contents"] == "¿cuántas piezas caben?"


def test_complete_uses_the_default_model_by_default(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    GeminiProvider().complete("prompt")

    assert fake_client.models.calls[0]["model"] == DEFAULT_MODEL


def test_a_custom_model_can_be_configured(monkeypatch):
    fake_client = _FakeClient()
    _patch_client(monkeypatch, fake_client)

    GeminiProvider(model="gemini-2.5-pro").complete("prompt")

    assert fake_client.models.calls[0]["model"] == "gemini-2.5-pro"


def test_complete_handles_an_empty_response(monkeypatch):
    fake_client = _FakeClient(response_text=None)
    _patch_client(monkeypatch, fake_client)

    assert GeminiProvider().complete("prompt") == ""
