# Arquitectura

Desarrollo del principio fundamental de `docs/masterplan/DOC-002-Arquitectura.md`: el Core nunca depende de ninguna interfaz; toda interfaz se construye alrededor de él.

## Capas (estado real del código)

```
                 BoardComposer
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │                             │              │
        ▼                             ▼              ▼
BoardComposer Studio (studio/)    CLI (cli.py)   API (api.py)
        │                             │              │
        └──────────────┬──────────────┴──────────────┘
                        ▼
              boardcomposer Core (src/boardcomposer/)
                        │
     ┌──────────────────┼───────────────────┬──────────┐
     ▼                  ▼                   ▼          ▼
  domain/            solver/            io/, export/,  ai/
     │                  │               presenters/    │
     └──────────────────┼───────────────────┴──────────┘
                         ▼
                  geometry/, layout/
```

## Core (`src/boardcomposer/`)

- **`domain/`** — modelos inmutables: `Board`, `Project`, `ProjectConstraints`, `BoardPlacement`, `AssemblySolution`, `SolutionScore`, `SolutionExplanation` (ver `docs/data_model.md`). Sin dependencias de `solver`, `io` ni interfaz alguna.
- **`geometry/`** — primitiva `Rectangle` y utilidades de colisión/transformación, compartidas por `domain` y `solver`.
- **`layout/`** — gestión de espacio libre (`FreeSpaceManager`, `place_board_in_first_space`) usada por el generador `free_space`.
- **`solver/`** — generadores de layout, validación de restricciones, deduplicación y evaluación (ver `docs/algorithms.md` y `docs/scoring.md`). `GeometrySolver` (en `solver/geometry_solver.py`) es el punto de entrada: envuelve `CandidatePipeline` con una `OptimizationStrategy`.
- **`io/`** — `load_project_from_csv()`, la única fuente de importación implementada hoy (RF-002 solo cubre CSV; Excel sigue pendiente).
- **`export/`** — `solution_to_svg()`, único exportador implementado.
- **`presenters/`** — `solution_to_text()` y `solutions_to_json()`, formateo de resultados para el CLI.
- **`ai/`** — cubre las Fases A, B, C y D de `IDE-0007` (`docs/masterplan/DOC-004-Backlog.md`). Fase A: puerto `AIProvider` (`ABC`, mismo patrón que `Presenter`) con un único método `complete(prompt: str) -> str`, `MockAIProvider` como implementación sin llamadas externas y `provider_by_name()` para resolver el proveedor por nombre (mismo patrón que `strategy_by_name()`). Fase B: `project_from_text()` (`project_from_text.py`) construye un `Project` a partir de texto libre — pide al `AIProvider` un JSON con la misma forma que ya valida `/solve` en la API (`boards`/`constraints`) y reutiliza esa misma validación; si la respuesta no es interpretable lanza `ProjectFromTextError`. Fase C: `explain_solution()` (`explain_solution.py`) pide al `AIProvider` una explicación en lenguaje natural de un `AssemblySolution`, a partir de sus métricas (tablas colocadas, dimensiones, desperdicio, puntuación) y de `SolutionExplanation`; a diferencia de `project_from_text()`, aquí la salida es texto libre sin parseo. Fase D: `suggest_strategy()` (`suggest_strategy.py`) traduce un objetivo en lenguaje natural en una `OptimizationStrategy` (pesos de `solver/scoring_weights.py` + `generator_names` validados contra `solver.generators.GENERATOR_REGISTRY`) que `GeometrySolver` ejecuta igual que las estrategias predefinidas — la IA nunca genera geometría directamente, solo ajusta los parámetros del solver determinista. Todavía no hay proveedor real conectado ni el chat contextual — queda para la fase final de `IDE-0007`, construida sobre el mismo puerto.

## CLI (`src/boardcomposer/cli.py`)

Consume el Core directamente: carga un `Project` (desde CSV o `build_demo_project()`), construye una `OptimizationStrategy` por nombre y llama a `GeometrySolver(project, strategy).solve()`. Sin lógica propia de negocio — es una interfaz fina sobre el Core, tal como exige el principio arquitectónico.

## API (`src/boardcomposer/api.py`)

