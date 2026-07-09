# Algoritmos

Todos los algoritmos viven en `src/boardcomposer/solver/` y comparten la misma firma: reciben un `Project` y devuelven una o varias `AssemblySolution` (sin puntuar ni validar — eso ocurre después, en el pipeline).

## Registro de generadores

`solver/generators.py` expone un registro por nombre (`GENERATOR_REGISTRY`) que `generators_by_name()` resuelve a funciones:

| Nombre | Función | Nº de soluciones |
|---|---|---|
| `horizontal` | `generate_horizontal_permutations()` | Una por permutación (o 1 si hay más de 6 tablas). |
| `vertical` | `generate_vertical_permutations()` | Igual que `horizontal`, en vertical. |
| `free_space` | `generate_free_space_solution()` | 1 |
| `skyline` | `generate_skyline_solution()` | 1 (la mejor encontrada) |
| `maxrects` | `generate_maxrects_solution()` | 1 (la mejor encontrada) |
| `maxrects_beam` | `generate_beam_maxrects_solution(beam_width=4)` | 1 (la mejor encontrada, vía beam search) |

Qué generadores se ejecutan depende de la `OptimizationStrategy` elegida (ver `docs/scoring.md`).

## Horizontal / Vertical (fuerza bruta)

`solver/layout_generator.py`. Coloca las tablas una tras otra a lo largo de un eje (X para horizontal, Y para vertical), sin huecos entre ellas. `generate_horizontal_permutations()`/`generate_vertical_permutations()` generan **todas** las permutaciones del orden de las tablas (`itertools.permutations`) mientras `len(project.boards) <= 6`; por encima de ese límite devuelven una única solución con el orden original, para evitar explosión combinatoria (6! = 720).

## Free Space

`solver/free_space_generator.py`. Calcula el área máxima (`max_length_mm`/`max_width_mm` de las restricciones, o el total de las tablas si no hay límite) y usa `FreeSpaceManager` + `place_board_in_first_space()` (`src/boardcomposer/layout/`) para colocar cada tabla en el primer hueco libre que la admite, en el orden en que aparece en el proyecto. Las tablas que no caben se omiten silenciosamente.

## Skyline

`solver/skyline_generator.py` → `solver/skyline_search.py` → `solver/skyline/skyline.py`.

Mantiene una línea de "perfil superior" (`SkylineNode`: segmentos `x_mm`/`width_mm` con su altura `y_mm`) inicializada como un único segmento a la altura 0. Para cada tabla:

1. `_find_best_candidate()` recorre los nodos del perfil y calcula, para cada punto de partida posible, la altura resultante y la fragmentación (número de nodos que cubre) si la tabla se apoya ahí.
2. Si `allow_rotation` está activo, se prueba también la tabla girada 90° y se compara con la orientación normal.
3. `_choose_candidate()` elige el candidato con menor `(altura resultante, fragmentación, y, x)` — minimiza primero cuánto sube el perfil, y como desempate prefiere menos fragmentación y las posiciones más bajas/izquierda.
4. `place()` actualiza el perfil: divide los nodos cubiertos, inserta un nuevo segmento a la altura de la pieza colocada y fusiona (`_merge_adjacent_nodes()`) los segmentos adyacentes que quedan a la misma altura.

`skyline_runner.py`/`skyline_search.py` repiten este proceso probando distintos órdenes de tablas (`board_ordering.py`: orden original, mayor área primero, lado más largo primero) y se quedan con la mejor solución encontrada.

## MaxRects

`solver/maxrects_generator.py` → `solver/maxrects_search.py` → `solver/maxrects/maxrects.py`.

Mantiene una lista de rectángulos libres (`FreeRectangle`), inicializada con un único rectángulo del tamaño total del tablero. Para cada tabla:

1. `find_candidates()` recorre los rectángulos libres y genera un candidato de colocación por cada uno donde la tabla quepa (normal y, si `allow_rotation`, girada).
2. `find_best_rectangle()` aplica una heurística (`solver/maxrects/heuristics.py`; por defecto `best_area_fit`, que minimiza el área desperdiciada) para elegir el mejor candidato.
3. `place_candidate()` actualiza el estado: divide (`_split_free_rectangle`) los rectángulos libres que solapan con la pieza colocada, resuelve solapes redundantes entre fragmentos (`_resolve_overlaps`/`_split_overlap`) y elimina (`_prune_free_rectangles`) los rectángulos contenidos por completo en otro.

### Variante Beam Search

`solver/maxrects_beam_runner.py` combina MaxRects con `solver/beam_search.py` (búsqueda genérica de haz: en cada profundidad expande el estado actual y conserva solo los `width` mejores según una función de puntuación). `search_states()` (`solver/maxrects/beam.py`) expande, para cada tabla pendiente, todas las heurísticas de `MAXRECTS_HEURISTICS` y todos los órdenes de `MAXRECTS_BOARD_ORDERINGS`, puntuando cada estado con `score_state()` — esto explora más combinaciones heurística/orden que la versión "greedy" simple, a cambio de más coste computacional. Registrada en `GENERATOR_REGISTRY` como `maxrects_beam` con `beam_width=4` (mismo valor usado en `workbench/app.py` y `tools/visualize_demo.py`); no forma parte de ninguna `OptimizationStrategy` por defecto, hay que seleccionarla explícitamente.

## Pipeline de candidatos

`solver/candidate_pipeline.py` (`CandidatePipeline.run()`, invocado por `GeometrySolver.solve()`) encadena:

```
generadores de la estrategia
  → respects_constraints()      (descarta soluciones que excedan max_length_mm/max_width_mm)
  → deduplicate_solutions()     (descarta soluciones con idéntica firma de colocaciones)
  → evaluate()                  (calcula el SolutionScore, ver docs/scoring.md)
  → sorted(key=score.total, reverse=True)
```

El resultado es la lista de `AssemblySolution` ordenada de mejor a peor, que consume el CLI (`--top N`) o BoardComposer Studio.
