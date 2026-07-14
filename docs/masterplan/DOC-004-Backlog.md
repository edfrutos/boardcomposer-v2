# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 01/07/2026

---

## Objetivo

Mantener un registro único, priorizado y trazable de todas las funcionalidades, mejoras, ideas e iniciativas previstas para BoardComposer.

El Backlog constituye la fuente oficial de trabajo del proyecto y evoluciona de forma continua.

---

## Principios

- Ninguna idea se pierde.
- Ninguna funcionalidad se implementa sin pasar previamente por el Backlog.
- Toda entrada debe tener un identificador único.
- La prioridad puede cambiar; la trazabilidad nunca.

---

## Estados

- ⚪ Idea
- 🔵 Planificada
- 🟡 En desarrollo
- 🟢 Completada
- 🔴 Bloqueada
- ⚫ Descartada

---

## Prioridades

- **P0** — Crítica
- **P1** — Alta
- **P2** — Media
- **P3** — Baja

---

## Formato de una entrada

```text
ID: IDE-0001
Título:
Estado:
Prioridad:
Impacto:
Esfuerzo:
Dependencias:
Documentos relacionados:
Descripción:
Criterios de aceptación:
Observaciones:
```

---

## Backlog inicial

| ID | Título | Estado | Prioridad |
|----|--------|--------|-----------|
| IDE-0001 | Workspace interactivo | 🟢 | P0 |
| IDE-0002 | Comparador de algoritmos | 🟢 | P0 |
| IDE-0003 | Inspector de piezas | 🟢 | P0 |
| IDE-0004 | Gestión de proyectos | 🟢 | P1 |
| IDE-0005 | Exportación PDF/SVG | 🟢 | P1 |
| IDE-0006 | API pública | 🟢 | P2 |
| IDE-0007 | Asistente IA | 🟢 | P2 |
| IDE-0008 | Sistema de plugins | 🟢 | P3 |
| IDE-0009 | Endurecimiento para producción | 🟢 | P0 |
| IDE-0010 | Importación desde Excel | 🟢 | P1 |
| IDE-0011 | Empaquetado de Studio | 🟢 | P1 |

---

## IDE-0007 — Asistente IA

**Estado:** 🟢 Completado (Fases A–F), incluyendo un proveedor de IA real: `AnthropicProvider` (`src/boardcomposer/ai/anthropic_provider.py`, SDK `anthropic`, modelo `claude-haiku-4-5`, API key vía variable de entorno `ANTHROPIC_API_KEY` — la resuelve el propio SDK con `Anthropic()`). `default_provider()` (`src/boardcomposer/ai/registry.py`) usa `AnthropicProvider` si hay `ANTHROPIC_API_KEY` en el entorno, si no cae a `MockAIProvider`; es el valor por defecto tanto de `create_app()` (`api.py`) como de `AssistantService` (Studio). Las capacidades que necesitan una respuesta JSON estructurada (`project_from_text()`, `suggest_strategy()`) ya dan resultados útiles con este proveedor, verificado con llamadas reales: se encontraron y corrigieron dos comportamientos reales de Claude que `MockAIProvider` nunca había ejercitado — envolver el JSON en un bloque ` ```json ... ``` ` pese a que el prompt pide lo contrario (`strip_json_fence()`, `json_response.py`) y devolver `thickness_mm: null` explícito en vez de omitir la clave cuando el texto no menciona grosor.

Alcance dividido en fases, cada una construida sobre la anterior:

- **Fase A** (🟢 completada) — puerto `AIProvider` en el Core (`src/boardcomposer/ai/`) con `MockAIProvider`, `AnthropicProvider` y `provider_by_name()`/`default_provider()`.
- **Fase B** (🟢 completada) — `project_from_text()` (`src/boardcomposer/ai/project_from_text.py`): genera un `Project` a partir de texto libre, pidiendo al `AIProvider` un JSON con la misma forma que ya valida `/solve` en la API.
- **Fase C** (🟢 completada) — `explain_solution()` (`src/boardcomposer/ai/explain_solution.py`): pide al `AIProvider` una explicación en lenguaje natural de un `AssemblySolution`, a partir de sus métricas (tablas colocadas, dimensiones, desperdicio, puntuación) y de `SolutionExplanation` (fortalezas/debilidades/notas).
- **Fase D** (🟢 completada) — `suggest_strategy()` (`src/boardcomposer/ai/suggest_strategy.py`): a partir de un objetivo en lenguaje natural, pide al `AIProvider` unos pesos de puntuación (`ScoringWeights`) y generadores de disposición, y construye una `OptimizationStrategy` que `GeometrySolver` ejecuta igual que `balanced`/`material`/`compact`. La IA solo ajusta parámetros del solver determinista existente — nunca genera geometría directamente, para no comprometer la validez de las disposiciones.
- **Fase E** (🟢 completada) — `AssistantService`/`render_chat()` (`studio/assistant_service.py`, `studio/panels/chat_panel.py`): chat de ayuda contextual, nuevo dock "Asistente" en Studio. Envía la pregunta del usuario más el contexto del proyecto abierto directamente a `AIProvider.complete()` (conversación libre, sin pasar por `project_from_text()`/`explain_solution()`/`suggest_strategy()`).
- **Fase F** (🟢 completada) — `POST /assist/project`, `POST /assist/strategy`, `POST /assist/explain` (`src/boardcomposer/api.py`): exponen las Fases B, D y C respectivamente vía HTTP, con la misma validación de `boards`/`constraints` que ya usa `/solve`. `create_app(ai_provider=None)` acepta un `AIProvider` inyectable (por defecto `default_provider()`).