Cubre `IDE-0006` (`docs/masterplan/DOC-004-Backlog.md`). Primer contrato HTTP mínimo sobre el Core (Flask, ya declarado en `pyproject.toml` pero sin usar hasta ahora) — mismo papel que `cli.py`, sin lógica propia: traduce peticiones a las mismas llamadas que ya usan CLI y Studio (`Project`/`ProjectConstraints`/`GeometrySolver`/`solutions_to_json`).

| Ruta | Método | Qué hace |
|---|---|---|
| `/health` | GET | Comprobación trivial de que el servicio responde. |
| `/strategies` | GET | Lista las estrategias registradas (`balanced`, `material`, `compact`). |
| `/solve` | POST | Recibe `boards`/`constraints`/`strategy`/`top` en JSON, ejecuta `GeometrySolver` y devuelve el mismo JSON que ya genera `solutions_to_json()` para el CLI. |

`docs/masterplan/DOC-008-API.md` describe una API mucho más amplia — autenticación, versionado (`/api/v1/`), gestión de perfiles, soporte multi-cliente — pero ese documento sigue "🟡 En revisión... pendiente de: definir los contratos públicos... especificar los recursos principales". Esta primera versión implementa solo lo que el backlog pide ("API pública", sin más detalle) y deja el resto para cuando esos contratos se definan: sin auth, sin versionado, sin persistencia entre peticiones.

## BoardComposer Studio (`studio/`)

Aplicación PySide6 (Qt) para explorar y editar proyectos visualmente. Estructura interna:

- **`models/`** — `StudioProject`, `StudioBoard`, `StudioPiece`, `StudioPlacement`: modelos propios de Studio, distintos de los del Core.
- **`workspace/`** — `BoardWorkspace`, `BoardPieceItem`, `SelectionController`, `DragController`, `PlacementValidator`, cámara y grid: la superficie gráfica (`QGraphicsScene`/`QGraphicsView`) donde el usuario coloca piezas manualmente.
- **`commands/`** — `CommandManager` + comandos (`MovePieceCommand`, `RotatePieceCommand`, `DeletePieceCommand`): patrón Command para undo/redo (ver ADR-008).
- **`events/`** — `EventBus` síncrono para desacoplar componentes de Studio (ver ADR-003).
- **`selection/`** — `SelectionManager`, seguimiento de qué objetos están seleccionados.
- **`project/`** — `ProjectManager` (ciclo de vida del proyecto abierto) + `project_io.py` (persistencia JSON `.bcstudio.json`).
- **`panels/`** — contenido de los paneles contextuales: `inspector_panel.py` (Proyecto/Tablero/Pieza) y `comparator_panel.py` (comparación de varias soluciones). Funciones puras, sin Qt, testeadas directamente.
- **`export/`** — exportación del estado actual del workspace a fichero: `svg_export.py` reutiliza `boardcomposer.export.solution_to_svg()` del Core; `pdf_export.py` dibuja lo mismo vía `QPainter`/`QPdfWriter` (Qt, por eso vive en Studio y no en el Core). `solution_bridge.py` convierte `StudioProject` (piezas + colocaciones) a un `AssemblySolution` del Core para que ambos exportadores reutilicen la misma geometría.
- **`layout_service.py`** — **el puente explícito entre Studio y el Core.** `LayoutService.to_core_project()` traduce un `StudioProject` a un `Project` del Core (con `ProjectConstraints(allow_rotation=True, allow_cutting=False)`); `solve_current_project()`/`compare_solutions()` invocan `GeometrySolver` sobre ese proyecto traducido; `apply_last_solution_to_current_project()`/`apply_comparison_solution()` vuelcan las `BoardPlacement` resultantes de vuelta a `StudioPlacement`. Es el único punto donde Studio conoce tipos del Core.
- **`main_window.py`** — ventana principal, ensambla menú, paneles y workspace.

## Regla de dependencia

`studio/` importa desde `boardcomposer` (el Core); lo inverso nunca ocurre. `LayoutService` es la única clase de Studio que importa tipos del Core (`Board`, `Project`, `ProjectConstraints`, `GeometrySolver`) — el resto de Studio trabaja exclusivamente con sus propios modelos (`StudioProject`, `StudioBoard`, etc.).
