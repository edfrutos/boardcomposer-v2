# Modelo de datos

Modelos de dominio en `src/boardcomposer/domain/`. Todos son `dataclass` (la mayoría `frozen`), sin dependencias de interfaz.

## Board

Tabla disponible como material de partida (`domain/board.py`).

| Campo | Tipo | Descripción |
|---|---|---|
| `length_mm` | `float` | Largo, debe ser > 0. |
| `width_mm` | `float` | Ancho, debe ser > 0. |
| `thickness_mm` | `float` | Grosor, debe ser > 0. |
| `id` | `str \| None` | Identificador opcional. |

Propiedad calculada: `area_mm2`.

## Project

Conjunto de tablas más restricciones (`domain/project.py`). No es `frozen`: `add_board()` muta la lista.

| Campo | Tipo | Descripción |
|---|---|---|
| `boards` | `list[Board]` | Tablas del proyecto. |
| `constraints` | `ProjectConstraints` | Restricciones aplicadas al generar soluciones. |

Propiedad calculada: `total_area_mm2`.

## ProjectConstraints

Restricciones del proyecto (`domain/constraints.py`).

| Campo | Tipo | Descripción |
|---|---|---|
| `max_length_mm` | `float \| None` | Largo máximo admitido para una solución. |
| `max_width_mm` | `float \| None` | Ancho máximo admitido para una solución. |
| `allow_rotation` | `bool` | Permite rotar piezas 90°. |
| `allow_cutting` | `bool` | Permite cortar tablas (no usado aún por los generadores actuales). |

## BoardPlacement

Colocación resuelta de una tabla dentro de una solución (`domain/placement.py`).

| Campo | Tipo | Descripción |
|---|---|---|
| `board_id` | `str` | Referencia al `Board.id` (o `board-N` si no tiene). |
| `x_mm`, `y_mm` | `float` | Esquina inferior-izquierda, ≥ 0. |
| `length_mm`, `width_mm` | `float` | Dimensiones colocadas (intercambiadas si `rotated=True`). |
| `rotated` | `bool` | Si la pieza se colocó girada 90°. |

Propiedades calculadas: `area_mm2`, `right_mm`, `top_mm`.

## AssemblySolution

Una solución completa de composición (`domain/solution.py`). Frozen; se reconstruye (no se muta) en cada etapa del pipeline (validación, evaluación).

| Campo | Tipo | Descripción |
|---|---|---|
| `placements` | `list[BoardPlacement]` | Colocaciones de la solución. |
| `score` | `SolutionScore` | Puntuación (ver `docs/scoring.md`). |
| `explanation` | `SolutionExplanation` | Explicación textual. |

Propiedades calculadas: `used_area_mm2`, `total_length_mm`, `total_width_mm` (a partir de `bounding_rectangle()` sobre los `placements`), `bounding_area_mm2`, `waste_area_mm2`, `waste_ratio`.

## SolutionScore

Desglose de puntuación (`domain/score.py`), todos los campos ≥ 0.

| Campo | Descripción |
|---|---|
| `waste_score` | Aprovechamiento de material ponderado. |
| `material_usage_score` | Proporción de tablas colocadas ponderada. |
| `cuts_score` | Penalización por rotaciones, invertida. |
| `regularity_score` | Compacidad ponderada. |
| `grain_score` | Reservado para veta de madera (no calculado todavía). |

Propiedad calculada: `total` (suma de los cinco campos).

## SolutionExplanation

Explicación en lenguaje natural (`domain/explanation.py`): `strengths`, `weaknesses`, `notes` (listas de `str`).

## Rectangle

Primitiva geométrica compartida (`src/boardcomposer/geometry/rectangle.py`), usada como base de colocaciones y espacios libres.

| Campo | Tipo |
|---|---|
| `x_mm`, `y_mm` | `float` |
| `length_mm`, `width_mm` | `float` |

Propiedades: `right_mm`, `top_mm`, `area_mm2`. Método: `overlaps(other)`.

## Formato de entrada CSV

Cargado por `load_project_from_csv()` (`src/boardcomposer/io/csv_loader.py`). Columnas requeridas:

```
id,length_mm,width_mm,thickness_mm
A,2000,300,20
B,1000,300,20
C,800,250,20
```

`id` es opcional (si falta, `Board.id` queda `None` y el generador asigna `board-N`); el resto son obligatorios y se convierten a `float`. Ejemplo real en `data/samples/basic_boards.csv`.
