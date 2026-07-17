"""Main window for BoardComposer Studio."""

import dataclasses
import uuid

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent

from PySide6.QtWidgets import (
    QDialog,
    QDockWidget,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from studio.dialogs import BoardDialog, MoveToBoardDialog, PieceDialog
from studio.models import (
    StudioBoard,
    StudioPiece,
    StudioPlacement,
    StudioProject,
)
from studio.panels import (
    render_board,
    render_chat,
    render_comparison,
    render_empty,
    render_piece,
    render_project,
)
from studio.export import export_project_to_pdf, export_project_to_svg
from studio.panel_plugins import discover_panel_plugins
from studio.project import load_project_from_file, save_project_to_file
from studio.workspace.board_workspace import BoardWorkspace
from studio.commands import (
    AddBoardCommand,
    AddPieceCommand,
    DeletePieceCommand,
    EditBoardCommand,
    EditPieceCommand,
    MoveToBoardCommand,
    RotatePieceCommand,
)

RESERVED_PANEL_NAMES = {"Explorer", "Inspector", "Timeline", "Comparador", "Asistente"}

PROJECT_FILE_FILTER = "BoardComposer Studio (*.bcstudio.json)"


def _generate_ids(
    base_id: str, quantity: int, existing_ids: frozenset[str]
) -> list[str]:
    """Returns `quantity` unique ids starting with `base_id` — the first one
    unchanged, the rest suffixed (`base_id-2`, `base_id-3`, ...) so a single
    dialog submission can create several identical boards/pieces at once."""
    ids = [base_id]
    suffix = 2
    while len(ids) < quantity:
        candidate = f"{base_id}-{suffix}"
        suffix += 1
        if candidate in existing_ids or candidate in ids:
            continue
        ids.append(candidate)
    return ids


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

        self._actions["add_board"] = QAction("Añadir tablero…", self)
        menus["Proyecto"].addAction(self._actions["add_board"])
        self._actions["add_board"].triggered.connect(self._add_board)
        self._actions["edit_board"] = QAction("Editar tablero…", self)
        menus["Proyecto"].addAction(self._actions["edit_board"])
        self._actions["edit_board"].triggered.connect(self._edit_board)

        menus["Proyecto"].addSeparator()
        self._actions["add_piece"] = QAction("Añadir pieza…", self)
        menus["Proyecto"].addAction(self._actions["add_piece"])
        self._actions["add_piece"].triggered.connect(self._add_piece)
        self._actions["edit_piece"] = QAction("Editar pieza…", self)
        menus["Proyecto"].addAction(self._actions["edit_piece"])
        self._actions["edit_piece"].triggered.connect(self._edit_piece)
        self._actions["move_piece_to_board"] = QAction("Mover a tablero…", self)
        menus["Proyecto"].addAction(self._actions["move_piece_to_board"])
        self._actions["move_piece_to_board"].triggered.connect(
            self._move_piece_to_board
        )

        self._actions["solve_layout"] = QAction("Calcular layout", self)
        menus["Herramientas"].addAction(self._actions["solve_layout"])
        self._actions["solve_layout"].triggered.connect(self._solve_layout)

        self._actions["apply_layout"] = QAction("Aplicar layout calculado", self)
        menus["Herramientas"].addAction(self._actions["apply_layout"])
        self._actions["apply_layout"].triggered.connect(self._apply_layout)

        self._actions["compare_solutions"] = QAction("Generar comparación", self)
        menus["Comparar"].addAction(self._actions["compare_solutions"])
        self._actions["compare_solutions"].triggered.connect(self._compare_solutions)

        menus["Comparar"].addSeparator()

        self._comparison_actions = []
        for index in range(4):
            action = QAction(f"Aplicar solución {index + 1}", self)
            menus["Comparar"].addAction(action)
            action.triggered.connect(
                lambda checked=False, i=index: self._apply_comparison_solution(i)
            )
            self._comparison_actions.append(action)

        self._actions["export_svg"] = QAction("Exportar SVG…", self)
        menus["Exportar"].addAction(self._actions["export_svg"])
        self._actions["export_svg"].triggered.connect(self._export_svg)

        self._actions["export_pdf"] = QAction("Exportar PDF…", self)
        menus["Exportar"].addAction(self._actions["export_pdf"])
        self._actions["export_pdf"].triggered.connect(self._export_pdf)

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
        self._actions["open"].triggered.connect(self._open_project)
        self._actions["save"].triggered.connect(self._save_project)

        self._menus = menus

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
        self._menus["Ver"].addAction(explorer_dock.toggleViewAction())

        self.inspector = QTextEdit()
        self.inspector.setReadOnly(True)
        self.inspector.setHtml(render_empty())

        inspector_dock = QDockWidget("Inspector", self)
        inspector_dock.setWidget(self.inspector)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            inspector_dock,
        )
        self._menus["Ver"].addAction(inspector_dock.toggleViewAction())

        console = QTextEdit()
        console.setReadOnly(True)
        console.setText("Timeline / Consola / Eventos")

        console_dock = QDockWidget("Timeline", self)
        console_dock.setWidget(console)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            console_dock,
        )
        self._menus["Ver"].addAction(console_dock.toggleViewAction())

        self.comparator = QTextEdit()
        self.comparator.setReadOnly(True)
        self.comparator.setHtml(render_comparison([]))

        comparator_dock = QDockWidget("Comparador", self)
        comparator_dock.setWidget(self.comparator)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            comparator_dock,
        )
        self.tabifyDockWidget(console_dock, comparator_dock)
        self._menus["Ver"].addAction(comparator_dock.toggleViewAction())

        self.assistant_history = QTextEdit()
        self.assistant_history.setReadOnly(True)
        self.assistant_history.setHtml(render_chat([]))

        self.assistant_input = QLineEdit()
        self.assistant_input.setPlaceholderText("Pregunta al asistente…")
        self.assistant_input.returnPressed.connect(self._ask_assistant)

        assistant_widget = QWidget()
        assistant_layout = QVBoxLayout(assistant_widget)
        assistant_layout.setContentsMargins(0, 0, 0, 0)
        assistant_layout.addWidget(self.assistant_history)
        assistant_layout.addWidget(self.assistant_input)

        assistant_dock = QDockWidget("Asistente", self)
        assistant_dock.setWidget(assistant_widget)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            assistant_dock,
        )
        self.tabifyDockWidget(inspector_dock, assistant_dock)
        self._menus["Ver"].addAction(assistant_dock.toggleViewAction())

        self._build_plugin_panels()

    def _build_plugin_panels(self):
        """Añade un QDockWidget por cada panel registrado por un plugin
        (IDE-0008 Fase E), con su acción de mostrar/ocultar en el menú
        "Ver". Un plugin roto (al cargarse o al construir su widget) no
        impide que arranque el resto de Studio."""
        plugins, errors = discover_panel_plugins()

        for error in errors:
            self.statusBar().showMessage(
                f"Plugin de panel '{error.name}' no se pudo cargar: {error.error}",
                5000,
            )

        for name, factory in plugins.items():
            if name in RESERVED_PANEL_NAMES:
                self.statusBar().showMessage(
                    f"El plugin de panel '{name}' usa un nombre reservado y "
                    "se ha ignorado.",
                    5000,
                )
                continue

            try:
                widget = factory(self.services)
            except Exception as error:  # noqa: BLE001 - código de terceros
                self.statusBar().showMessage(
                    f"El plugin de panel '{name}' falló al construirse: {error}",
                    5000,
                )
                continue

            dock = QDockWidget(name, self)
            dock.setWidget(widget)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
            self._menus["Ver"].addAction(dock.toggleViewAction())

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
                StudioPlacement("P-001", 120, 120, board_id="TAB-001"),
                StudioPlacement("P-002", 900, 120, board_id="TAB-001"),
                StudioPlacement("P-003", 1500, 120, board_id="TAB-001"),
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
        root.setData(0, Qt.ItemDataRole.UserRole, f"project:{project.project_id}")
        boards_root = QTreeWidgetItem(["Tableros"])
        pieces_root = QTreeWidgetItem(["Piezas"])

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
        self.explorer.addTopLevelItem(root)
        self.explorer.expandAll()

    def _on_explorer_selection_changed(self):
        selected = self.explorer.selectedItems()

        if not selected:
            self.inspector.setHtml(render_empty())
            return

        item = selected[0]
        data = item.data(0, Qt.ItemDataRole.UserRole)
        project = self.services.projects.current_project

        if project is None or data is None:
            self.inspector.setHtml(f"<h3>Inspector</h3><p>{item.text(0)}</p>")
            return

        kind, object_id = data.split(":", 1)

        if kind == "project":
            self.inspector.setHtml(render_project(project))
            return

        if kind == "board":
            board = next(
                board for board in project.boards if board.board_id == object_id
            )
            pieces_by_id = {piece.piece_id: piece for piece in project.pieces}
            board_placements = [
                placement
                for placement in project.placements
                if placement.board_id == object_id
            ]
            self.inspector.setHtml(render_board(board, board_placements, pieces_by_id))
            self.workspace.set_active_board(object_id)
            return

        if kind == "piece":
            self.services.selection.select_one(object_id)
            self.workspace.select_piece(object_id)

    def _new_project(self):
        project = StudioProject(
            project_id=str(uuid.uuid4()),
            name="Nuevo proyecto",
        )

        self.services.projects.new_project(project)
        self.workspace.reload_project()
        self._reload_explorer()
        self.statusBar().showMessage("Nuevo proyecto creado", 3000)
        self._update_window_title()

    def _open_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Abrir proyecto", "", PROJECT_FILE_FILTER
        )

        if not path:
            return

        try:
            project = load_project_from_file(path)
        except (OSError, ValueError, KeyError) as error:
            self.statusBar().showMessage(f"No se pudo abrir el proyecto: {error}", 5000)
            return

        self.services.projects.open_project(project, filename=path)
        self.workspace.reload_project()
        self.workspace.selection.clear()
        self.workspace.selection.sync_inspector(self)
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()
        self.statusBar().showMessage(f"Proyecto abierto: {path}", 3000)

    def _save_project(self):
        project = self.services.projects.current_project

        if project is None:
            return

        path = self.services.projects.filename

        if path is None:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar proyecto",
                f"{project.name}.bcstudio.json",
                PROJECT_FILE_FILTER,
            )

            if not path:
                return

        try:
            save_project_to_file(project, path)
        except OSError as error:
            self.statusBar().showMessage(
                f"No se pudo guardar el proyecto: {error}", 5000
            )
            return

        self.services.projects.mark_saved(path)
        self._update_window_title()
        self.statusBar().showMessage(f"Proyecto guardado: {path}", 3000)

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.services.projects.is_modified:
            event.accept()
            return

        project = self.services.projects.current_project
        name = project.name if project is not None else "el proyecto"

        choice = QMessageBox.question(
            self,
            "Cambios sin guardar",
            f'"{name}" tiene cambios sin guardar. ¿Quieres guardarlos antes de salir?',
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )

        if choice == QMessageBox.StandardButton.Cancel:
            event.ignore()
            return

        if choice == QMessageBox.StandardButton.Save:
            self._save_project()
            if self.services.projects.is_modified:
                # El usuario canceló el diálogo de guardado, o falló: no cerramos.
                event.ignore()
                return

        event.accept()

    def refresh_inspector_for_piece(self, piece_id: str):
        """Refresh inspector panel for the selected piece."""
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)
        placement = project.placement_by_piece_id(piece_id)

        self.inspector.setHtml(render_piece(piece, placement))

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
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()

    def _add_board(self):
        project = self.services.projects.current_project
        if project is None:
            return

        existing_ids = frozenset(board.board_id for board in project.boards)
        dialog = BoardDialog(self, existing_ids=existing_ids)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        board_id, length_mm, width_mm, material, thickness_mm = dialog.values()
        if not board_id:
            self.statusBar().showMessage("El tablero necesita un id.", 5000)
            return

        if any(board.board_id == board_id for board in project.boards):
            self.statusBar().showMessage(
                f"Ya existe un tablero con id '{board_id}'.", 5000
            )
            return

        board_ids = _generate_ids(board_id, dialog.quantity(), existing_ids)
        for new_board_id in board_ids:
            command = AddBoardCommand(
                self.services,
                StudioBoard(new_board_id, length_mm, width_mm, material, thickness_mm),
            )
            self.services.commands.execute(command)
        self.services.projects.mark_modified()

        self.workspace.set_active_board(board_ids[0])
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()
        if len(board_ids) == 1:
            self.statusBar().showMessage(f"Tablero '{board_id}' añadido.", 3000)
        else:
            self.statusBar().showMessage(
                f"{len(board_ids)} tableros añadidos: {', '.join(board_ids)}.", 4000
            )

    def _edit_board(self):
        project = self.services.projects.current_project
        active_board_id = self.workspace.active_board_id
        if project is None or active_board_id is None:
            self.statusBar().showMessage("No hay ningún tablero que editar.", 5000)
            return

        old_board = next(
            (board for board in project.boards if board.board_id == active_board_id),
            None,
        )
        if old_board is None:
            return

        dialog = BoardDialog(
            self,
            board_id=old_board.board_id,
            length_mm=old_board.length_mm,
            width_mm=old_board.width_mm,
            material=old_board.material,
            thickness_mm=old_board.thickness_mm,
            id_editable=False,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        _, length_mm, width_mm, material, thickness_mm = dialog.values()
        new_board = dataclasses.replace(
            old_board,
            length_mm=length_mm,
            width_mm=width_mm,
            material=material,
            thickness_mm=thickness_mm,
        )

        command = EditBoardCommand(self.services, old_board, new_board)
        self.services.commands.execute(command)
        self.services.projects.mark_modified()

        self.workspace.reload_project()
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()
        self.statusBar().showMessage(
            f"Tablero '{new_board.board_id}' actualizado.", 3000
        )

    def _add_piece(self):
        project = self.services.projects.current_project
        active_board_id = self.workspace.active_board_id
        if project is None or active_board_id is None:
            self.statusBar().showMessage("Añade primero un tablero.", 5000)
            return

        existing_ids = frozenset(piece.piece_id for piece in project.pieces)
        dialog = PieceDialog(self, existing_ids=existing_ids)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        piece_id, length_mm, width_mm, material, thickness_mm = dialog.values()
        if not piece_id:
            self.statusBar().showMessage("La pieza necesita un id.", 5000)
            return

        if any(piece.piece_id == piece_id for piece in project.pieces):
            self.statusBar().showMessage(
                f"Ya existe una pieza con id '{piece_id}'.", 5000
            )
            return

        piece_ids = _generate_ids(piece_id, dialog.quantity(), existing_ids)
        for new_piece_id in piece_ids:
            piece = StudioPiece(
                new_piece_id, length_mm, width_mm, material, thickness_mm
            )
            placement = StudioPlacement(new_piece_id, 0, 0, board_id=active_board_id)
            command = AddPieceCommand(self.services, piece, placement)
            self.services.commands.execute(command)
        self.services.projects.mark_modified()

        self.workspace.reload_project()
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()
        if len(piece_ids) == 1:
            self.statusBar().showMessage(f"Pieza '{piece_id}' añadida.", 3000)
        else:
            self.statusBar().showMessage(
                f"{len(piece_ids)} piezas añadidas: {', '.join(piece_ids)}.", 4000
            )

    def _edit_piece(self):
        project = self.services.projects.current_project
        piece_id = self.workspace.selection.current()
        if project is None or piece_id is None:
            self.statusBar().showMessage("Selecciona una pieza primero.", 5000)
            return

        old_piece = next(
            (piece for piece in project.pieces if piece.piece_id == piece_id),
            None,
        )
        if old_piece is None:
            return

        dialog = PieceDialog(
            self,
            piece_id=old_piece.piece_id,
            length_mm=old_piece.length_mm,
            width_mm=old_piece.width_mm,
            material=old_piece.material,
            thickness_mm=old_piece.thickness_mm,
            id_editable=False,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        _, length_mm, width_mm, material, thickness_mm = dialog.values()
        new_piece = dataclasses.replace(
            old_piece,
            length_mm=length_mm,
            width_mm=width_mm,
            material=material,
            thickness_mm=thickness_mm,
        )

        command = EditPieceCommand(self.services, old_piece, new_piece)
        self.services.commands.execute(command)
        self.services.projects.mark_modified()

        self.workspace.reload_project()
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()
        self.statusBar().showMessage(f"Pieza '{new_piece.piece_id}' actualizada.", 3000)

    def _move_piece_to_board(self):
        project = self.services.projects.current_project
        piece_id = self.workspace.selection.current()
        if project is None or piece_id is None:
            self.statusBar().showMessage("Selecciona una pieza primero.", 5000)
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is None:
            self.statusBar().showMessage("Esa pieza no tiene una colocación.", 5000)
            return

        other_board_ids = [
            board.board_id
            for board in project.boards
            if board.board_id != placement.board_id
        ]
        if not other_board_ids:
            self.statusBar().showMessage(
                "No hay otro tablero al que mover la pieza.", 5000
            )
            return

        dialog = MoveToBoardDialog(self, board_ids=other_board_ids)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        new_board_id = dialog.selected_board_id()
        command = MoveToBoardCommand(
            self.services, piece_id, placement.board_id, new_board_id
        )
        self.services.commands.execute(command)
        self.services.projects.mark_modified()

        self.workspace.reload_project()
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()
        self.statusBar().showMessage(
            f"Pieza '{piece_id}' movida al tablero '{new_board_id}'.", 3000
        )

    def _solve_layout(self):
        solution = self.services.layout.solve_current_project(
            self.workspace.active_board_id
        )

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

    def _unplaced_piece_ids(self) -> list[str]:
        project = self.services.projects.current_project
        if project is None:
            return []

        return [
            piece.piece_id
            for piece in project.pieces
            if project.placement_by_piece_id(piece.piece_id) is None
        ]

    def _apply_layout(self):
        if not self.services.layout.apply_last_solution_to_current_project(
            self.workspace.active_board_id
        ):
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        self.workspace.reload_project()
        self.workspace.reload_project()
        self.services.selection.clear()
        self._reload_explorer()
        self._update_undo_redo()
        self._update_window_title()

        unplaced = self._unplaced_piece_ids()
        if unplaced:
            self.statusBar().showMessage(
                f"Layout aplicado — {len(unplaced)} pieza(s) sin colocar: "
                f"{', '.join(unplaced)}",
                6000,
            )
        else:
            self.statusBar().showMessage("Layout aplicado al proyecto", 3000)

    def _compare_solutions(self):
        solutions = self.services.layout.compare_solutions(
            self.workspace.active_board_id
        )
        self.comparator.setHtml(render_comparison(solutions))

        if not solutions:
            self.statusBar().showMessage(
                "No se pudieron generar soluciones para comparar", 3000
            )
            return

        self.statusBar().showMessage(
            f"{len(solutions)} solución(es) generada(s) para comparar", 3000
        )

    def _apply_comparison_solution(self, index: int):
        if not self.services.layout.apply_comparison_solution(
            index, self.workspace.active_board_id
        ):
            self.statusBar().showMessage(
                "No hay una solución generada en esa posición", 3000
            )
            return

        self.workspace.reload_project()
        self.workspace.selection.clear()
        self.workspace.selection.sync_inspector(self)
        self._reload_explorer()
        self._update_window_title()
        self._update_undo_redo()

        unplaced = self._unplaced_piece_ids()
        if unplaced:
            self.statusBar().showMessage(
                f"Solución {index + 1} aplicada — {len(unplaced)} pieza(s) sin "
                f"colocar: {', '.join(unplaced)}",
                6000,
            )
        else:
            self.statusBar().showMessage(f"Solución {index + 1} aplicada", 3000)

    def _ask_assistant(self):
        question = self.assistant_input.text()
        if not question.strip():
            return

        self.services.assistant.ask(question)
        self.assistant_history.setHtml(render_chat(self.services.assistant.history))
        self.assistant_input.clear()

    def _export_svg(self):
        project = self.services.projects.current_project
        if project is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar SVG", f"{project.name}.svg", "SVG (*.svg)"
        )
        if not path:
            return

        if not export_project_to_svg(project, path):
            self.statusBar().showMessage(
                "El proyecto no tiene piezas colocadas que exportar", 3000
            )
            return

        self.statusBar().showMessage(f"SVG exportado: {path}", 3000)

    def _export_pdf(self):
        project = self.services.projects.current_project
        if project is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar PDF", f"{project.name}.pdf", "PDF (*.pdf)"
        )
        if not path:
            return

        if not export_project_to_pdf(project, path):
            self.statusBar().showMessage(
                "El proyecto no tiene piezas colocadas que exportar", 3000
            )
            return

        self.statusBar().showMessage(f"PDF exportado: {path}", 3000)
