from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QContextMenuEvent, QMouseEvent
from PySide6.QtWidgets import QApplication

from studio.activity_log import ACTIVITY_EVENT
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices
from studio.workspace.board_workspace import BoardWorkspace


def _services_with_two_boards() -> StudioServices:
    services = StudioServices()
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[
            StudioBoard("B1", 2000, 300),
            StudioBoard("B2", 1500, 400),
        ],
        pieces=[
            StudioPiece("p1", 500, 200),
            StudioPiece("p2", 400, 150),
        ],
        placements=[
            StudioPlacement("p1", 0, 0, board_id="B1"),
            StudioPlacement("p2", 0, 0, board_id="B2"),
        ],
    )
    services.projects.new_project(project)
    return services


def _workspace() -> BoardWorkspace:
    QApplication.instance() or QApplication([])
    return BoardWorkspace(_services_with_two_boards())


def test_reload_project_defaults_the_active_board_to_the_first_one():
    workspace = _workspace()

    workspace.reload_project()

    assert workspace.active_board_id == "B1"


def test_finish_piece_drag_publishes_to_the_activity_event_bus():
    # BoardWorkspace has no MainWindow reference — before this fix, a
    # freehand drag-move (the single most common piece-manipulation
    # gesture) called CommandManager.execute() directly and never reached
    # the Actividad log, unlike every dialog-driven mutation.
    workspace = _workspace()
    workspace.reload_project()

    messages = []
    workspace.services.events.subscribe(
        ACTIVITY_EVENT, lambda name, payload: messages.append(payload["message"])
    )

    item = workspace.piece_item_by_id("p1")
    workspace._drag.begin("p1", 0, 0)
    placement = workspace.services.projects.current_project.placement_by_piece_id("p1")
    placement.x_mm = 300
    placement.y_mm = 50
    item.setPos(300, 50)

    workspace._finish_piece_drag()

    assert messages == ["Pieza movida: p1"]


def test_reload_project_only_renders_pieces_placed_on_the_active_board():
    workspace = _workspace()

    workspace.reload_project()

    assert [item.piece_id for item in workspace._piece_items] == ["p1"]


def test_set_active_board_switches_to_the_other_board_and_its_pieces():
    workspace = _workspace()
    workspace.reload_project()

    workspace.set_active_board("B2")

    assert workspace.active_board_id == "B2"
    assert [item.piece_id for item in workspace._piece_items] == ["p2"]


def test_reload_project_falls_back_to_the_first_board_if_the_active_one_is_gone():
    workspace = _workspace()
    workspace.set_active_board("B2")
    project = workspace.services.projects.current_project
    project.boards = [board for board in project.boards if board.board_id != "B2"]

    workspace.reload_project()

    assert workspace.active_board_id == "B1"


def _right_click(workspace, scene_point):
    """A physical right mouse button press — still handled by
    mousePressEvent() for panning, unchanged by DT-0026."""
    viewport_point = workspace.mapFromScene(scene_point)
    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(viewport_point),
        workspace.mapToGlobal(viewport_point),
        Qt.MouseButton.RightButton,
        Qt.MouseButton.RightButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mousePressEvent(event)


def _request_context_menu(workspace, scene_point):
    """Whatever platform mechanism asks for a context menu — right-click,
    Magic Mouse secondary click, trackpad gesture, the keyboard Menu key —
    Qt normalizes all of it into this one event (DT-0026)."""
    viewport_point = workspace.mapFromScene(scene_point)
    event = QContextMenuEvent(
        QContextMenuEvent.Reason.Mouse,
        viewport_point,
        workspace.mapToGlobal(viewport_point),
    )
    workspace.contextMenuEvent(event)


def test_context_menu_on_a_piece_emits_piece_context_menu_requested():
    workspace = _workspace()
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()

    received = []
    workspace.piece_context_menu_requested.connect(
        lambda piece_id, pos: received.append(piece_id)
    )

    item = workspace.piece_item_by_id("p1")
    _request_context_menu(workspace, item.sceneBoundingRect().center())

    assert received == ["p1"]


def test_context_menu_on_the_board_background_emits_board_context_menu_requested():
    workspace = _workspace()
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()

    received = []
    workspace.board_context_menu_requested.connect(lambda pos: received.append(pos))

    # B1 is 2000x300; p1 (500x200 at 0,0) doesn't reach this point.
    _request_context_menu(workspace, QPointF(1500, 150))

    assert len(received) == 1


def test_context_menu_outside_the_board_requests_nothing():
    workspace = _workspace()
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()

    piece_signals = []
    board_signals = []
    workspace.piece_context_menu_requested.connect(lambda *a: piece_signals.append(a))
    workspace.board_context_menu_requested.connect(lambda *a: board_signals.append(a))

    # Far outside B1's bounds (2000x300) but still inside sceneRect(),
    # where the grid lives — itemAt() alone would see a grid line here.
    _request_context_menu(workspace, QPointF(-4000, -4000))

    assert piece_signals == []
    assert board_signals == []


def test_context_menu_cancels_an_in_progress_pan():
    # A real right mouse button reaches mousePressEvent() (pan starts)
    # *and* contextMenuEvent() for the same click — the menu blocks on
    # exec(), so mouseReleaseEvent() never arrives to end the pan on its
    # own. Left stuck, the next left-click drag would pan the view
    # instead of moving a piece.
    workspace = _workspace()
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()

    item = workspace.piece_item_by_id("p1")
    _right_click(workspace, item.sceneBoundingRect().center())
    assert workspace._panning is True

    _request_context_menu(workspace, item.sceneBoundingRect().center())

    assert workspace._panning is False


def test_right_click_outside_the_board_still_pans():
    workspace = _workspace()
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()

    # Far outside B1's bounds (2000x300) but still inside sceneRect(),
    # where the grid lives — itemAt() alone would see a grid line here.
    _right_click(workspace, QPointF(-4000, -4000))

    assert workspace._panning is True
