# BoardComposer Studio — documentación funcional

Cubre `DT-0001` (`docs/masterplan/DOC-006-DeudaTecnica.md`). Complementa a `docs/architecture.md` (estructura de capas) y `docs/masterplan/DOC-007-UX-Studio.md` (pantallas/UX): aquí se documenta **qué hace cada componente** de `studio/` y cómo colaboran en tiempo de ejecución.

## StudioServices — contenedor de servicios

`studio/services.py`. `StudioServices` es el punto único de acceso a los servicios compartidos de Studio; `MainWindow` y el resto de componentes reciben esta instancia en vez de crear sus propias dependencias:

| Servicio | Tipo | Responsabilidad |
|---|---|---|
| `events` | `EventBus` | Bus de eventos síncrono (ver más abajo). |
| `projects` | `ProjectManager` | Ciclo de vida del proyecto abierto. |
| `selection` | `SelectionManager` | Selección activa a nivel de aplicación (un único id). |
| `commands` | `CommandManager` | Pilas de undo/redo. |
| `layout` | `LayoutService` | Puente hacia el Core (ver `docs/architecture.md`). |

`layout` se construye en `__post_init__` porque `LayoutService` necesita la instancia completa de `services` para acceder a `projects`.

## Ciclo de vida del proyecto — `ProjectManager`

`studio/project/project_manager.py`. Guarda el `StudioProject` actualmente abierto (`_project`), si tiene cambios sin guardar (`_modified`) y su ruta de fichero (`_filename`).

- `new_project(project)` — abre un proyecto nuevo, sin fichero asociado, marcado como modificado.
- `open_project(project, filename)` — abre un proyecto existente desde disco, sin marcar como modificado.
- `mark_modified()` / `mark_saved(filename)` — se llaman tras cualquier edición o guardado.
- `close_project()` — vuelve al estado sin proyecto.

`MainWindow._update_window_title()` lee `is_modified` para mostrar el marcador `●` en el título de la ventana.

### Persistencia — `studio/project/project_io.py`

`project_to_dict()`/`project_from_dict()` (serialización pura, sin Qt) convierten un `StudioProject` a/desde un `dict` JSON-compatible (tableros, piezas y colocaciones); `save_project_to_file()`/`load_project_from_file()` son los envoltorios de fichero. Formato: `.bcstudio.json`.

`MainWindow._open_project()`/`_save_project()` conectan esto a los `QAction` "Abrir…"/"Guardar" del menú Archivo (antes creados pero sin conectar — `IDE-0004`): `_save_project()` reutiliza `ProjectManager.filename` si ya existe, o pide ruta con `QFileDialog` la primera vez; `_open_project()` carga el fichero, lo registra vía `ProjectManager.open_project()` y recarga workspace/explorador/inspector.

`MainWindow.closeEvent()` (testeado en `tests/test_main_window_close.py`) impide perder cambios sin guardar al cerrar la ventana: si `ProjectManager.is_modified` es `False` acepta el cierre directamente; si es `True`, muestra un `QMessageBox` con "Guardar"/"Descartar"/"Cancelar" — "Cancelar" hace `event.ignore()`, "Descartar" acepta el cierre sin tocar el fichero, y "Guardar" reutiliza `_save_project()` y solo acepta el cierre si terminó con éxito (si el usuario cancela el diálogo de ruta o falla el guardado, `is_modified` sigue en `True` y el cierre se ignora también).

## Undo/Redo — `CommandManager` + `Command`

`studio/commands/`. `Command` (`command.py`) es un `Protocol` con `name: str`, `redo()` y `undo()` — cualquier objeto que implemente esos tres miembros sirve como comando, sin herencia obligatoria.

`CommandManager` (`command_manager.py`) mantiene dos pilas (`undo_stack`, `redo_stack`):

- `execute(command)` — ejecuta `command.redo()`, lo apila en `undo_stack` y **vacía `redo_stack`** (una nueva acción invalida el historial de "rehacer").
- `undo()` — desapila de `undo_stack`, llama a `command.undo()`, lo apila en `redo_stack`.
- `redo()` — inverso: desapila de `redo_stack`, llama a `command.redo()`, lo vuelve a apilar en `undo_stack`.
- `can_undo()` / `can_redo()` — usados por `MainWindow._update_undo_redo()` para habilitar/deshabilitar los menús.