---

## IDE-0008 — Sistema de plugins

**Estado:** 🟢 Completado (Fases A–E). A diferencia de `IDE-0007`, introduce ejecución de código de terceros dentro de la aplicación (paquetes Python instalables, registrados vía *entry points*).

Alcance dividido en fases, cada una construida sobre la anterior:

- **Fase A** (🟢 completada) — `discover_plugins(group)` (`src/boardcomposer/plugins/discovery.py`): resuelve los *entry points* instalados para un grupo dado (`importlib.metadata.entry_points()`) en un diccionario `nombre -> objeto`, junto a una lista de `PluginLoadError` para los que fallan al cargar sin bloquear al resto.
- **Fase B** (🟢 completada) — `available_generators()`/`generator_plugin_errors()` (`src/boardcomposer/solver/generators.py`): generadores de disposición registrados por plugins (grupo `boardcomposer.generators`) junto a los 6 ya existentes en `GENERATOR_REGISTRY`, que siempre gana si un plugin repite un nombre. `generators_by_name()` (usado por `CandidatePipeline`) y `suggest_strategy()` (`IDE-0007` Fase D) ya resuelven contra este conjunto ampliado.
- **Fase C** (🟢 completada) — `available_strategies()`/`strategy_plugin_errors()` (`src/boardcomposer/solver/strategies.py`): estrategias de optimización registradas por plugins (grupo `boardcomposer.strategies`) junto a `balanced`/`material`/`compact` en `STRATEGY_FACTORIES`, que siempre gana si un plugin repite un nombre. `strategy_by_name()` y `GET /strategies` en la API ya resuelven contra este conjunto ampliado.
- **Fase D** (🟢 completada) — `available_importers()`/`importer_by_name()` (`src/boardcomposer/io/registry.py`) y `available_exporters()`/`exporter_by_name()` (`src/boardcomposer/export/registry.py`): importadores/exportadores registrados por plugins (grupos `boardcomposer.importers`/`boardcomposer.exporters`) junto a `"csv"`/`"svg"`, que siempre ganan si un plugin repite un nombre. A diferencia de B y C, no había un mecanismo existente de selección por nombre en CLI/API/Studio al que enchufarse — queda como infraestructura lista para usarse cuando se necesite.
- **Fase E** (🟢 completada) — `discover_panel_plugins()` (`studio/panel_plugins.py`) y `MainWindow._build_plugin_panels()`: paneles de Studio registrados por plugins (grupo `boardcomposer.studio_panels`, factoría `(services) -> QWidget`). Cada panel añade un `QDockWidget` y su acción de mostrar/ocultar al menú "Ver" (antes vacío). Sin capacidad integrada que fusionar (a diferencia de B/C/D): Explorer/Inspector/Timeline/Comparador/Asistente son parte fija de `MainWindow`, no plugins; un plugin que repita uno de esos 5 nombres, falle al cargarse o falle al construir su widget se ignora con aviso en la barra de estado, sin bloquear el arranque de Studio.

---

## IDE-0009 — Endurecimiento para producción

**Estado:** 🟢 Completado. Cierra el punto P0 de `DOC-003-Roadmap.md` ("Servicios remotos" de la Fase 3 — Plataforma): la API deja de ser exclusivamente el servidor de desarrollo de Flask sin auth ni rate limiting.

