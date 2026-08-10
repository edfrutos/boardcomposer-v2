"""Interactive board workspace for BoardComposer Studio."""

from __future__ import annotations
from studio.workspace.workspace_camera import WorkspaceCamera
from PySide6.QtCore import QPoint, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QMouseEvent, QPainter, QResizeEvent, QWheelEvent
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)
from studio.activity_log import ACTIVITY_EVENT
from studio.commands import MovePieceCommand
from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.drag_controller import DragController
from studio.workspace.grid import add_grid
from studio.workspace.board_item import create_board_item
from studio.workspace.piece_factory import create_piece_item
from studio.workspace.placement_validator import PlacementValidator
from studio.workspace.selection_controller import SelectionController


class BoardWorkspace(QGraphicsView):
    # Right-click on an element (IDE-0040), instead of the panning every
    # other right-click still triggers: MainWindow owns the actual menus
    # (it already owns the equivalent Explorer one), this widget only
    # reports what got clicked and where.
    piece_context_menu_requested = Signal(str, QPoint)
    board_context_menu_requested = Signal(QPoint)

    def __init__(self, services):
        super().__init__()
        self._validator = None

        self.services = services
        self._scene = QGraphicsScene(self)
        self._camera = WorkspaceCamera(center=QPointF(1500, 500))
        self._panning = False
        self._last_pan_point = QPoint()
        self._board_item: QGraphicsRectItem | None = None
        self._piece_items: list[BoardPieceItem] = []
        self._active_board_id: str | None = None
        self.selection = SelectionController(services)
        self._drag = DragController()
        self._drag_start: tuple[str, float, float] | None = None
        # reload_project() calls fit_board() right away, but the dock is
        # usually still at its default construction-time size then — real
        # layout (the window opening, a dock resizing to its docked share
        # of the screen) happens afterwards, leaving the board fit to a
        # size it never actually has, stranded small in a corner with a
        # sea of empty grid around it. Tracks whether a real fit has
        # happened yet for the current board so resizeEvent can catch that
        # first real size without re-fitting (and undoing the user's own
        # zoom/pan) on every later resize.
        self._fitted_once = False

        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    @property
    def active_board_id(self) -> str | None:
        return self._active_board_id

    def set_active_board(self, board_id: str) -> None:
        self._active_board_id = board_id
        self.reload_project()

    def reload_project(self) -> None:
        self._scene.clear()
        self._piece_items.clear()
        self._board_item = None
        self._scene.setSceneRect(QRectF(-5000, -5000, 13000, 11000))
        self._fitted_once = False

        project = self.services.projects.current_project
        if project is not None and project.boards:
            board_ids = {board.board_id for board in project.boards}
            if self._active_board_id not in board_ids:
                self._active_board_id = project.boards[0].board_id
        else:
            self._active_board_id = None

        add_grid(self._scene)
        self._add_board()
        self._add_pieces()
        self.fit_board()

    def _add_board(self) -> None:
        project = self.services.projects.current_project
        if project is None or not project.boards:
            return

        board_model = next(
            (
                board
                for board in project.boards
                if board.board_id == self._active_board_id
            ),
            None,
        )
        if board_model is None:
            return

        board = create_board_item(board_model)

        self._scene.addItem(board)
        self._board_item = board
        self._validator = PlacementValidator(
            QRectF(
                0,
                0,
                board_model.length_mm,
                board_model.width_mm,
            )
        )

        self._camera.center = board.sceneBoundingRect().center()

    def _add_pieces(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        for placement in project.placements:
            if placement.board_id != self._active_board_id:
                continue

            piece = project.piece_by_id(placement.piece_id)
            item = create_piece_item(piece, placement)
            self._scene.addItem(item)
            self._piece_items.append(item)
            self.selection.bind_items(self._piece_items)
            self.selection.bind_items(self._piece_items)

    def constrain_piece_position(
        self, item: BoardPieceItem, new_pos: QPointF
    ) -> QPointF:
        if self._validator is None:
            return new_pos

        project = self.services.projects.current_project
        gap_mm = project.kerf_mm if project is not None else 0.0

        return self._validator.constrain_position(item, new_pos, gap_mm)

    def select_piece(self, piece_id: str) -> None:
        self.selection.select(piece_id)
        self.selection.sync_inspector(self.window())

    def fit_board(self) -> None:
        if self._board_item is None:
            return

        viewport_rect = self.viewport().rect()
        board_rect = self._board_item.sceneBoundingRect()

        if viewport_rect.width() <= 0 or viewport_rect.height() <= 0:
            return

        x_zoom = viewport_rect.width() / board_rect.width()
        y_zoom = viewport_rect.height() / board_rect.height()
        self._camera.zoom = self._camera.clamp_zoom(min(x_zoom, y_zoom) * 0.75)
        self._camera.center = board_rect.center()
        self._apply_camera()
        self._fitted_once = True

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        # Only the size the dock settles into after its first real layout
        # pass — not every resize after that, which would undo a user's own
        # zoom/pan the moment they nudge a splitter (see _fitted_once).
        if not self._fitted_once:
            self.fit_board()

    def wheelEvent(self, event: QWheelEvent) -> None:
        mouse_scene_before = self.mapToScene(event.position().toPoint())
        factor = self._camera.zoom_factor(event.angleDelta().y())
        self._camera.zoom = self._camera.clamp_zoom(self._camera.zoom * factor)
        self._apply_camera()

        mouse_scene_after = self.mapToScene(event.position().toPoint())
        self._camera.center += mouse_scene_before - mouse_scene_after
        self._apply_camera()
        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        clicked_item = self.itemAt(event.position().toPoint())

        if isinstance(clicked_item, BoardPieceItem):
            self._drag.begin(
                clicked_item.piece_id,
                clicked_item.pos().x(),
                clicked_item.pos().y(),
            )

        if event.button() == Qt.MouseButton.RightButton:
            if isinstance(clicked_item, BoardPieceItem):
                self.piece_context_menu_requested.emit(
                    clicked_item.piece_id, event.globalPosition().toPoint()
                )
                event.accept()
                return

            # Geometric containment, not itemAt(): the grid (grid.py) is
            # made of QGraphicsLineItems covering the whole sceneRect(),
            # not just the board, so itemAt() alone can't tell "empty
            # canvas" from "empty patch of board" apart.
            scene_pos = self.mapToScene(event.position().toPoint())
            if (
                self._board_item is not None
                and self._board_item.sceneBoundingRect().contains(scene_pos)
            ):
                self.board_context_menu_requested.emit(event.globalPosition().toPoint())
                event.accept()
                return

            self._start_pan(event.position().toPoint())
            event.accept()
            return

        if clicked_item is None:
            self._start_pan(event.position().toPoint())
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._panning:
            current_position = event.position().toPoint()
            delta = current_position - self._last_pan_point
            self._last_pan_point = current_position

            self._camera.center -= QPointF(
                delta.x() / self._camera.zoom,
                delta.y() / self._camera.zoom,
            )
            self._apply_camera()
            event.accept()
            return

        super().mouseMoveEvent(event)

        selected = self.scene().selectedItems()

        if len(selected) == 1 and isinstance(selected[0], BoardPieceItem):
            item = selected[0]

            if self._validator is not None and not self._validator.can_place(item):
                item.set_invalid()
            else:
                item.set_valid()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._panning:
            self._end_pan()
            event.accept()
            return

        super().mouseReleaseEvent(event)
        self._finish_piece_drag()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.fit_board()
        event.accept()

    def _finish_piece_drag(self) -> None:
        drag = self._drag.clear()
        if drag is None:
            return

        piece_id, old_x, old_y = drag

        item = self.piece_item_by_id(piece_id)
        if item is None:
            return

        if self._validator is not None and not self._validator.can_place(item):
            item.setPos(old_x, old_y)
            item.set_normal()
            return

        project = self.services.projects.current_project
        placement = project.placement_by_piece_id(piece_id) if project else None
        if placement is None:
            return

        if placement.x_mm == old_x and placement.y_mm == old_y:
            return

        command = MovePieceCommand(
            self.services,
            piece_id,
            old_x,
            old_y,
            placement.x_mm,
            placement.y_mm,
        )

        self.services.commands.execute(command)
        self.services.projects.mark_modified()
        # No MainWindow reference to reach _execute()/_log_activity() with —
        # ADR-003's EventBus is exactly for this: publish and let whatever's
        # subscribed (MainWindow._on_activity_event) handle showing it.
        self.services.events.publish(ACTIVITY_EVENT, {"message": command.name})

        window = self.window()

        if hasattr(window, "_update_undo_redo"):
            window._update_undo_redo()

        if hasattr(window, "_update_window_title"):
            window._update_window_title()

        item.set_normal()

    def piece_item_by_id(self, piece_id: str) -> BoardPieceItem | None:
        for item in self._piece_items:
            if item.piece_id == piece_id:
                return item
        return None

    def can_rotate_item(self, item: BoardPieceItem, angle: int) -> bool:
        if self._validator is None:
            return False

        return self._validator.can_rotate(item, angle)

    def _start_pan(self, point: QPoint) -> None:
        self._panning = True
        self._last_pan_point = point
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def _end_pan(self) -> None:
        self._panning = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def _apply_camera(self) -> None:
        self.resetTransform()
        self.scale(self._camera.zoom, self._camera.zoom)
        self.centerOn(self._camera.center)

    def piece_moved(self, piece_id: str, x: float, y: float) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is not None:
            placement.x_mm = x
            placement.y_mm = y

        self.selection.select(piece_id)

        window = self.window()
        self.selection.sync_inspector(window)

        self.viewport().update()
