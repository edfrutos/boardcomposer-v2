"""Command manager for undo/redo."""

from dataclasses import dataclass, field

from studio.commands.command import Command


@dataclass
class CommandManager:
    """Stores undo and redo stacks."""

    undo_stack: list[Command] = field(default_factory=list)
    redo_stack: list[Command] = field(default_factory=list)

    def execute(self, command: Command) -> None:
        command.redo()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> None:
        if not self.undo_stack:
            return

        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self) -> None:
        if not self.redo_stack:
            return

        command = self.redo_stack.pop()
        command.redo()
        self.undo_stack.append(command)

    def can_undo(self) -> bool:
        return bool(self.undo_stack)

    def can_redo(self) -> bool:
        return bool(self.redo_stack)
