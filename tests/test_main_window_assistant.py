import pytest
from PySide6.QtWidgets import QApplication

from boardcomposer.ai import MockAIProvider
from studio.main_window import MainWindow
from studio.prompt_input import PromptTextEdit
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    win = MainWindow(services=StudioServices())
    win.services.assistant.provider = MockAIProvider(response="ok")
    return win


def test_assistant_input_is_a_multiline_prompt_edit(window):
    assert isinstance(window.assistant_input, PromptTextEdit)
    assert window.assistant_input.minimumHeight() >= 64


def test_submitting_the_prompt_input_asks_the_assistant(window):
    window.assistant_input.setPlainText("¿cómo exporto?")

    window.assistant_input.submitted.emit()

    assert window.services.assistant.history == [("¿cómo exporto?", "ok")]
    assert window.assistant_input.toPlainText() == ""


def test_choosing_an_attachment_shows_a_chip_and_folds_it_into_the_question(
    window, tmp_path
):
    attached = tmp_path / "notas.txt"
    attached.write_text("contenido de prueba")

    window._attach_assistant_files([str(attached)])

    assert window.assistant_attachment_chip.isHidden() is False
    assert "notas.txt" in window.assistant_attachment_chip.text()

    window.assistant_input.setPlainText("resume esto")
    window._ask_assistant()

    question = window.services.assistant.history[0][0]
    assert "resume esto" in question
    assert "notas.txt" in question
    assert "contenido de prueba" in question
    # The attachment is consumed by sending, so the chip clears afterwards.
    assert window.assistant_attachment_chip.isHidden() is True


def test_attaching_a_non_text_file_references_it_by_name_only(window, tmp_path):
    attached = tmp_path / "logo.png"
    attached.write_bytes(b"\x89PNG\r\n\x1a\n")

    window._attach_assistant_files([str(attached)])
    window.assistant_input.setPlainText("qué es esto")
    window._ask_assistant()

    question = window.services.assistant.history[0][0]
    assert "logo.png" in question
    assert "no legible como texto" in question
