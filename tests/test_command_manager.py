from studio.commands import AddBoardCommand, CommandManager
from studio.models import StudioBoard, StudioProject
from studio.services import StudioServices


def _services_with_project(project_id="proj-1") -> StudioServices:
    services = StudioServices()
    services.projects.new_project(StudioProject(project_id=project_id, name="Demo"))
    return services


def test_clear_drops_the_undo_stack():
    services = _services_with_project()
    manager = CommandManager()
    manager.execute(AddBoardCommand(services, StudioBoard("B1", 2000, 300)))

    manager.clear()

    assert manager.can_undo() is False
    assert manager.undo_stack == []


def test_clear_drops_the_redo_stack():
    services = _services_with_project()
    manager = CommandManager()
    manager.execute(AddBoardCommand(services, StudioBoard("B1", 2000, 300)))
    manager.undo()

    manager.clear()

    assert manager.can_redo() is False
    assert manager.redo_stack == []


def test_undo_after_clear_does_not_touch_the_new_project():
    # Commands resolve the current project at undo time, so without clear() an
    # undo from the previous project would mutate whatever is open now.
    services = _services_with_project()
    manager = CommandManager()
    manager.execute(AddBoardCommand(services, StudioBoard("B1", 2000, 300)))
    manager.clear()

    services.projects.new_project(StudioProject(project_id="proj-2", name="Otro"))
    services.projects.current_project.boards.append(StudioBoard("B2", 1000, 500))
    manager.undo()

    assert [board.board_id for board in services.projects.current_project.boards] == [
        "B2"
    ]
