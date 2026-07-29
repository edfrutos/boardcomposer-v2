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
            '<table id="empty-state-table"><tr><td id="empty-state">'
            "<h3>Asistente</h3>"
            "<p>Escribe una pregunta sobre el proyecto, los resultados o "
            "cómo usar BoardComposer Studio.</p>"
            "</td></tr></table>"
        )

    entries = []
    for question, answer in history:
        entries.append(f"<p><b>Tú:</b> {_escape(question)}</p>")
        entries.append(f"<p><b>Asistente:</b> {_escape(answer)}</p>")

    return "<h3>Asistente</h3>" + "".join(entries)


def _escape(text: str) -> str:
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # The multi-line prompt input (Shift+Enter) and attached-file content can
    # carry newlines; HTML collapses them, so turn them into <br> to keep
    # multi-line questions and attachments readable in the chat history.
    return escaped.replace("\n", "<br>")
