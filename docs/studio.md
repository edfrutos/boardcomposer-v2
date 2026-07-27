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

### Reapertura del último proyecto al arrancar

`MainWindow._load_last_or_demo_project()`. `_save_project()`/`_open_project()` recuerdan la ruta del fichero en `QSettings` (clave `last_project/path`, constante `LAST_PROJECT_PATH_SETTINGS_KEY`), y al arrancar se carga esa ruta en vez del proyecto demo. Cae a la demo solo si no hay ruta recordada, o si el fichero desapareció o está corrupto — arrancar nunca falla por esto.

`QSettings` necesita nombre de organización y aplicación para saber dónde escribir; se fijan en el constructor de `MainWindow` vía `QCoreApplication`. Los tests aíslan `QSettings` en un directorio temporal por test (`tests/conftest.py`), para no leer ni escribir los ajustes reales de la máquina de desarrollo.

### Proyectos dañados — colocaciones colgantes

`project_from_dict()` **descarta** las colocaciones que apuntan a una pieza o un tablero ausentes del fichero, en vez de rechazar el fichero entero: un proyecto dañado sigue siendo recuperable, y el siguiente guardado lo escribirá ya limpio. Cada descarte se informa por el callback opcional `on_warning` de `load_project_from_file()`, que `MainWindow` conecta a un diálogo de avisos. Antes la carga "tenía éxito" y el fallo aparecía después, sin protección, al renderizar el workspace.

Los modelos `StudioBoard`/`StudioPiece` validan sus dimensiones (positivas y finitas) y `StudioPlacement` sus coordenadas (finitas, pero no el signo: una coordenada negativa es un estado transitorio legítimo mientras se arrastra una pieza fuera del tablero). Sin esto, un `.bcstudio.json` manipulado podía sembrar un tablero de -500 mm o un `NaN` — `json.loads()` acepta `NaN`/`Infinity` como flotantes, y toda comparación contra `NaN` es falsa, así que las guardas `<= 0` no bastaban.

### Importación de piezas desde CSV — `studio/project/csv_import.py`

`load_pieces_from_csv(path, existing_ids)` (función pura, sin Qt, testeada en `tests/test_csv_import.py`) lee un CSV con las mismas columnas obligatorias que el importador CSV del Core/CLI (`id`/`length_mm`/`width_mm`/`thickness_mm`, más `material` opcional) y devuelve una lista de `StudioPiece`. Cualquier fila inválida (columna obligatoria ausente, dimensión no numérica, id vacío, o id repetido — dentro del propio fichero o contra `existing_ids`, los ids ya presentes en el proyecto abierto) lanza `CsvImportError` con el número de fila, abortando toda la importación sin devolver piezas parciales.

`MainWindow._import_pieces_csv()` conecta esto al `QAction` "Importar piezas (CSV)…" del menú Archivo (testeado en `tests/test_main_window_import_csv.py`): pide el tablero activo (igual que `_add_piece()`, sin tablero no hay dónde colocar), abre el CSV con `QFileDialog`, y por cada `StudioPiece` válida ejecuta un `AddPieceCommand` (deshacible, uno por pieza) colocándola en `(0, 0)` del tablero activo. Un fallo de `load_pieces_from_csv()` se muestra en la barra de estado y no ejecuta ningún comando — el proyecto queda exactamente como estaba.

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
| `RotatePieceCommand` | Aplica `new_rotation` (y `rotated`, más las coordenadas nuevas si hubo recolocación). | Restaura el estado anterior completo. |
| `DeletePieceCommand` | Elimina la pieza del proyecto. | La reinserta. |
| `AddBoardCommand` / `AddPieceCommand` | Añaden un `StudioBoard`/`StudioPiece` al proyecto. | Lo eliminan. |
| `EditBoardCommand` / `EditPieceCommand` | Sustituyen el modelo por su versión editada. | Restauran el anterior. |
| `MoveToBoardCommand` | Reasigna el `board_id` de una colocación (con las coordenadas nuevas si hubo recolocación). | Devuelve la colocación a su tablero y posición previos. |
| `SetKerfCommand` | Fija `project.kerf_mm` (ancho de sierra). | Restaura el valor anterior. |

Ninguno valida colisiones por sí mismo — la validación ocurre **antes** de construir y ejecutar el comando, en `MainWindow` o `BoardWorkspace` (`PlacementValidator` en el lienzo, `piece_fits_on_board()` fuera de él).

Los comandos resuelven `services.projects.current_project` **en el momento de deshacer**, no guardan una referencia al proyecto: si no, deshacer tras abrir otro proyecto aplicaba el comando al proyecto equivocado. `CommandManager.clear()` se llama además en cada transición de proyecto (nuevo, abrir, cargar el último al arrancar).

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

`MainWindow._rotate_selected_piece()` llama a `can_rotate_item()` (envoltorio en `BoardWorkspace` sobre `PlacementValidator.can_rotate()`) **antes** de crear el `RotatePieceCommand`; si no cabe en su posición actual, se intenta recolocar (ver abajo) y solo si tampoco así cabe se muestra un mensaje en la barra de estado sin ejecutar nada.

