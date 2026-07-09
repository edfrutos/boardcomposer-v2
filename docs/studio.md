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

## Arrastre de piezas — `DragController`

`studio/workspace/drag_controller.py`. Deliberadamente mínimo: solo guarda `(piece_id, x, y)` al iniciar el arrastre (`begin()`) y lo devuelve al soltar (`clear()`), para que `BoardWorkspace` pueda comparar posición inicial/final y decidir si merece la pena crear un `MovePieceCommand` (evita comandos de undo/redo vacíos cuando no hubo movimiento real).

## Flujo de resolución de layout

`MainWindow._solve_layout()` → `services.layout.solve_current_project()` (Core, ver `docs/architecture.md`) → si hay solución, `_show_layout_solution()` la muestra en el inspector (piezas colocadas, dimensiones totales, `waste_ratio`) **sin aplicarla todavía**. `_apply_layout()` es un paso explícito y separado: llama a `services.layout.apply_last_solution_to_current_project()`, recarga el workspace y limpia la selección. Este calcular-antes-de-aplicar es intencional: dos operaciones distintas, ninguna deshace la otra automáticamente (no hay un `ApplyLayoutCommand` en el sistema de undo/redo).

## EventBus — infraestructura presente, aún sin uso

`studio/events/event_bus.py`. `EventBus` implementa un pub/sub síncrono simple (`subscribe(event_name, handler)`, `publish(event_name, payload)`) y está instanciado en `StudioServices.events`, como prevé ADR-003 (Event Bus). **A día de hoy ningún componente de Studio llama a `publish()` ni `subscribe()`** — es infraestructura ya construida y disponible, pero todavía no conectada a ningún flujo real. Cualquier extensión futura que necesite desacoplar componentes (p. ej. notificar a varios paneles cuando cambia el proyecto) tiene esta pieza lista para usarse.

## Orquestación — `MainWindow`

`studio/main_window.py` es el único lugar que conecta todo lo anterior: construye menú/paneles/workspace (`_build_menu`, `_build_panels`, `_build_workspace`), reacciona a la selección del explorador (`_on_explorer_selection_changed`), y para cada acción de usuario (rotar, borrar, deshacer, rehacer, calcular layout, aplicar layout) sigue el mismo patrón: **validar → ejecutar comando (si aplica) → recargar workspace → actualizar título/undo-redo**.