- Autenticación por clave de API: `create_app(api_key=None)` (`src/boardcomposer/api.py`), por defecto `os.environ.get("BOARDCOMPOSER_API_KEY")`. Si está definida, todas las rutas salvo `/health` exigen esa clave en la cabecera `X-API-Key` (`401` si falta o no coincide, vía `@app.before_request`); si no está definida, sin autenticación — mismo comportamiento que antes de esta fase.
- Rate limiting con `Flask-Limiter`: `create_app(rate_limit=None)`, por defecto `"60 per minute"` por IP en todas las rutas salvo `/health` (`@limiter.exempt`); `429` con el mismo formato `jsonify(error=...)` que el resto de la API. Almacenamiento en memoria (`storage_uri="memory://"`) — no compartido entre workers de `gunicorn` (`DOC-006-DeudaTecnica.md`, DT-0010).
- Servidor WSGI de producción: `gunicorn` como dependencia opcional (`pip install -e ".[prod]"`), invocado vía su soporte de *app factory* (`gunicorn "boardcomposer.api:create_app()"`, `make serve`) en vez del servidor de desarrollo de Flask.
- Verificado con `gunicorn` real (no solo tests): `/health` sin clave, `/strategies` rechazado sin clave (`401`) y aceptado con la clave correcta.

---

## IDE-0010 — Importación desde Excel

**Estado:** 🟢 Completado. Cierra RF-002 (`docs/requirements.md`), que cubría CSV y Excel pero solo tenía CSV implementado.

- `load_project_from_excel()` (`src/boardcomposer/io/excel_loader.py`, SDK `openpyxl`, modo `read_only=True`): mismas columnas obligatorias que `load_project_from_csv()` (`id`/`length_mm`/`width_mm`/`thickness_mm`), primera hoja del `.xlsx`, primera fila como cabecera; ignora filas finales completamente vacías.
- Registrado en `IMPORTER_REGISTRY` (`src/boardcomposer/io/registry.py`) como `"xlsx"`, junto a `"csv"` — `importer_by_name()`/`available_importers()` ya lo resuelven sin cambios adicionales (infraestructura de `IDE-0008` Fase D).
- CLI: nuevo flag `--excel`, mutuamente excluyente con `--csv` (`argparse.add_mutually_exclusive_group()`).
- Fichero de muestra `data/samples/basic_boards.xlsx`, mismos datos que `basic_boards.csv`, para tests y demos.
- Fuera de alcance (igual que CSV hoy): no está expuesto ni en la API ni en Studio — ambos solo aceptan datos inline (`/solve`) o el propio formato `.bcstudio.json` de Studio.

---

## IDE-0011 — Empaquetado de Studio

**Estado:** 🟢 Completado. Cierra el punto P1 de `DOC-003-Roadmap.md` ("Empaquetado y distribución de Studio") y `DT-0008` (`docs/masterplan/DOC-006-DeudaTecnica.md`): Studio deja de ejecutarse exclusivamente desde código fuente.

- Nuevo punto de entrada `boardcomposer-studio = "studio.app:main"` (`pyproject.toml`) — hasta ahora Studio no tenía ninguna forma documentada de lanzarse fuera de invocar `studio/app.py` directamente.
- Empaquetado con `pyside6-deploy` (herramienta oficial de PySide6, basada en Nuitka): genera un `.app` nativo de macOS (arm64), modo `--standalone --macos-create-app-bundle` (el que usa macOS por defecto independientemente de `mode` en el `.spec`).
- Configuración en `studio/pysidedeploy.spec`: `exec_directory = ./dist` (salida en `studio/dist/BoardComposerStudio.app`, fuera del árbol de código fuente). `icon`/`python_path` se dejan en blanco a propósito — son rutas específicas de la máquina que generó el build; `python_path` se sobrescribe en cada ejecución con el intérprete activo (`Config.set_or_fetch`), e `icon` cae al icono por defecto de PySide6 si se deja en blanco. `studio/dist/`/`studio/deployment/` (build intermedio de Nuitka) ignorados en git.
- `make package` (Makefile) para generarlo localmente; dependencia opcional `nuitka` bajo `pip install -e ".[package]"`.
- CI (`.github/workflows/package-studio.yml`, `runs-on: macos-latest`): al crear un tag `v*`, corre los tests, compila el `.app`, lo comprime con `ditto` y lo publica como asset de una release de GitHub (`gh release create`/`upload`) para ese tag.
- Verificado con una compilación real (no solo el `--dry-run`): `.app` de 161 MB, arm64, lanzado con `open` y confirmado como proceso Qt vivo (sin crash reports) — no solo revisión del binario.
- Fuera de alcance: sin firma ni notarización de Apple, solo macOS/arm64 (`DT-0011`, `docs/masterplan/DOC-006-DeudaTecnica.md`).

---

## Reglas de mantenimiento

- Cada nueva idea comienza como **IDE**.
- Cuando una idea se aprueba para desarrollo, se vinculará a una Épica (EP) y posteriormente a uno o varios Sprints (SPR).
- Las funcionalidades completadas permanecerán en este documento como histórico.
- Ninguna entrada se elimina; únicamente cambia de estado.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- incorporar las primeras Épicas (EP);
- enlazar el Roadmap con el Backlog;
- definir el flujo completo Idea → Épica → Sprint → Implementación → Liberación.
