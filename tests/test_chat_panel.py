from studio.panels.chat_panel import render_chat


def test_render_chat_with_no_history_explains_how_to_start():
    html = render_chat([])

    assert "Asistente" in html
    assert "Escribe una pregunta" in html


def test_render_chat_shows_questions_and_answers():
    html = render_chat([("¿cómo exporto?", "Usa el menú Exportar.")])

    assert "¿cómo exporto?" in html
    assert "Usa el menú Exportar." in html


def test_render_chat_shows_entries_in_order():
    html = render_chat([("primera", "respuesta 1"), ("segunda", "respuesta 2")])

    assert html.index("primera") < html.index("segunda")
    assert html.index("respuesta 1") < html.index("segunda")


def test_render_chat_escapes_html_in_free_text():
    html = render_chat([("<script>alert(1)</script>", "<b>ok</b>")])

    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;ok&lt;/b&gt;" in html