Comandos concretos (todos con la misma forma: guardan el estado antes/después y lo aplican vía `self.services.projects.current_project`):

| Comando | Efecto de `redo()` | Efecto de `undo()` |
|---|---|---|
| `MovePieceCommand` | Mueve la pieza a `(new_x, new_y)`. | La devuelve a `(old_x, old_y)`. |
| `RotatePieceCommand` | Aplica `new_rotation`. | Restaura `old_rotation`. |
| `DeletePieceCommand` | Elimina la pieza del proyecto. | La reinserta. |

Ninguno valida colisiones por sí mismo — la validación (`PlacementValidator`) ocurre **antes** de construir y ejecutar el comando, en `MainWindow` o `BoardWorkspace`.

## Selección — dos capas distintas

Hay **dos** mecanismos de selección con responsabilidades distintas, que se sincronizan pero no son el mismo objeto:

- **`SelectionManager`** (`studio/selection/selection_manager.py`, servicio de `StudioServices`) — selección a nivel de aplicación: un conjunto de ids (`_selected_ids`), con `select_one()`, `add()`, `remove()`, `toggle()`, `clear()`.
- **`SelectionController`** (`studio/workspace/selection_controller.py`) — selección a nivel del workspace gráfico: mantiene la lista de `BoardPieceItem` (`bind_items()`) y aplica el resaltado visual (`apply_selection()` de `studio/workspace/selection.py`). Cuando la selección del workspace queda en un único elemento, la propaga a `SelectionManager.select_one()`. `sync_inspector(window)` actualiza el panel inspector según haya 0 o 1 elementos seleccionados.

## Validación de colocación — `PlacementValidator`

`studio/workspace/placement_validator.py`. Única fuente de verdad para saber si una pieza puede colocarse o rotarse (ADR-010):

- `constrain_position(item, new_pos)` — recorta la posición propuesta para que la pieza no salga de `board_rect` (clamping, no rechazo).
- `collides(item)` / `overlaps(rect_a, rect_b)` — colisión contra el resto de `BoardPieceItem` de la escena, vía `QRectF.intersects()`.
- `can_place(item)` — `True` si la pieza está dentro del tablero y no colisiona.
- `rotated_rect(item, angle)` / `can_rotate(item, angle)` — calcula el rectángulo que ocuparía la pieza tras rotar 90° e intercambiar `length_mm`/`width_mm`, y comprueba que quepa sin colisionar.

`MainWindow._rotate_selected_piece()` llama a `can_rotate_item()` (envoltorio en `BoardWorkspace` sobre `PlacementValidator.can_rotate()`) **antes** de crear el `RotatePieceCommand`; si no cabe, muestra un mensaje en la barra de estado y no ejecuta nada.

## Inspector contextual — `studio/panels/inspector_panel.py`

Cubre `IDE-0003` (`docs/masterplan/DOC-004-Backlog.md`) y la especificación `docs/masterplan/ui/SCR-004-Inspector.md`. `render_project()`/`render_board()`/`render_piece()`/`render_empty()` son funciones puras (sin Qt, testeadas en `tests/test_inspector_panel.py`) que devuelven el HTML mostrado en el dock "Inspector" (`MainWindow.inspector.setHtml(...)`), según qué se seleccione en el explorador o en el workspace:

- **Proyecto** (nodo raíz del explorador): nombre, materiales usados (unión de tableros + piezas), nº de tableros, nº de piezas.
- **Tablero**: dimensiones, material, nº de piezas colocadas, superficie utilizada y desperdicio (calculados sumando el área de las piezas de `project.placements` — Studio solo soporta un tablero activo por proyecto, así que se asume que todas las colocaciones pertenecen a él).
- **Pieza**: dimensiones, material, rotación y coordenadas si está colocada; si no, se indica explícitamente "Sin colocar".

