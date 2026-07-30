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

    def undo(self) -> Command | None:
        if not self.undo_stack:
            return None

        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        return command

    def redo(self) -> Command | None:
        if not self.redo_stack:
            return None

        command = self.redo_stack.pop()
        command.redo()
        self.undo_stack.append(command)
        return command

    def can_undo(self) -> bool:
        return bool(self.undo_stack)

    def can_redo(self) -> bool:
        return bool(self.redo_stack)

    def clear(self) -> None:
        """Drops both stacks — call whenever the open project changes.

        Commands look up the current project at undo/redo time rather than
        holding their own reference, so a stale command from a previous
        project would otherwise apply to whatever project is open next.
        """
        self.undo_stack.clear()
        self.redo_stack.clear()
