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


def test_undo_returns_the_command_it_reverted():
    # Callers that want to log/announce what happened used to reach into
    # redo_stack[-1] after calling undo() with no other way to know which
    # command it was — undo() just returning it removes the need to know
    # the stacks exist at all.
    services = _services_with_project()
    manager = CommandManager()
    command = AddBoardCommand(services, StudioBoard("B1", 2000, 300))
    manager.execute(command)

    assert manager.undo() is command


def test_undo_on_an_empty_stack_returns_none():
    manager = CommandManager()

    assert manager.undo() is None


def test_redo_returns_the_command_it_reapplied():
    services = _services_with_project()
    manager = CommandManager()
    command = AddBoardCommand(services, StudioBoard("B1", 2000, 300))
    manager.execute(command)
    manager.undo()

    assert manager.redo() is command


def test_redo_on_an_empty_stack_returns_none():
    manager = CommandManager()

    assert manager.redo() is None
