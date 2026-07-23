"""Tests for the MainWindow side of the Asistente file attachment (S750).

The widget-level paste/drop behavior lives in test_prompt_input.py; this
covers what MainWindow does once a file is chosen — the attachment chip
appears/disappears, only the first of several dropped files is kept, and a
readable text file is inlined into the question sent to the assistant while
a binary/unknown one is flagged as unreadable instead.

`isHidden()` (not `isVisible()`) is used throughout: the window is never
shown in a headless test, so effective visibility is always False, but
`isHidden()` still reflects the explicit setVisible() calls under test.
"""

import pytest
from PySide6.QtWidgets import QApplication, QFileDialog

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_choose_attachment_shows_chip_and_stores_path(window, monkeypatch):
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda *a, **k: ("/tmp/piezas.csv", "")
    )

    window._choose_assistant_attachment()

    assert window._assistant_attachment_path == "/tmp/piezas.csv"
    assert not window.assistant_attachment_chip.isHidden()
    assert not window.assistant_attachment_clear.isHidden()
    assert "piezas.csv" in window.assistant_attachment_chip.text()


def test_choose_attachment_cancelled_keeps_no_attachment(window, monkeypatch):
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *a, **k: ("", ""))

    window._choose_assistant_attachment()

    assert window._assistant_attachment_path is None
    assert window.assistant_attachment_chip.isHidden()


def test_attach_files_keeps_only_the_first(window):
    window._attach_assistant_files(["/tmp/a.csv", "/tmp/b.csv"])

    assert window._assistant_attachment_path == "/tmp/a.csv"


def test_attach_empty_list_is_a_noop(window):
    window._attach_assistant_files([])

    assert window._assistant_attachment_path is None
    assert window.assistant_attachment_chip.isHidden()


def test_clear_attachment_hides_chip_and_drops_path(window):
    window._set_assistant_attachment("/tmp/x.csv")
    assert not window.assistant_attachment_chip.isHidden()

    window._clear_assistant_attachment()

    assert window._assistant_attachment_path is None
    assert window.assistant_attachment_chip.isHidden()
    assert window.assistant_attachment_clear.isHidden()


def test_question_inlines_a_readable_text_file(window, tmp_path):
    attachment = tmp_path / "piezas.csv"
    attachment.write_text("id,largo\nA,100\n", encoding="utf-8")
    window._set_assistant_attachment(str(attachment))

    question = window._question_with_assistant_attachment("¿cuántas piezas?")

    assert "[Archivo adjunto: piezas.csv]" in question
    assert "id,largo" in question


def test_question_flags_an_unreadable_binary_attachment(window, tmp_path):
    attachment = tmp_path / "logo.png"
    attachment.write_bytes(b"\x89PNG\r\n")
    window._set_assistant_attachment(str(attachment))

    question = window._question_with_assistant_attachment("¿qué es esto?")

    assert "contenido no legible como texto" in question
    assert "logo.png" in question