Solo se muestran campos con datos reales. La especificación SCR-004 menciona campos que el modelo de datos actual no soporta (descripción y fecha de modificación de proyecto, espesor y restricciones activas) — se omiten en vez de rellenarlos con valores inventados; la propia especificación los marca como "edición directa de propiedades" para una versión futura, no la actual.

Los contextos "Solución" y "Algoritmo" de SCR-004 dependen del Comparador (`IDE-0002`, aún sin construir) y no están cubiertos todavía.

## Arrastre de piezas — `DragController`

`studio/workspace/drag_controller.py`. Deliberadamente mínimo: solo guarda `(piece_id, x, y)` al iniciar el arrastre (`begin()`) y lo devuelve al soltar (`clear()`), para que `BoardWorkspace` pueda comparar posición inicial/final y decidir si merece la pena crear un `MovePieceCommand` (evita comandos de undo/redo vacíos cuando no hubo movimiento real).

## Flujo de resolución de layout

`MainWindow._solve_layout()` → `services.layout.solve_current_project()` (Core, ver `docs/architecture.md`) → si hay solución, `_show_layout_solution()` la muestra en el inspector (piezas colocadas, dimensiones totales, `waste_ratio`) **sin aplicarla todavía**. `_apply_layout()` es un paso explícito y separado: llama a `services.layout.apply_last_solution_to_current_project()`, recarga el workspace y limpia la selección. Este calcular-antes-de-aplicar es intencional: dos operaciones distintas, ninguna deshace la otra automáticamente (no hay un `ApplyLayoutCommand` en el sistema de undo/redo).

## Comparador de soluciones — `studio/panels/comparator_panel.py`

Cubre `IDE-0002` (`docs/masterplan/DOC-004-Backlog.md`) y la especificación `docs/masterplan/ui/SCR-003-Comparador.md`. `render_comparison(solutions)` es una función pura (sin Qt, testeada en `tests/test_comparator_panel.py`) que construye la tabla HTML mostrada en el dock "Comparador" (tabificado junto a "Timeline" en la zona inferior).

- **`LayoutService.compare_solutions()`** (`studio/layout_service.py`, testeado en `tests/test_layout_service.py`) ejecuta `GeometrySolver` con `material_first_strategy()` (en vez de la `balanced_strategy()` por defecto de `solve_current_project()`) porque incluye los cinco generadores — `horizontal`, `vertical`, `free_space`, `skyline`, `maxrects` — necesarios para comparar algoritmos realmente distintos; guarda hasta `MAX_COMPARISON_SOLUTIONS` (4, según el criterio de aceptación de SCR-003) en `last_solutions`.
- **`LayoutService.apply_comparison_solution(index)`** aplica la solución de esa posición al proyecto actual; devuelve `False` si el índice está fuera de rango, sin lanzar excepción.
- `MainWindow._compare_solutions()`/`_apply_comparison_solution(index)` conectan esto al menú "Comparar": "Generar comparación" y cuatro acciones "Aplicar solución 1..4".

Métricas mostradas por solución: algoritmo (`explanation.notes` tal cual las registra el generador), piezas colocadas, aprovechamiento y desperdicio (`1 - waste_ratio` / `waste_ratio`), puntuación (`score.total`), y fortalezas/debilidades de `explanation`. La especificación SCR-003 pide también número de cortes, tiempo de cálculo, fragmentación del material y tiempo estimado de mecanizado — **ninguno de estos se calcula en el dominio actual**, así que se omiten con una nota explícita en vez de inventarse. Tampoco hay todavía miniaturas gráficas por tablero (solo texto/tabla) ni "fijar como favorita".

## Exportación — `studio/export/`

Cubre `IDE-0005` (`docs/masterplan/DOC-004-Backlog.md`). Exporta el estado actual del workspace (lo que haya colocado en `project.placements`, venga de arrastrar piezas o de aplicar una solución) a fichero — no depende de haber ejecutado el solver.

