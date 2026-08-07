from boardcomposer.ai import AIProvider, AnthropicProvider, MockAIProvider
from studio.assistant_service import AssistantService
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.services import StudioServices


def _project() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 700, 300)],
    )


def test_ask_returns_the_provider_response():
    services = StudioServices()
    provider = MockAIProvider(response="Puedes exportar desde el menú Exportar.")
    assistant = AssistantService(services, provider=provider)

    answer = assistant.ask("¿Cómo exporto a PDF?")

    assert answer == "Puedes exportar desde el menú Exportar."


def test_ask_records_history():
    services = StudioServices()
    assistant = AssistantService(services, provider=MockAIProvider(response="ok"))

    assistant.ask("primera pregunta")
    assistant.ask("segunda pregunta")

    assert assistant.history == [
        ("primera pregunta", "ok"),
        ("segunda pregunta", "ok"),
    ]


def test_ask_ignores_blank_questions():
    services = StudioServices()
    assistant = AssistantService(services, provider=MockAIProvider())

    answer = assistant.ask("   ")

    assert answer == ""
    assert assistant.history == []


def test_ask_includes_project_context_when_a_project_is_open():
    services = StudioServices()
    services.projects.new_project(_project())
    provider = MockAIProvider()
    assistant = AssistantService(services, provider=provider)

    assistant.ask("¿cuántas piezas tengo?")

    prompt = provider.calls[0]
    assert "Proyecto: Demo" in prompt
    assert "Piezas: 1" in prompt


def test_ask_reports_no_open_project():
    services = StudioServices()
    provider = MockAIProvider()
    assistant = AssistantService(services, provider=provider)

    assistant.ask("¿qué es BoardComposer?")

    assert "No hay ningún proyecto abierto" in provider.calls[0]


def test_studio_services_wires_a_default_assistant():
    services = StudioServices()

    assert services.assistant.ask("hola") != ""


class _FailingProvider(AIProvider):
    def complete(self, prompt: str) -> str:
        raise RuntimeError("invalid x-api-key")


def test_ask_reports_a_provider_failure_instead_of_raising():
    services = StudioServices()
    assistant = AssistantService(services, provider=_FailingProvider())

    answer = assistant.ask("¿cómo exporto a PDF?")

    assert "invalid x-api-key" in answer
    assert assistant.history == [("¿cómo exporto a PDF?", answer)]


def test_reload_provider_picks_up_a_newly_set_api_key(monkeypatch):
    # Regression: __init__ only resolves default_provider() once — without
    # reload_provider(), setting an API key in Preferences mid-session
    # would need a restart to take effect.
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    services = StudioServices()
    assistant = AssistantService(services)
    assert isinstance(assistant.provider, MockAIProvider)

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-abc123")
    assistant.reload_provider()

    assert isinstance(assistant.provider, AnthropicProvider)
