"""Application services for BoardComposer Studio."""

from dataclasses import dataclass, field

from studio.commands import CommandManager
from studio.events import EventBus
from studio.project import ProjectManager
from studio.selection import SelectionManager
from studio.layout_service import LayoutService


@dataclass
class StudioServices:
    """Container for shared Studio services."""

    events: EventBus = field(default_factory=EventBus)
    projects: ProjectManager = field(default_factory=ProjectManager)
    selection: SelectionManager = field(default_factory=SelectionManager)
    commands: CommandManager = field(default_factory=CommandManager)

    def __post_init__(self):
        self.layout = LayoutService(self)
