"""Base command protocol for Studio undo/redo."""

from typing import Protocol


class Command(Protocol):
    """Undoable command."""

    name: str

    def redo(self) -> None:
        """Apply command."""

    def undo(self) -> None:
        """Revert command."""