### Encaje fuera del lienzo — `placement_fit.py`

`studio/workspace/placement_fit.py`. `PlacementValidator` hace el mismo trabajo pero solo para el arrastre/rotación interactivos, acoplado a los `QGraphicsItem` vivos de la escena. Las acciones que reasignan una pieza a **otro** tablero ocurren fuera de esa escena, así que necesitan un equivalente sin Qt. Dos funciones puras (testeadas en `tests/test_placement_fit.py`), que reutilizan `boardcomposer.geometry.Rectangle.overlaps()` en vez de reimplementar la geometría:

- **`piece_fits_on_board(board, piece, x_mm, y_mm, rotated, other_placements, pieces_by_id)`** — `True` si la pieza cabe dentro de los límites del tablero en esa posición y no solapa a ninguna otra colocación.
- **`find_free_position(board, length_mm, width_mm, other_placements, pieces_by_id)`** — busca la esquina superior-izquierda de un hueco libre, o `None` si no hay. Heurística por esquinas: candidatas son el origen del tablero más el borde derecho/inferior de cada colocación existente, recorridas de arriba abajo y luego de izquierda a derecha. **No es empaquetado completo** — sirve para recolocar *una* pieza que si no habría que rechazar; resolver una disposición entera es trabajo del solver ("Generar").

Se usan en tres sitios de `MainWindow`, siempre antes de construir el comando: mover una pieza a otro tablero (`MoveToBoardCommand`, con el diálogo ofreciendo solo tableros del mismo grosor), rotarla en el sitio (`RotatePieceCommand`), y editar una pieza o un tablero (`_edit_piece()` comprueba que las dimensiones nuevas siguen cabiendo sin solapar; `_edit_board()`, que todas las piezas ya colocadas siguen encajando en el tablero redimensionado).

## Inspector contextual — `studio/panels/inspector_panel.py`

Cubre `IDE-0003` (`docs/masterplan/DOC-004-Backlog.md`) y la especificación `docs/masterplan/ui/SCR-004-Inspector.md`. `render_project()`/`render_board()`/`render_piece()`/`render_empty()` son funciones puras (sin Qt, testeadas en `tests/test_inspector_panel.py`) que devuelven el HTML mostrado en el dock "Inspector" (`MainWindow.inspector.setHtml(...)`), según qué se seleccione en el explorador o en el workspace:

- **Proyecto** (nodo raíz del explorador): nombre, materiales usados (unión de tableros + piezas), nº de tableros, nº de piezas.
- **Tablero**: dimensiones, material, nº de piezas colocadas, superficie utilizada y desperdicio. `MainWindow` filtra `project.placements` por el `board_id` del tablero seleccionado antes de llamar a `render_board()`: desde el soporte multi-tablero (`DT-0013`) cada colocación sabe a qué tablero pertenece.
- **Pieza**: dimensiones, material, rotación y coordenadas si está colocada; si no, se indica explícitamente "Sin colocar".

Solo se muestran campos con datos reales. La especificación SCR-004 menciona campos que el modelo de datos actual no soporta (descripción y fecha de modificación de proyecto, espesor y restricciones activas) — se omiten en vez de rellenarlos con valores inventados; la propia especificación los marca como "edición directa de propiedades" para una versión futura, no la actual.

Los contextos "Solución" y "Algoritmo" de SCR-004 siguen sin cubrirse como vistas propias del Inspector: la información equivalente se muestra en el Comparador (`IDE-0002`, ver más abajo) y en el resumen que `_show_layout_solution()` vuelca en el Inspector tras "Generar".

## Ancho de sierra (kerf)

`StudioProject.kerf_mm` (por defecto `0.0`, persistido en `.bcstudio.json` con migración retrocompatible vía `data.get("kerf_mm", 0.0)`). Se configura en el menú "Proyecto" → "Ancho de sierra…" (`KerfDialog`) y se cambia con `SetKerfCommand`, deshacible como cualquier otro comando.

El Core no sabe qué es un kerf y no necesita saberlo (`DEC-0016`): la traducción vive entera en Studio, en tres sitios que comparten la misma convención — **cada pieza se ensancha un corte a la derecha y otro abajo**.

