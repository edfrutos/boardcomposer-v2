# Arquitectura interna del Solver

Cubre `DT-0002` (`docs/masterplan/DOC-006-DeudaTecnica.md`): "Revisar y documentar la arquitectura interna del Solver tras la incorporación de nuevos algoritmos". Complementa a `docs/algorithms.md` (qué hace cada algoritmo) documentando **cómo están organizados los ficheros internamente** y qué cadena de llamadas hay detrás de cada uno — incluida la proliferación de módulos `maxrects_*` que ha ido creciendo con cada algoritmo añadido.

## Dos jerarquías de solver independientes

`BaseSolver` (`base_solver.py`) es una `ABC` con un único método abstracto `solve() -> list[AssemblySolution]`. Solo tiene **dos** implementaciones, y no comparten código entre sí:

- **`GeometrySolver`** (`geometry_solver.py`) — el solver de producción. `solve()` delega en `CandidatePipeline` (ver `docs/algorithms.md`), que ejecuta los generadores de la estrategia elegida, filtra por restricciones, deduplica y puntúa con `evaluate()`/`ScoringWeights`. Es el único que usa el CLI (`cli.py`) y `LayoutService` (Studio).
- **`SequentialSolver`** (`sequential_solver.py`) — coloca las tablas en fila (con salto de línea manual si no caben) calculando su propia puntuación simplificada a mano (`usage_score`/`waste_score` con fórmulas ad-hoc), sin pasar por `evaluate()` ni `ScoringWeights`. **No es un experimento abandonado**: según el historial del repositorio original (`edfrutos/boardcomposer`), fue el primer solver del proyecto (27/06/2026, "Motor v0.1" de `TODO.md`), construido incrementalmente antes de que existieran `GENERATOR_REGISTRY`/`CandidatePipeline`. Se mantiene como implementación de referencia mínima — exportada en `solver/__init__.py` y cubierta por tests — pero **no la invoca ni el CLI, ni `generators.py`, ni Studio**; no forma parte del pipeline de producción.

## La familia MaxRects: por qué hay tantos ficheros `maxrects_*`

Esto es lo que más ha crecido y lo que motiva este documento. La cadena real, de arriba abajo:

```
generators.py (GENERATOR_REGISTRY["maxrects"])
  → maxrects_generator.py :: generate_maxrects_solution()
    → maxrects_search.py :: generate_best_maxrects_solution()
      → search.py :: search_best_solution()            (elige la mejor por nº de piezas/dimensiones)
      → maxrects_runner.py :: iter_maxrects_solutions()  (itera heurística × orden de tablas)
        → maxrects/maxrects.py :: MaxRects               (el algoritmo geométrico real)
```

MaxRects "clásico", sin beam search — es la ruta más barata computacionalmente.

Existe una **segunda ruta**, con beam search, registrada en `GENERATOR_REGISTRY` como `"maxrects_beam"` (`beam_width=4`, ver `docs/algorithms.md`):

```
generators.py (GENERATOR_REGISTRY["maxrects_beam"])
  → generators.py :: maxrects_beam_generator()
    → maxrects_search.py :: generate_beam_maxrects_solution(beam_width=4)
      → maxrects_beam_runner.py :: iter_beam_maxrects_solutions()
        → solver/maxrects/beam.py :: search_states()   (beam search genérico sobre MaxRectsState)
```

No está incluida en ninguna `OptimizationStrategy` por defecto (`balanced`/`material`/`compact`) — hay que seleccionarla explícitamente pasando `"maxrects_beam"` en `generator_names`. Las herramientas de exploración (`workbench/app.py`, `tools/visualize_demo.py`) usan una tercera vía equivalente, `maxrects_engine.py::iter_maxrects_candidates(project, beam_width)`, que decide entre la ruta clásica y la de beam search según el `beam_width` recibido — útil para comparar ambas variantes en un mismo script, pero no es la que usa `GENERATOR_REGISTRY`.

### Paquete `solver/maxrects/` — el algoritmo en sí

