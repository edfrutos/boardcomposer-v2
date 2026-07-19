from __future__ import annotations

from boardcomposer.ai import AIProvider, default_provider

PROMPT_TEMPLATE = (
    "Eres el asistente de ayuda de BoardComposer Studio. Responde en "
    "español, de forma breve y concreta, a la pregunta del usuario. Usa "
    "el contexto del proyecto actual si es relevante para la pregunta; "
    "si no lo es, ignóralo.\n\n"
    "Contexto del proyecto actual:\n{context}\n\n"
    "Pregunta del usuario:\n{question}\n"
)


class AssistantService:
    """Bridge between BoardComposer Studio and the Core's AI capabilities
    (IDE-0007 Fase E). Same role as LayoutService for the solver: the only
    place in Studio that talks to boardcomposer.ai."""

    def __init__(self, services, provider: AIProvider | None = None):
        self.services = services
        self.provider = provider or default_provider()
        self.history: list[tuple[str, str]] = []

    def ask(self, question: str) -> str:
        question = question.strip()
        if not question:
            return ""

        prompt = PROMPT_TEMPLATE.format(
            context=self._project_context(),
            question=question,
        )
        try:
            answer = self.provider.complete(prompt)
        except Exception as error:
            # A real AIProvider (AnthropicProvider) is a network call — an
            # invalid API key, rate limit, or connection failure shouldn't
            # crash Studio or silently do nothing; show it in the chat like
            # any other answer.
            answer = f"No se pudo obtener respuesta del proveedor de IA: {error}"
        self.history.append((question, answer))
        return answer

    def _project_context(self) -> str:
        project = self.services.projects.current_project
        if project is None:
            return "No hay ningún proyecto abierto."

        return (
            f"Proyecto: {project.name}\n"
            f"Tableros: {len(project.boards)}\n"
            f"Piezas: {len(project.pieces)}\n"
            f"Piezas colocadas: {len(project.placements)}"
        )