- **Solver** — `LayoutService.to_core_project()` entrega cada pieza con `length_mm + kerf` y `width_mm + kerf`, y el tablero con `length_mm + kerf` / `width_mm + kerf`. Lo segundo cancela lo primero: N piezas en fila ocupan `suma(largos) + N·kerf` y deben caber en `largo + kerf`, es decir `suma(largos) + (N-1)·kerf ≤ largo` — exactamente los N-1 cortes que hacen falta para separar N piezas. Sin agrandar el tablero, una pieza del ancho completo del tablero (el caso más común: cortes transversales) dejaba de caber, porque reservaba un corte contra el borde del propio tablero, donde no hay nada que cortar.
- **Encaje fuera del lienzo** — `piece_fits_on_board()` y `find_free_position()` aceptan `kerf_mm` (por defecto `0.0`). Los límites del tablero se comprueban contra la pieza real; el solape, contra la pieza **y su vecina**, ambas ensanchadas. Ensanchar solo la candidata no detectaría a la vecina de la izquierda, cuyo corte es el que se estaría invadiendo; ensanchar las dos exige exactamente un kerf de separación en cualquier dirección, no dos.
- **Arrastre interactivo** — `BoardWorkspace.constrain_piece_position()` se lo pasa a `PlacementValidator.constrain_position()`, que separa la pieza `gap_mm` de sus vecinas al hacer *snap*.

**El kerf no llega nunca al plano exportado**: `studio_project_to_solution()` dibuja las dimensiones reales de la pieza. La holgura es espacio reservado en el tablero, no parte de la pieza — un plano dibujado 3 mm más grande por lado se cortaría mal.

En dos dimensiones sigue siendo una aproximación conservadora (una pieza puede reservar un corte que su posición concreta no necesita). Reservar de más desperdicia material sobre el papel; reservar de menos produce un plano que no se puede cortar.

## Lienzo — etiquetas

`create_board_item()` (`studio/workspace/board_item.py`) dibuja el rectángulo del tablero y añade su `board_id` como `QGraphicsSimpleTextItem` **fuera** de los límites del tablero, para no solaparse con una pieza colocada cerca del origen. Las piezas se etiquetan a su vez con su `piece_id` (`create_piece_item()`): con varios tableros, sin la etiqueta del tablero la única forma de saber cuál se estaba mirando era el Explorer o el Inspector.

## Arrastre de piezas — `DragController`

`studio/workspace/drag_controller.py`. Deliberadamente mínimo: solo guarda `(piece_id, x, y)` al iniciar el arrastre (`begin()`) y lo devuelve al soltar (`clear()`), para que `BoardWorkspace` pueda comparar posición inicial/final y decidir si merece la pena crear un `MovePieceCommand` (evita comandos de undo/redo vacíos cuando no hubo movimiento real).

## Flujo de resolución de layout

`MainWindow._solve_layout()` → `services.layout.solve_current_project()` (Core, ver `docs/architecture.md`) → si hay solución, `_show_layout_solution()` la muestra en el inspector (piezas colocadas, dimensiones totales, `waste_ratio`) **sin aplicarla todavía**. `_apply_layout()` es un paso explícito y separado: llama a `services.layout.apply_last_solution_to_current_project()`, recarga el workspace y limpia la selección. Este calcular-antes-de-aplicar es intencional: dos operaciones distintas, ninguna deshace la otra automáticamente (no hay un `ApplyLayoutCommand` en el sistema de undo/redo).

Con varios tableros, el solver resuelve siempre **uno solo** — el activo (`_resolve_board()`), cuyas dimensiones se convierten en las restricciones del `Project` del Core. De ahí tres reglas en `to_core_project()`/`_apply_solution()`, todas para no estropear el resto del proyecto:

- Las piezas ya colocadas en **otro** tablero se excluyen del candidato; si no, resolver el tablero B reempaquetaba una pieza ya puesta en el A y quedaban dos colocaciones para la misma pieza.
- Se excluyen también las piezas cuyo `thickness_mm` no coincide con el del tablero que se resuelve: una pieza sin tablero de su grosor queda correctamente sin colocar, en vez de forzada donde no corresponde.
- Al aplicar, se sustituyen solo las colocaciones del tablero resuelto, no la lista entera (antes se vaciaban los demás tableros).

`_fill_other_empty_boards_with_leftovers()` prueba después los demás tableros del proyecto con lo que haya quedado sin colocar, pero **solo los que están completamente vacíos** — nunca rebaraja un tablero que alguien ya había ordenado.

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
- **`pdf_export.py::export_project_to_pdf(project, path)`** — misma idea que el SVG (rectángulos + etiqueta `board_id`) pero dibujada con `QPainter` sobre un `QPdfWriter`, a 96 DPI con la página ajustada a las dimensiones reales en mm. Vive en Studio y no en el Core porque necesita Qt (`docs/architecture.md`: el Core nunca depende de una interfaz). Como `QPainter`/`QFontDatabase` abortan sin una `QGuiApplication` activa, sus tests (`tests/test_pdf_export.py`) necesitan `tests/conftest.py`, que fija `QT_QPA_PLATFORM=offscreen`. En local (macOS) eso basta; en CI (runner Ubuntu sin cabecera) además hace falta instalar las librerías nativas de Qt (`libegl1`, `libgl1`, `libxkbcommon0`, paquetes `libxcb-*`) — sin ellas, ni siquiera se puede *importar* `PySide6.QtGui`/`QtWidgets` (falla con `libEGL.so.1: cannot open shared object file`, no es un problema del plugin offscreen en sí). Ver el paso "Install Qt runtime libraries" en `.github/workflows/ci.yml`.
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
