"""Project manager for BoardComposer Studio."""

from dataclasses import dataclass

from studio.models import StudioProject


@dataclass
class ProjectManager:
    """Owns the currently opened Studio project."""

    _project: StudioProject | None = None
    _modified: bool = False
    _filename: str | None = None

    @property
    def current_project(self) -> StudioProject | None:
        return self._project

    @property
    def has_project(self) -> bool:
        return self._project is not None

    @property
    def is_modified(self) -> bool:
        return self._modified

    @property
    def filename(self) -> str | None:
        return self._filename

    def new_project(self, project: StudioProject) -> None:
        self._project = project
        self._filename = None
        self._modified = True

    def open_project(
        self,
        project: StudioProject,
        filename: str | None = None,
    ) -> None:
        self._project = project
        self._filename = filename
        self._modified = False

    def mark_modified(self) -> None:
        self._modified = True

    def mark_saved(self, filename: str | None = None) -> None:
        if filename is not None:
            self._filename = filename
        self._modified = False

    def close_project(self) -> None:
        self._project = None
        self._filename = None
        self._modified = False
