"""Content builder for the Asistente (chat) panel (IDE-0007 Fase E).

Pure function, no Qt dependency, so it's unit-testable — same pattern as
comparator_panel.py. Escapes question/answer text before embedding it in
HTML: unlike the other panels, this content includes free text typed by
the user and returned by the AI provider, not just internally generated
solver strings.
"""


def render_chat(history: list[tuple[str, str]]) -> str:
    if not history:
        return (
            "<h3>Asistente</h3>"
            "<p>Escribe una pregunta sobre el proyecto, los resultados o "
            "cómo usar BoardComposer Studio.</p>"
        )

    entries = []
    for question, answer in history:
        entries.append(f"<p><b>Tú:</b> {_escape(question)}</p>")
        entries.append(f"<p><b>Asistente:</b> {_escape(answer)}</p>")

    return "<h3>Asistente</h3>" + "".join(entries)


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
