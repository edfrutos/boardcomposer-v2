"""Main window for BoardComposer Studio."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
)

from studio.models import (
    StudioBoard,
    StudioPiece,
    StudioPlacement,
    StudioProject,
)
from studio.workspace.board_workspace import BoardWorkspace
from studio.commands import RotatePieceCommand
from studio.commands import DeletePieceCommand


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, services):
        super().__init__()
        self.services = services
        self.setWindowTitle("BoardComposer Studio")
        self.resize(1400, 900)

        self._build_menu()
        self._build_workspace()
        self._build_panels()
        self._build_statusbar()
        self._load_demo_project()

    def _build_menu(self):
        menu = QMenuBar(self)
        self.setMenuBar(menu)

        menus = {}

        for name in (
            "Archivo",
            "Editar",
            "Ver",
            "Proyecto",
            "Generar",
            "Comparar",
            "Exportar",
            "Herramientas",
            "Ayuda",
        ):
            menus[name] = menu.addMenu(name)

        self._actions = {}

        self._actions["new_project"] = QAction("Nuevo proyecto", self)
        self._actions["open"] = QAction("Abrir…", self)
        self._actions["save"] = QAction("Guardar", self)
        self._actions["exit"] = QAction("Salir", self)
        self._actions["undo"] = QAction("Deshacer", self)
        self._actions["redo"] = QAction("Rehacer", self)
        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")

        menus["Editar"].addAction(self._actions["undo"])
        menus["Editar"].addAction(self._actions["redo"])
        self._actions["rotate_piece"] = QAction("Rotar 90°", self)
        self._actions["rotate_piece"].setShortcut("R")
        menus["Editar"].addSeparator()
        menus["Editar"].addAction(self._actions["rotate_piece"])
        self._actions["delete_piece"] = QAction("Eliminar pieza", self)
        self._actions["delete_piece"].setShortcut("Backspace")
        menus["Editar"].addAction(self._actions["delete_piece"])
        self._actions["delete_piece"].triggered.connect(self._delete_selected_piece)
        self._actions["rotate_piece"].triggered.connect(self._rotate_selected_piece)
        self._actions["solve_layout"] = QAction("Calcular layout", self)
        menus["Herramientas"].addAction(self._actions["solve_layout"])
        self._actions["solve_layout"].triggered.connect(self._solve_layout)

        self._actions["apply_layout"] = QAction("Aplicar layout calculado", self)
        menus["Herramientas"].addAction(self._actions["apply_layout"])
        self._actions["apply_layout"].triggered.connect(self._apply_layout)

        self._actions["undo"].triggered.connect(self._undo)
        self._actions["redo"].triggered.connect(self._redo)

        menus["Archivo"].addAction(self._actions["new_project"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["open"])
        menus["Archivo"].addAction(self._actions["save"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["exit"])

        self._actions["exit"].triggered.connect(self.close)
        self._actions["new_project"].triggered.connect(self._new_project)

    def _build_workspace(self):
        self.workspace = BoardWorkspace(self.services)
        self.setCentralWidget(self.workspace)

    def _build_panels(self):
        self.explorer = QTreeWidget()
        self.explorer.setHeaderHidden(True)
        self.explorer.itemSelectionChanged.connect(self._on_explorer_selection_changed)

        explorer_dock = QDockWidget("Explorer", self)
        explorer_dock.setWidget(self.explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, explorer_dock)

        self.inspector = QTextEdit()
        self.inspector.setReadOnly(True)
        self.inspector.setText("Inspector\n\nSin selección")

        inspector_dock = QDockWidget("Inspector", self)
        inspector_dock.setWidget(self.inspector)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            inspector_dock,
        )

        console = QTextEdit()
        console.setReadOnly(True)
        console.setText("Timeline / Consola / Eventos")

        console_dock = QDockWidget("Timeline", self)
        console_dock.setWidget(console)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            console_dock,
        )

    def _build_statusbar(self):
        status = QStatusBar(self)
        status.showMessage("BoardComposer Studio listo")
        self.setStatusBar(status)

    def _load_demo_project(self):
        project = StudioProject(
            project_id="PRJ-DEMO-001",
            name="Proyecto demo",
            boards=[StudioBoard("TAB-001", 3000, 1000)],
            pieces=[
                StudioPiece("P-001", 700, 300),
                StudioPiece("P-002", 520, 360),
                StudioPiece("P-003", 820, 240),
            ],
            placements=[
                StudioPlacement("P-001", 120, 120),
                StudioPlacement("P-002", 900, 120),
                StudioPlacement("P-003", 1500, 120),
            ],
        )

        self.services.projects.new_project(project)
        self.workspace.reload_project()
        self._reload_explorer()
        self._update_window_title()

    def _reload_explorer(self):
        project = self.services.projects.current_project
        self.explorer.clear()

        if project is None:
            return

        root = QTreeWidgetItem([project.name])
        boards_root = QTreeWidgetItem(["Tableros"])
        pieces_root = QTreeWidgetItem(["Piezas"])
        solutions_root = QTreeWidgetItem(["Soluciones"])

        for board in project.boards:
            item = QTreeWidgetItem(
                [f"{board.board_id} — {board.length_mm:g} x {board.width_mm:g} mm"]
            )
            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                f"board:{board.board_id}",
            )
            boards_root.addChild(item)

        for piece in project.pieces:
            item = QTreeWidgetItem(
                [f"{piece.piece_id} — {piece.length_mm:g} x {piece.width_mm:g} mm"]
            )
            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                f"piece:{piece.piece_id}",
            )
            pieces_root.addChild(item)

        root.addChild(boards_root)
        root.addChild(pieces_root)
        root.addChild(solutions_root)
        self.explorer.addTopLevelItem(root)
        self.explorer.expandAll()

    def _on_explorer_selection_changed(self):
        selected = self.explorer.selectedItems()

        if not selected:
            self.inspector.setText("Inspector\n\nSin selección")
            return

        item = selected[0]
        data = item.data(0, Qt.ItemDataRole.UserRole)
        project = self.services.projects.current_project

        if project is None or data is None:
            self.inspector.setText(f"Inspector\n\n{item.text(0)}")
            return

        kind, object_id = data.split(":", 1)

        if kind == "board":
            board = next(
                board for board in project.boards if board.board_id == object_id
            )
            self.inspector.setText(
                "Inspector\n\n"
                f"Tablero: {board.board_id}\n"
                f"Dimensiones: {board.length_mm:g} x {board.width_mm:g} mm\n"
                f"Material: {board.material}"
            )
            return

        if kind == "piece":
            piece = project.piece_by_id(object_id)
            self.services.selection.select_one(object_id)
            self.workspace.select_piece(object_id)
            self.inspector.setText(
                "Inspector\n\n"
                f"Pieza: {piece.piece_id}\n"
                f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
                f"Material: {piece.material}"
            )

    def _new_project(self):
        self._load_demo_project()
        self.statusBar().showMessage("Nuevo proyecto creado", 3000)
        self._update_window_title()

    def refresh_inspector_for_piece(self, piece_id: str):
        """Refresh inspector panel for the selected piece."""
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)
        placement = next(
            placement
            for placement in project.placements
            if placement.piece_id == piece_id
        )

        self.inspector.setText(
            "Inspector\n\n"
            f"Pieza: {piece.piece_id}\n"
            f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
            f"Posición: {placement.x_mm:g}, {placement.y_mm:g} mm\n"
            f"Material: {piece.material}"
        )

    def _update_window_title(self):
        project = self.services.projects.current_project
        marker = "● " if self.services.projects.is_modified else ""

        if project is None:
            self.setWindowTitle("BoardComposer Studio")
            return

        self.setWindowTitle(f"{marker}BoardComposer Studio — {project.name}")

    def _update_undo_redo(self):
        self._actions["undo"].setEnabled(self.services.commands.can_undo())
        self._actions["redo"].setEnabled(self.services.commands.can_redo())

        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")

    def _undo(self):
        self.services.commands.undo()
        self.workspace.reload_project()
        self._update_undo_redo()

    def _redo(self):
        self.services.commands.redo()
        self.workspace.reload_project()
        self._update_undo_redo()

    def _rotate_selected_piece(self):
        selected = self.workspace.scene().selectedItems()
        if not selected:
            return

        piece_id = selected[0].piece_id
        project = self.services.projects.current_project

        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is None:
            return

        old_rotation = placement.rotation
        new_rotation = 90 if old_rotation == 0 else 0

        item = self.workspace.piece_item_by_id(piece_id)
        if item is None:
            return

        if not self.workspace.can_rotate_item(item, new_rotation):
            self.statusBar().showMessage(
                "La pieza no puede rotarse en esa posición",
                3000,
            )
            return

        command = RotatePieceCommand(
            self.services,
            piece_id,
            old_rotation,
            new_rotation,
        )
        self.services.commands.execute(command)

        self.workspace.reload_project()
        self.workspace.select_piece(piece_id)
        self.refresh_inspector_for_piece(piece_id)
        self.services.projects.mark_modified()
        self._update_window_title()
        self._update_undo_redo()

    def _delete_selected_piece(self):
        piece_id = self.workspace.selection.current()
        if piece_id is None:
            return

        command = DeletePieceCommand(self.services, piece_id)
        self.services.commands.execute(command)

        self.workspace.reload_project()
        self.workspace.selection.clear()
        self.workspace.selection.sync_inspector(self)

        self.services.projects.mark_modified()
        self._update_window_title()
        self._update_undo_redo()

    def _solve_layout(self):
        solution = self.services.layout.solve_current_project()

        if solution is None:
            self.statusBar().showMessage("No se pudo calcular layout", 3000)
            return

        self._show_layout_solution(solution)
        self.statusBar().showMessage(
            f"Layout calculado: {len(solution.placements)} piezas",
            3000,
        )

    def _show_layout_solution(self, solution):
        lines = [
            "Layout calculado",
            "",
            f"Piezas colocadas: {len(solution.placements)}",
            f"Largo total: {solution.total_length_mm:.0f} mm",
            f"Ancho total: {solution.total_width_mm:.0f} mm",
            f"Desperdicio: {solution.waste_ratio:.1%}",
        ]

        self.inspector.setText("\n".join(lines))

    def _apply_layout(self):
        if not self.services.layout.apply_last_solution_to_current_project():
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        self.workspace.reload_project()
        self.workspace.reload_project()
        self.services.selection.clear()
        self._reload_explorer()
        self._update_undo_redo()
        self._update_window_title()

        self.statusBar().showMessage("Layout aplicado al proyecto", 3000)
