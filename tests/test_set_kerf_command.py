from studio.commands import SetKerfCommand
from studio.models import StudioProject
from studio.services import StudioServices


def _services_with_project() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(StudioProject(project_id="proj-1", name="Demo"))
    return services


def test_set_kerf_command_changes_the_project_kerf():
    services = _services_with_project()
    command = SetKerfCommand(services, 0.0, 3.0)

    command.redo()

    assert services.projects.current_project.kerf_mm == 3.0


def test_set_kerf_command_undo_restores_the_old_kerf():
    services = _services_with_project()
    command = SetKerfCommand(services, 0.0, 3.0)
    command.redo()

    command.undo()

    assert services.projects.current_project.kerf_mm == 0.0
