# Plugins de BoardComposer

BoardComposer permite ampliar cuatro áreas del Core y una de Studio mediante paquetes Python instalables, sin tocar el código fuente de BoardComposer: **generadores** de disposición, **estrategias** de optimización, **importadores**/**exportadores** de proyectos, y **paneles** de BoardComposer Studio.

El mecanismo es *entry points* estándar de Python (`importlib.metadata`, [PEP 621](https://peps.python.org/pep-0621/)) — el mismo que usan `pytest`, `flake8` o `sphinx` para sus propios plugins. No hay un cargador propio de BoardComposer ni un registro externo: instalar el paquete del plugin en el mismo entorno (`pip install`) es suficiente para que BoardComposer lo detecte en el siguiente arranque.

---

## Cómo funciona

Cada tipo de plugin usa su propio **grupo** de entry point:

| Tipo | Grupo | Forma esperada |
|---|---|---|
| Generador de disposición | `boardcomposer.generators` | `(Project) -> list[AssemblySolution]` |
| Estrategia de optimización | `boardcomposer.strategies` | `() -> OptimizationStrategy` |
| Importador | `boardcomposer.importers` | `(str \| Path) -> Project` |
| Exportador | `boardcomposer.exporters` | `(AssemblySolution) -> str` |
| Panel de Studio | `boardcomposer.studio_panels` | `(StudioServices) -> QWidget` |

En el arranque (o en la primera llamada a `available_generators()`/`available_strategies()`/etc.), BoardComposer resuelve todos los entry points instalados para el grupo correspondiente y los añade al conjunto ya disponible. Dos reglas se cumplen siempre:

- **Un plugin roto nunca bloquea nada.** Si un entry point falla al cargarse (paquete a medio instalar, error de sintaxis, dependencia que falta…), BoardComposer lo ignora y sigue arrancando con normalidad. El fallo queda disponible como `PluginLoadError` (`generator_plugin_errors()`, `strategy_plugin_errors()`, `importer_plugin_errors()`, `exporter_plugin_errors()`) para quien quiera inspeccionarlo — hoy solo Studio lo consume (aviso en la barra de estado al construir paneles).
- **Lo integrado siempre gana.** Si un plugin registra un nombre que ya existe (`"skyline"`, `"balanced"`, `"csv"`, `"svg"`…), BoardComposer usa la versión integrada y descarta la del plugin en silencio. Un plugin nunca puede sustituir una capacidad ya presente en el Core (`DEC-0008`, `docs/masterplan/DOC-005-Decisiones.md`).

Los paneles de Studio son la única excepción: no hay ningún panel integrado que un plugin pueda intentar sustituir (Explorer/Inspector/Timeline/Comparador/Asistente son parte fija de `MainWindow`), pero sí hay 5 nombres reservados que un plugin no puede usar — ver más abajo.

---

## Declarar el entry point

En el `pyproject.toml` de tu paquete de plugin (no en el de BoardComposer):

```toml
[project.entry-points."boardcomposer.generators"]
mi_generador = "mi_paquete.generadores:mi_generador"
```

La clave a la izquierda del `=` (`mi_generador`) es el **nombre** con el que se registra tu plugin — es lo que verá `available_generators()`, lo que se usa en `generator_names` de una estrategia, o en `--strategy`/`GET /strategies` si aplica. El valor de la derecha es la ruta `módulo:atributo` al objeto (función o factoría) que BoardComposer va a cargar.

Después de instalar tu paquete (`pip install -e .` o `pip install mi-paquete`) en el mismo entorno donde corre BoardComposer, el plugin queda disponible sin ningún paso adicional.

---

## Ejemplo mínimo — Generador de disposición

Un generador recibe un `Project` (con sus `boards` y `constraints`) y devuelve una lista de `AssemblySolution` candidatas. BoardComposer las evalúa y puntúa igual que las suyas — el plugin solo aporta geometría, nunca decide cuál es "la mejor".

```python
# mi_paquete/generadores.py
from boardcomposer import Project
from boardcomposer.domain import AssemblySolution


def mi_generador(project: Project) -> list[AssemblySolution]:
    # Ejemplo trivial: una solución sin ninguna tabla colocada.
    # Un generador real recorrería project.boards y construiría
    # BoardPlacement reales — ver src/boardcomposer/solver/skyline_generator.py
    # como referencia de un generador integrado.
    return [AssemblySolution(placements=[])]
```

```toml
[project.entry-points."boardcomposer.generators"]
mi_generador = "mi_paquete.generadores:mi_generador"
```

Verificación:

```python
from boardcomposer.solver.generators import available_generators

assert "mi_generador" in available_generators()
```

---

## Ejemplo mínimo — Estrategia de optimización

Una estrategia es una factoría sin argumentos que devuelve una `OptimizationStrategy`: un nombre, unos pesos de puntuación (`ScoringWeights`) y la lista de generadores (por nombre) que va a usar `GeometrySolver`. La IA (`IDE-0007`) y las estrategias integradas solo ajustan estos parámetros — nunca generan geometría directamente (`DEC-0006`).

```python
# mi_paquete/estrategias.py
from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.strategies import OptimizationStrategy


def mi_estrategia() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="mi_estrategia",
        weights=ScoringWeights(
            material_utilization=50.0,
            placed_boards=30.0,
            compactness=15.0,
            rotation_penalty=5.0,
        ),
        # Puede combinar generadores integrados y de plugins por nombre.
        generator_names=("horizontal", "vertical", "mi_generador"),
    )
```

```toml
[project.entry-points."boardcomposer.strategies"]
mi_estrategia = "mi_paquete.estrategias:mi_estrategia"
```

Verificación:

```python
from boardcomposer.solver.strategies import strategy_by_name

strategy = strategy_by_name("mi_estrategia")
assert strategy.name == "mi_estrategia"
```

---

## Ejemplo mínimo — Importador

Un importador recibe una ruta (`str` o `Path`) y devuelve un `Project` ya construido — mismo contrato que `load_project_from_csv()`/`load_project_from_excel()`.

```python
# mi_paquete/importadores.py
from pathlib import Path

from boardcomposer import Board, Project


def mi_importador(path: str | Path) -> Project:
    project = Project()
    # Un importador real parsearía `path` (JSON, XML, un ERP propio...).
    project.add_board(Board(length_mm=1200, width_mm=600, thickness_mm=18, id="A"))
    return project
```

```toml
[project.entry-points."boardcomposer.importers"]
mi_formato = "mi_paquete.importadores:mi_importador"
```

Verificación:

```python
from boardcomposer.io import importer_by_name

importer = importer_by_name("mi_formato")
project = importer("cualquier-ruta")
```

---

## Ejemplo mínimo — Exportador

Un exportador recibe una `AssemblySolution` ya resuelta y devuelve el contenido serializado como `str` — mismo contrato que `solution_to_svg()`/`solution_to_dxf()`.

```python
# mi_paquete/exportadores.py
from boardcomposer.domain import AssemblySolution


def mi_exportador(solution: AssemblySolution) -> str:
    lineas = [f"tablas colocadas: {len(solution.placements)}"]
    for placement in solution.placements:
        lineas.append(f"{placement.board_id} en ({placement.x_mm}, {placement.y_mm})")
    return "\n".join(lineas)
```

```toml
[project.entry-points."boardcomposer.exporters"]
mi_formato = "mi_paquete.exportadores:mi_exportador"
```

Verificación:

```python
from boardcomposer.export import exporter_by_name

exporter = exporter_by_name("mi_formato")
```

---

## Ejemplo mínimo — Panel de Studio

A diferencia de los cuatro anteriores, un panel de Studio vive fuera del Core: su factoría recibe los `StudioServices` compartidos de la ventana y devuelve un `QWidget` (PySide6) que se añade como un nuevo `QDockWidget` en el área derecha, con su propia entrada de mostrar/ocultar en el menú "Ver".

```python
# mi_paquete/panel.py
from PySide6.QtWidgets import QLabel, QWidget

from studio.services import StudioServices


def mi_panel(services: StudioServices) -> QWidget:
    return QLabel(f"Proyecto activo: {services.projects.current_project}")
```

```toml
[project.entry-points."boardcomposer.studio_panels"]
"Métricas" = "mi_paquete.panel:mi_panel"
```

El nombre del entry point (`Métricas` en este ejemplo) es también el título del dock y de la entrada de menú — no puede coincidir con ninguno de los 5 nombres reservados: `Explorer`, `Inspector`, `Timeline`, `Comparador`, `Asistente`. Si coincide, si el entry point falla al cargarse, o si la factoría lanza una excepción al construir el widget, Studio ignora ese panel con un aviso en la barra de estado — nunca bloquea el arranque del resto de la aplicación.

Nota de TOML: una clave de entry point con espacios, tildes u otros caracteres fuera de `[A-Za-z0-9_-]` debe ir entre comillas (`"Métricas" = ...`, no `Métricas = ...`) — si no, `pip install` falla con un `TOMLDecodeError` antes de llegar siquiera a BoardComposer.

---

## Referencia rápida

| Grupo | Registro integrado | Módulo del Core/Studio |
|---|---|---|
| `boardcomposer.generators` | `GENERATOR_REGISTRY` (`horizontal`, `vertical`, `free_space`, `skyline`, `maxrects`, `maxrects_beam`) | `src/boardcomposer/solver/generators.py` |
| `boardcomposer.strategies` | `STRATEGY_FACTORIES` (`balanced`, `material`, `compact`) | `src/boardcomposer/solver/strategies.py` |
| `boardcomposer.importers` | `IMPORTER_REGISTRY` (`csv`, `xlsx`) | `src/boardcomposer/io/registry.py` |
| `boardcomposer.exporters` | `EXPORTER_REGISTRY` (`svg`, `dxf`) | `src/boardcomposer/export/registry.py` |
| `boardcomposer.studio_panels` | — (sin paneles integrados que fusionar) | `studio/panel_plugins.py` |

Para el mecanismo de descubrimiento en sí (`discover_plugins()`, `PluginLoadError`), ver `src/boardcomposer/plugins/discovery.py` y `docs/architecture.md`.
