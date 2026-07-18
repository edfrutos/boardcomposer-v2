import pytest
from PySide6.QtCore import Qt, QMimeData, QUrl
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from studio.prompt_input import PromptTextEdit


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def prompt_input(app):
    return PromptTextEdit()


def _key_event(key, modifiers=Qt.KeyboardModifier.NoModifier):
    return QKeyEvent(QKeyEvent.Type.KeyPress, key, modifiers)


def test_enter_without_shift_emits_submitted_and_inserts_no_newline(prompt_input):
    prompt_input.setPlainText("hola")
    received = []
    prompt_input.submitted.connect(lambda: received.append(True))

    prompt_input.keyPressEvent(_key_event(Qt.Key.Key_Return))

    assert received == [True]
    assert prompt_input.toPlainText() == "hola"


def test_shift_enter_inserts_a_newline_and_does_not_submit(prompt_input):
    prompt_input.setPlainText("hola")
    prompt_input.moveCursor(prompt_input.textCursor().MoveOperation.End)
    received = []
    prompt_input.submitted.connect(lambda: received.append(True))

    prompt_input.keyPressEvent(
        _key_event(Qt.Key.Key_Return, Qt.KeyboardModifier.ShiftModifier)
    )

    assert received == []
    assert prompt_input.toPlainText() == "hola\n"


def test_has_a_comfortable_minimum_height(prompt_input):
    assert prompt_input.minimumHeight() >= 64


def test_pasting_a_file_url_emits_files_attached_instead_of_inserting_text(
    prompt_input,
):
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile("/tmp/example.txt")])
    received = []
    prompt_input.files_attached.connect(received.append)

    prompt_input.insertFromMimeData(mime)

    assert received == [["/tmp/example.txt"]]
    assert prompt_input.toPlainText() == ""


def test_pasting_plain_text_still_inserts_it(prompt_input):
    mime = QMimeData()
    mime.setText("hola mundo")

    prompt_input.insertFromMimeData(mime)

    assert prompt_input.toPlainText() == "hola mundo"
