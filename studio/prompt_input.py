"""Multi-line prompt input for the Asistente panel.

A plain QLineEdit can't hold more than one line, so a pasted snippet or a
longer question had nowhere to wrap. PromptTextEdit is a QTextEdit tuned to
behave like a chat input instead: Enter sends, Shift+Enter inserts a
newline, Tab moves focus rather than indenting, and dropping/pasting a file
(from Finder, or a copied file on the clipboard) attaches it instead of
dumping its raw path or binary data into the text.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QTextEdit


class PromptTextEdit(QTextEdit):
    """Emits `submitted` on Enter and `files_attached` when a file is pasted
    or dropped, instead of inserting either into the text body."""

    submitted = Signal()
    files_attached = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setTabChangesFocus(True)
        self.setAcceptDrops(True)
        self.setMinimumHeight(88)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        is_enter = event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
        if is_enter and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            event.accept()
            self.submitted.emit()
            return

        super().keyPressEvent(event)

    def insertFromMimeData(self, source) -> None:
        paths = _local_file_paths(source)
        if paths:
            self.files_attached.emit(paths)
            return

        super().insertFromMimeData(source)

    def dropEvent(self, event) -> None:
        paths = _local_file_paths(event.mimeData())
        if paths:
            event.acceptProposedAction()
            self.files_attached.emit(paths)
            return

        super().dropEvent(event)


def _local_file_paths(mime_data) -> list[str]:
    if not mime_data.hasUrls():
        return []
    return [url.toLocalFile() for url in mime_data.urls() if url.isLocalFile()]
