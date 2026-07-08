# Arquitectura

Desarrollo del principio fundamental de `docs/masterplan/DOC-002-Arquitectura.md`: el Core nunca depende de ninguna interfaz; toda interfaz se construye alrededor de él.

## Capas (estado real del código)

```
                 BoardComposer
                       │
        ┌──────────────┼──────────────┐
        │                             │
        ▼                             ▼
BoardComposer Studio (studio/)    CLI (cli.py)
        │                             │
        └──────────────┬──────────────┘
                        ▼
              boardcomposer Core (src/boardcomposer/)
                        │
     ┌──────────────────┼───────────────────┐
     ▼                  ▼                   ▼
  domain/            solver/            io/, export/, presenters/
     │                  │                   │
     └──────────────────┼───────────────────┘
                         ▼
                  geometry/, layout/
```

No existe todavía una capa API independiente (DOC-002 y DOC-008 la describen como evolución prevista, no como código actual).

## Core (`src/boardcomposer/`)

- **`domain/`** — modelos inmutables: `Board`, `Project`, `ProjectConstraints`, `BoardPlacement`, `AssemblySolution`, `SolutionScore`, `SolutionExplanation` (ver `docs/data_model.md`). Sin dependencias de `solver`, `io` ni interfaz alguna.
- **`geometry/`** — primitiva `Rectangle` y utilidades de colisión/transformación, compartidas por `domain` y `solver`.
- **`layout/`** — gestión de espacio libre (`FreeSpaceManager`, `place_board_in_first_space`) usada por el generador `free_space`.
- **`solver/`** — generadores de layout, validación de restricciones, deduplicación y evaluación (ver `docs/algorithms.md` y `docs/scoring.md`). `GeometrySolver` (en `solver/geometry_solver.py`) es el punto de entrada: envuelve `CandidatePipeline` con una `OptimizationStrategy`.
- **`io/`** — `load_project_from_csv()`, la única fuente de importación implementada hoy (RF-002 solo cubre CSV; Excel sigue pendiente).
- **`export/`** — `solution_to_svg()`, único exportador implementado.
- **`presenters/`** — `solution_to_text()` y `solutions_to_json()`, formateo de resultados para el CLI.

## CLI (`src/boardcomposer/cli.py`)

Consume el Core directamente: carga un `Project` (desde CSV o `build_demo_project()`), construye una `OptimizationStrategy` por nombre y llama a `GeometrySolver(project, strategy).solve()`. Sin lógica propia de negocio — es una interfaz fina sobre el Core, tal como exige el principio arquitectónico.

## BoardComposer Studio (`studio/`)

Aplicación PySide6 (Qt) para explorar y editar proyectos visualmente. Estructura interna:

- **`models/`** — `StudioProject`, `StudioBoard`, `StudioPiece`, `StudioPlacement`: modelos propios de Studio, distintos de los del Core.
- **`workspace/`** — `BoardWorkspace`, `BoardPieceItem`, `SelectionController`, `DragController`, `PlacementValidator`, cámara y grid: la superficie gráfica (`QGraphicsScene`/`QGraphicsView`) donde el usuario coloca piezas manualmente.
- **`commands/`** — `CommandManager` + comandos (`MovePieceCommand`, `RotatePieceCommand`, `DeletePieceCommand`): patrón Command para undo/redo (ver ADR-008).
- **`events/`** — `EventBus` síncrono para desacoplar componentes de Studio (ver ADR-003).
- **`selection/`** — `SelectionManager`, seguimiento de qué objetos están seleccionados.
- **`project/`** — `ProjectManager`, ciclo de vida del proyecto abierto en Studio.
- **`layout_service.py`** — **el puente explícito entre Studio y el Core.** `LayoutService.to_core_project()` traduce un `StudioProject` a un `Project` del Core (con `ProjectConstraints(allow_rotation=True, allow_cutting=False)`); `solve_current_project()` invoca `GeometrySolver` sobre ese proyecto traducido; `apply_last_solution_to_current_project()` vuelca las `BoardPlacement` resultantes de vuelta a `StudioPlacement`. Es el único punto donde Studio conoce tipos del Core.
- **`main_window.py`** — ventana principal, ensambla menú, paneles y workspace.

## Regla de dependencia

`studio/` importa desde `boardcomposer` (el Core); lo inverso nunca ocurre. `LayoutService` es la única clase de Studio que importa tipos del Core (`Board`, `Project`, `ProjectConstraints`, `GeometrySolver`) — el resto de Studio trabaja exclusivamente con sus propios modelos (`StudioProject`, `StudioBoard`, etc.).
