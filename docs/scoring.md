# Puntuación

La puntuación vive en `src/boardcomposer/solver/`: métricas independientes en `objectives.py`, combinación ponderada en `evaluation.py` y pesos configurables en `scoring_weights.py`.

## Métricas (`objectives.py`)

Funciones puras, cada una calculada sobre una `AssemblySolution`:

| Métrica | Fórmula | Rango |
|---|---|---|
| `material_utilization()` | `used_area_mm2 / bounding_area_mm2` | 0–1 |
| `compactness()` | `min(largo, ancho) / max(largo, ancho)` del rectángulo envolvente | 0–1 (1 = cuadrado perfecto) |
| `rotation_ratio()` | proporción de piezas colocadas con `rotated=True` | 0–1 |
| `placed_board_ratio(solution, total_boards)` | `len(placements) / total_boards` | 0–1 |

Todas devuelven `0.0` en los casos degenerados (sin colocaciones, área cero).

## Pesos (`scoring_weights.py`)

`ScoringWeights` define cuánto pesa cada métrica en la puntuación final:

| Campo | Peso por defecto (`balanced()`) |
|---|---|
| `material_utilization` | 40.0 |
| `placed_boards` | 30.0 |
| `compactness` | 20.0 |
| `rotation_penalty` | 10.0 |

Presets alternativos:

- `material_first()`: prioriza aprovechamiento de material (60/25/10/5).
- `compact_first()`: prioriza composiciones compactas (30/20/45/5).

## Cálculo (`evaluate()`)

`evaluate(solution, total_boards, weights)` reconstruye la `AssemblySolution` con un nuevo `SolutionScore`:

```
waste_score            = material_utilization(solution) * weights.material_utilization
material_usage_score   = placed_board_ratio(solution, total_boards) * weights.placed_boards
regularity_score        = compactness(solution) * weights.compactness
rotation_penalty        = rotation_ratio(solution) * weights.rotation_penalty
cuts_score              = max(0.0, 10.0 - rotation_penalty)
```

`SolutionScore.total` es la suma de `waste_score + material_usage_score + cuts_score + regularity_score` (`grain_score` existe en el modelo pero `evaluate()` no lo rellena todavía — reservado para una futura métrica de veta de madera). Las soluciones del pipeline se ordenan por `score.total` descendente.

## Explicación textual

`evaluate()` genera además una `SolutionExplanation` con reglas fijas (no derivadas de los pesos):

- Fortaleza *"Muy buen aprovechamiento del material"* si `material_utilization >= 0.90`.
- Debilidad *"Aprovechamiento bajo del material"* si `material_utilization < 0.70`.
- Fortaleza *"Composición compacta"* si `compactness >= 0.50`, debilidad *"Composición alargada o poco compacta"* en caso contrario.

## Estrategias (`solver/strategies.py`)

Una `OptimizationStrategy` combina un juego de pesos con los generadores a ejecutar (`solver/generators.py`, ver `docs/algorithms.md`):

| Estrategia | Pesos | Generadores |
|---|---|---|
| `balanced` (por defecto) | `balanced()` | `horizontal`, `vertical`, `free_space` |
| `material` | `material_first()` | `horizontal`, `vertical`, `free_space`, `skyline`, `maxrects` |
| `compact` | `compact_first()` | `vertical`, `free_space` |

Seleccionable por nombre con `strategy_by_name()` (CLI: `--strategy {balanced,material,compact}`).