Todos los ficheros anteriores son *runners* (orquestan iteración de heurísticas/órdenes); la lógica geométrica vive en el subpaquete:

| Fichero | Contenido |
|---|---|
| `maxrects.py` | Clase `MaxRects`: mantiene la lista de rectángulos libres, `find_best_rectangle()`, `place()`/`place_candidate()` (ver `docs/algorithms.md`). |
| `free_rectangle.py` | `FreeRectangle` — rectángulo libre disponible. |
| `placement.py` | `MaxRectsPlacement` — resultado de una colocación. |
| `heuristics.py` | `Heuristic` (alias de tipo) + `best_area_fit`, `best_bottom_left_fit`, `best_long_side_fit`, `best_short_side_fit`. |
| `orderings.py` | `MAXRECTS_BOARD_ORDERINGS` — reexporta los mismos tres órdenes de `board_ordering.py` (ver más abajo). |
| `strategies.py` | `MAXRECTS_HEURISTICS` — registro de heurísticas disponibles. |
| `state.py` / `beam.py` / `scoring.py` | `MaxRectsState`, `search_states()`, `score_state()` — solo usados por la ruta de beam search. |

## La familia Skyline (más simple, un único camino)

```
generators.py (GENERATOR_REGISTRY["skyline"])
  → skyline_generator.py :: generate_skyline_solution()
    → skyline_search.py :: generate_best_skyline_solution()
      → search.py :: search_best_solution()
      → skyline_runner.py :: iter_skyline_solutions()   (itera 3 órdenes de tablas)
        → skyline/skyline.py :: Skyline                  (el algoritmo geométrico real)
```

A diferencia de MaxRects, Skyline no tiene variante beam search ni una segunda ruta — un único camino, sin la duplicación de MaxRects.

## Piezas compartidas entre familias

- **`board_ordering.py`** (`original_order`, `largest_area_first`, `longest_edge_first`) — los tres órdenes de tablas están definidos **una sola vez** aquí y los reutilizan tanto `skyline_runner.py` como `maxrects/orderings.py` (que solo los reexporta bajo `MAXRECTS_BOARD_ORDERINGS`). No hay duplicación real pese a que a primera vista parezcan dos registros distintos.
- **`search.py::search_best_solution()`** — criterio genérico "más piezas colocadas, luego menor anchura, luego menor longitud" usado por `maxrects_search.py` y `skyline_search.py` para elegir la mejor entre varios candidatos generados internamente. **No debe confundirse** con `CandidatePipeline`/`evaluate()` (el sistema de puntuación ponderado de cara al usuario, ver `docs/scoring.md`): este criterio interno solo sirve para que cada algoritmo elija su mejor intento entre heurísticas/órdenes *antes* de entregar una única `AssemblySolution` al pipeline exterior, que es quien la puntúa de verdad.
- **`beam_search.py`** (genérico, en la raíz de `solver/`) — implementación de beam search independiente del dominio (`State`/`Score` genéricos). Curiosamente, `maxrects/beam.py::search_states()` **no lo usa**: reimplementa su propio bucle de expansión específico para `MaxRectsState`. `beam_search.py` solo está cubierto por su propio test (`test_beam_search.py`) sin otro consumidor en el árbol — candidato a revisar si de verdad hace falta mantener las dos implementaciones.

## Generadores "de una sola solución" vs "de varias"

`GENERATOR_REGISTRY` (`generators.py`) espera funciones `Project -> list[AssemblySolution]`. `skyline`/`maxrects`/`maxrects_beam`/`free_space` internamente calculan **una única** mejor solución (`search_best_solution()` ya eligió la ganadora, o en el caso de `maxrects_beam` el propio beam search) y la envuelven en una lista de un elemento a mano (`return [generate_x_solution(project)]`); `horizontal`/`vertical` sí devuelven varias (todas las permutaciones válidas). No existe un adaptador genérico para el caso "una sola solución" — cada generador escribe su propio `return [...]` de una línea.