- **`solution_bridge.py::studio_project_to_solution(project)`** — función pura que convierte `StudioProject` (piezas + `StudioPlacement`) a un `AssemblySolution` del Core (`BoardPlacement`, intercambiando `length_mm`/`width_mm` si `rotated=True`). Evita reimplementar en Studio la geometría de bounding-box que ya existe en `boardcomposer.domain`.
- **`svg_export.py::export_project_to_svg(project, path)`** — reutiliza `boardcomposer.export.solution_to_svg()` del Core sobre la solución convertida. Devuelve `False` (sin escribir fichero) si no hay piezas colocadas.
- **`pdf_export.py::export_project_to_pdf(project, path)`** — misma idea que el SVG (rectángulos + etiqueta `board_id`) pero dibujada con `QPainter` sobre un `QPdfWriter`, a 96 DPI con la página ajustada a las dimensiones reales en mm. Vive en Studio y no en el Core porque necesita Qt (`docs/architecture.md`: el Core nunca depende de una interfaz). Como `QPainter`/`QFontDatabase` abortan sin una `QGuiApplication` activa, sus tests (`tests/test_pdf_export.py`) necesitan `tests/conftest.py`, que fija `QT_QPA_PLATFORM=offscreen` para que funcionen igual en local que en CI (sin pantalla).
- `MainWindow._export_svg()`/`_export_pdf()` conectan esto al menú "Exportar" → "Exportar SVG…"/"Exportar PDF…", pidiendo la ruta con `QFileDialog`.

## Asistente — `studio/assistant_service.py`, `studio/panels/chat_panel.py`

Cubre la Fase E de `IDE-0007` (`docs/masterplan/DOC-004-Backlog.md`). Un chat de ayuda contextual: el usuario escribe una pregunta libre sobre el proyecto abierto, los resultados o cómo usar Studio, y recibe una respuesta del `AIProvider` del Core (`docs/architecture.md`).

- **`AssistantService.ask(question)`** (`studio/assistant_service.py`, testeado en `tests/test_assistant_service.py`) construye un prompt con el contexto del proyecto actual (nombre, nº de tableros/piezas/piezas colocadas, o "No hay ningún proyecto abierto") más la pregunta, lo envía a `AIProvider.complete()` y añade el par `(pregunta, respuesta)` a `history`. Ignora preguntas en blanco sin llamar al proveedor. Usa `default_provider()` por defecto: `AnthropicProvider` si hay `ANTHROPIC_API_KEY` en el entorno, si no `MockAIProvider`.
- **`render_chat(history)`** (`studio/panels/chat_panel.py`, testeado en `tests/test_chat_panel.py`) es una función pura (sin Qt) que construye el HTML mostrado en el dock "Asistente" (tabificado junto a "Inspector"). A diferencia de `render_comparison()`/`render_project()` (que solo formatean datos generados internamente por el solver), aquí el contenido incluye texto libre tecleado por el usuario y devuelto por el proveedor de IA, así que escapa `<`/`>`/`&` antes de insertarlo en el HTML.
- `MainWindow._ask_assistant()` conecta el `QLineEdit` del dock (`returnPressed`) con `services.assistant.ask()` y refresca el `QTextEdit` del historial con `render_chat()`.

## EventBus — infraestructura presente, aún sin uso

`studio/events/event_bus.py`. `EventBus` implementa un pub/sub síncrono simple (`subscribe(event_name, handler)`, `publish(event_name, payload)`) y está instanciado en `StudioServices.events`, como prevé ADR-003 (Event Bus). **A día de hoy ningún componente de Studio llama a `publish()` ni `subscribe()`** — es infraestructura ya construida y disponible, pero todavía no conectada a ningún flujo real. Cualquier extensión futura que necesite desacoplar componentes (p. ej. notificar a varios paneles cuando cambia el proyecto) tiene esta pieza lista para usarse.

## Orquestación — `MainWindow`

`studio/main_window.py` es el único lugar que conecta todo lo anterior: construye menú/paneles/workspace (`_build_menu`, `_build_panels`, `_build_workspace`), reacciona a la selección del explorador (`_on_explorer_selection_changed`), y para cada acción de usuario (rotar, borrar, deshacer, rehacer, calcular layout, aplicar layout) sigue el mismo patrón: **validar → ejecutar comando (si aplica) → recargar workspace → actualizar título/undo-redo**.
