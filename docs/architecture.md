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
     ┌──────────────────┼───────────────────┬──────────┬──────────┐
     ▼                  ▼                   ▼          ▼          ▼
  domain/            solver/            io/, export/,  ai/     plugins/
     │                  │               presenters/    │          │
     └──────────────────┼───────────────────┴──────────┴──────────┘
                         ▼
                  geometry/, layout/
```

## Core (`src/boardcomposer/`)

- **`domain/`** — modelos inmutables: `Board`, `Project`, `ProjectConstraints`, `BoardPlacement`, `AssemblySolution`, `SolutionScore`, `SolutionExplanation` (ver `docs/data_model.md`). Sin dependencias de `solver`, `io` ni interfaz alguna.
- **`geometry/`** — primitiva `Rectangle` y utilidades de colisión/transformación, compartidas por `domain` y `solver`.
- **`layout/`** — gestión de espacio libre (`FreeSpaceManager`, `place_board_in_first_space`) usada por el generador `free_space`.
- **`solver/`** — generadores de layout, validación de restricciones, deduplicación y evaluación (ver `docs/algorithms.md` y `docs/scoring.md`). `GeometrySolver` (en `solver/geometry_solver.py`) es el punto de entrada: envuelve `CandidatePipeline` con una `OptimizationStrategy`. `strategy_by_name()` resuelve tanto las 3 estrategias integradas (`balanced`/`material`/`compact`) como las registradas por plugins (`IDE-0008` Fase C, ver `plugins/` más abajo).
- **`io/`** — `load_project_from_csv()` y `load_project_from_excel()` (`excel_loader.py`, SDK `openpyxl`, `IDE-0010`), las dos fuentes de importación integradas (RF-002 ya cubre ambos formatos). Mismas columnas obligatorias que el CSV (`id`/`length_mm`/`width_mm`/`thickness_mm`) en la primera hoja del `.xlsx`, primera fila como cabecera; ignora cualquier fila completamente vacía, no solo las finales (`workbook.active.iter_rows()` a veces incluye huecos intermedios por el rango usado de la hoja). `importer_by_name()` resuelve `"csv"`/`"xlsx"` más los importadores registrados por plugins (`IDE-0008` Fase D, ver `plugins/` más abajo).
- **`export/`** — `solution_to_svg()` y `solution_to_dxf()` (`dxf_exporter.py`, SDK `ezdxf`, `IDE-0012`): un `LWPolyline` cerrado por tabla colocada más una etiqueta de texto (`board_id`), mismo criterio visual que el SVG. `exporter_by_name()` resuelve `"svg"`/`"dxf"` más los exportadores registrados por plugins (`IDE-0008` Fase D).
- **`presenters/`** — `solution_to_text()` y `solutions_to_json()`, formateo de resultados para el CLI.
- **`ai/`** — cubre las Fases A, B, C y D de `IDE-0007` (`docs/masterplan/DOC-004-Backlog.md`). Fase A: puerto `AIProvider` (`ABC`, mismo patrón que `Presenter`) con un único método `complete(prompt: str) -> str`; `MockAIProvider` (sin llamadas externas) y `AnthropicProvider` (SDK `anthropic`, modelo `claude-haiku-4-5`, API key vía `ANTHROPIC_API_KEY`) como implementaciones; `provider_by_name()` resuelve el proveedor por nombre (mismo patrón que `strategy_by_name()`) y `default_provider()` elige `AnthropicProvider` si hay `ANTHROPIC_API_KEY` en el entorno, si no `MockAIProvider`. Fase B: `project_from_text()` (`project_from_text.py`) construye un `Project` a partir de texto libre — pide al `AIProvider` un JSON con la misma forma que ya valida `/solve` en la API (`boards`/`constraints`) y reutiliza esa misma validación; si la respuesta no es interpretable lanza `ProjectFromTextError`. Antes de parsear, pasa la respuesta por `strip_json_fence()` (`json_response.py`, también usado por `suggest_strategy()`): verificado contra `AnthropicProvider` real, Claude suele envolver el JSON en un bloque ` ```json ... ``` ` pese a que el prompt pide explícitamente "sin texto adicional". `thickness_mm` también trata un `null` explícito igual que una clave ausente (Claude incluye la clave con `null` cuando el texto no menciona grosor, no la omite). Fase C: `explain_solution()` (`explain_solution.py`) pide al `AIProvider` una explicación en lenguaje natural de un `AssemblySolution`, a partir de sus métricas (tablas colocadas, dimensiones, desperdicio, puntuación) y de `SolutionExplanation`; a diferencia de `project_from_text()`, aquí la salida es texto libre sin parseo. Fase D: `suggest_strategy()` (`suggest_strategy.py`) traduce un objetivo en lenguaje natural en una `OptimizationStrategy` (pesos de `solver/scoring_weights.py` + `generator_names` validados contra `solver.generators.available_generators()`) que `GeometrySolver` ejecuta igual que las estrategias predefinidas — la IA nunca genera geometría directamente, solo ajusta los parámetros del solver determinista. La Fase E (chat contextual, ver sección Studio) consume directamente `AIProvider.complete()` en vez de estas funciones específicas; la Fase F (ver sección API) expone las Fases B, C y D vía HTTP.
- **`plugins/`** — cubre la Fase A de `IDE-0008` (`docs/masterplan/DOC-004-Backlog.md`): `discover_plugins(group)` resuelve los *entry points* de Python instalados para un grupo dado (`importlib.metadata.entry_points()`) en un diccionario `nombre -> objeto cargado`, junto a una lista de `PluginLoadError` para los que fallan al cargar — un plugin de terceros roto no bloquea a los demás ni a la aplicación. La Fase B (`solver/generators.py`) es la primera capacidad construida encima: `available_generators()` = `GENERATOR_REGISTRY` (los 6 generadores integrados) + los registrados por plugins en el grupo `boardcomposer.generators`, con los integrados siempre ganando si un plugin repite un nombre; `generators_by_name()` y `suggest_strategy()` (Fase D de `IDE-0007`) ya resuelven contra este conjunto ampliado. Fase C (`solver/strategies.py`), mismo patrón: `available_strategies()` = `STRATEGY_FACTORIES` (`balanced`/`material`/`compact`) + plugins del grupo `boardcomposer.strategies`; `strategy_by_name()` y `GET /strategies` en la API ya resuelven contra este conjunto ampliado. Fase D (`io/registry.py`, `export/registry.py`), mismo patrón otra vez, pero es la primera capacidad de `IDE-0008` sin un punto de integración previo en CLI/API/Studio (a diferencia de B y C, que se enchufaron en mecanismos ya existentes — `generator_names`/`--strategy`): `importer_by_name()`/`exporter_by_name()` resuelven `"csv"`/`"svg"` más lo registrado en los grupos `boardcomposer.importers`/`boardcomposer.exporters`, listos para cuando haga falta exponerlos. Fase E (`studio/panel_plugins.py`, ver sección Studio) cierra `IDE-0008`: paneles de Studio como plugins, sobre el grupo `boardcomposer.studio_panels` — sin capacidad integrada que fusionar, a diferencia de B/C/D. Guía para desarrolladores de plugins (`IDE-0013`), con un ejemplo mínimo funcional por cada uno de los 5 grupos: `docs/plugins.md`.

## CLI (`src/boardcomposer/cli.py`)

Consume el Core directamente: carga un `Project` (desde CSV, Excel o `build_demo_project()`; `--csv`/`--excel` son mutuamente excluyentes), construye una `OptimizationStrategy` por nombre y llama a `GeometrySolver(project, strategy).solve()`. Sin lógica propia de negocio — es una interfaz fina sobre el Core, tal como exige el principio arquitectónico.

Subcomando `boardcomposer plugins` (`--json` opcional): visibilidad de plugins instalados, misma fuente que `GET /plugins` en la API (`plugin_visibility.plugin_summary()`). Opcional (`add_subparsers(dest="command")`, no `required`), así que no rompe la invocación sin subcomando que ya usan `--csv`/`--excel`/etc.

La carga del fichero de entrada va envuelta en `try/except`: `LoaderError` (fichero malformado, con el número de fila) y `OSError` (fichero inexistente o ilegible) se convierten en una línea legible por stderr y `SystemExit(1)`, en vez del traceback de Python que salía antes. `LoaderError` (`io/errors.py`) hereda de `ValueError`, así que quien ya capturaba `ValueError` alrededor de los cargadores sigue funcionando.

Referencia de usuario de la línea de comandos (opciones, formato de entrada, salida, códigos de salida): `docs/cli.md`.

## API (`src/boardcomposer/api.py`)

Cubre `IDE-0006` y la Fase F de `IDE-0007` (`docs/masterplan/DOC-004-Backlog.md`). Primer contrato HTTP mínimo sobre el Core (Flask, ya declarado en `pyproject.toml`) — mismo papel que `cli.py`, sin lógica propia: traduce peticiones a las mismas llamadas que ya usan CLI y Studio (`Project`/`ProjectConstraints`/`GeometrySolver`/`solutions_to_json`, y ahora también `boardcomposer.ai`). `_parse_boards()`/`_parse_constraints()`/`_parse_top()`/`_solve_response()` son helpers internos que factorizan la validación que `/solve` y los `/assist/*` comparten.

`MAX_BOARDS = 100` limita `boards` en `/solve`, `/assist/strategy` y `/assist/explain` (`400` si se supera). No protege contra combinatoria — `generate_horizontal_permutations()`/`generate_vertical_permutations()` ya se limitan solas a 6 tableros internamente (`layout_generator.py`, sin relación con esta constante) — sino contra el coste, más difuso pero real, de `GeometrySolver` con proyectos grandes: medido empíricamente, 100 tableros resuelven en ~1s, 200 en ~7s, 300+ no termina en un tiempo razonable.

| Ruta | Método | Qué hace |
|---|---|---|
| `/health` | GET | Comprobación trivial de que el servicio responde. |
| `/strategies` | GET | Lista las estrategias registradas: `balanced`/`material`/`compact` más las que aporten plugins instalados (`IDE-0008` Fase C). |
| `/plugins` | GET | Visibilidad de plugins instalados (`DOC-999-Ideas.md`, Marketplace/Comunidad): plugins de terceros detectados y errores de carga, por cada uno de los 4 grupos de entry point del Core (generadores, estrategias, importadores, exportadores) — `plugin_visibility.plugin_summary()`, misma lógica que `boardcomposer plugins` en la CLI. Los paneles de Studio quedan fuera, solo importan dentro de la app de escritorio. |
| `/solve` | POST | Recibe `boards`/`constraints`/`strategy`/`top` en JSON, ejecuta `GeometrySolver` y devuelve el mismo JSON que ya genera `solutions_to_json()` para el CLI. |
| `/assist/project` | POST | Recibe `text`, llama a `project_from_text()` (Fase B) y devuelve `boards`/`constraints` en la misma forma que acepta `/solve`. |
| `/assist/strategy` | POST | Recibe `boards`/`constraints`/`goal`/`top`, llama a `suggest_strategy()` (Fase D) y resuelve con la estrategia sugerida — misma respuesta que `/solve`, pero con la estrategia elegida por la IA en vez de por nombre. |
| `/assist/explain` | POST | Recibe `boards`/`constraints`/`strategy`, resuelve como `/solve` (una sola solución) y añade `assistant_explanation` con el texto de `explain_solution()` (Fase C) sobre la mejor solución. |

`create_app(ai_provider=None)` acepta un `AIProvider` inyectable; por defecto usa `default_provider()`, que resuelve a `AnthropicProvider` si hay `ANTHROPIC_API_KEY` en el entorno y a `MockAIProvider` si no. Con `MockAIProvider` (texto fijo no-JSON), `/assist/project` y `/assist/strategy` responden `502` — solo `/assist/explain` funciona sin proveedor real, porque no necesita parsear la respuesta como JSON. Con `ANTHROPIC_API_KEY` configurada, los tres responden con resultados reales.

`docs/masterplan/DOC-008-API.md` describe una API mucho más amplia — versionado (`/api/v1/`), gestión de perfiles, soporte multi-cliente — pero ese documento sigue "🟡 En revisión... pendiente de: definir los contratos públicos... especificar los recursos principales". Esta primera versión implementa solo lo que el backlog pide ("API pública", sin más detalle) y deja el resto para cuando esos contratos se definan: sin versionado, sin persistencia entre peticiones.

### Autenticación y rate limiting (IDE-0009)

`create_app(ai_provider=None, api_key=None, rate_limit=None)` acepta ahora dos parámetros más, ambos con el mismo patrón de inyección que `ai_provider`: `api_key` (por defecto `os.environ.get("BOARDCOMPOSER_API_KEY")`) y `rate_limit` (por defecto `"60 per minute"`, cadena de límite de Flask-Limiter). Con `BOARDCOMPOSER_API_KEY` sin definir, no hay autenticación — mismo comportamiento permisivo de antes de `IDE-0009`. Con ella definida, todas las rutas salvo `/health` exigen esa clave en la cabecera `X-API-Key` (`401` si falta o no coincide); `/health` queda siempre abierta, para no romper comprobaciones de infraestructura sin credenciales.

Rate limiting vía `Flask-Limiter` (`storage_uri="memory://"` por defecto, `redis://...` si se configura `REDIS_URL`), un límite por IP aplicado a todas las rutas salvo `/health` (`@limiter.exempt`); al superarlo, `429` con el mismo formato `jsonify(error=...)` que el resto de la API. El almacenamiento en memoria es adecuado para un único proceso, pero no se comparte entre workers de `gunicorn` — cada worker cuenta sus propias peticiones (`DOC-006-DeudaTecnica.md`, DT-0010); Redis lo comparte.

Para producción, `gunicorn` es una dependencia opcional (`pip install -e ".[prod]"`) en vez de una dependencia obligatoria del paquete, porque `api.py` nunca la importa — se invoca como proceso externo vía su soporte de *app factory*: `gunicorn "boardcomposer.api:create_app()"` (`make serve`), en vez del servidor de desarrollo de Flask (`create_app().run(...)`, en el bloque `if __name__ == "__main__"`, que sigue existiendo solo para uso local). `[prod]` incluye además `redis` (contador de cuota compartido) y `stripe` (facturación de overage, ver más abajo).

### Claves de cliente, cuota y facturación (IDE-0020, IDE-0021)

`create_app()` acepta tres parámetros más además de `api_key`/`rate_limit`: `db_path` (o `BOARDCOMPOSER_DB_PATH`), `quota_store` y `redis_url` (o `REDIS_URL`). Con `db_path` definido, `_authenticate_and_meter()` sustituye a la comprobación simple de antes: la clave única legacy (`BOARDCOMPOSER_API_KEY`) sigue funcionando igual, sin medir — es la clave admin. Cualquier otra clave se resuelve contra `src/boardcomposer/billing.py`, un registro SQLite de claves por cliente (`key_hash` SHA-256, nunca en claro) ligadas a un plan — `PLAN_LIMITS`: `free` (20 solves/mes), `basico` (300/mes), `pro` (1500/mes).

La cuota solo se cuenta en `billing.METERED_ENDPOINTS` (`/solve`, `/assist/*`) — `/health`, `/strategies`, `/plugins` quedan fuera por ser metadata sin coste de cómputo real. `check_quota()` bloquea con `402` al plan `free` una vez agotada la cuota del mes; `basico`/`pro` siguen respondiendo por encima de su cuota y acumulan overage. El contador (`QuotaStore`) es pluggable: `InMemoryQuotaStore` (dev/test, por proceso) o `RedisQuotaStore` (producción, compartido entre workers — mismo problema y misma solución que el rate limiter).

`src/boardcomposer/stripe_billing.py` (`IDE-0021`) cierra el cobro: cada request por encima de cuota en un plan de pago reporta una unidad de uso a Stripe (`SubscriptionItem.create_usage_record`, *best-effort* — un fallo de Stripe nunca rompe la petición real del cliente, solo se registra en el log). Inactivo por defecto (mismo patrón que `REDIS_URL`): sin `STRIPE_SECRET_KEY`/`STRIPE_PRICE_BASICO`/`STRIPE_PRICE_PRO`, nada cambia. `scripts/manage_keys.py` (CLI admin: `create`/`revoke`/`list`) da de alta el Customer+Subscription en Stripe automáticamente al emitir una clave de plan de pago, cuando Stripe está configurado.

Receta de despliegue en la nube (`IDE-0014`), `Dockerfile` en la raíz del repo más Fly.io o VPS+Caddy, incluidas las variables de billing/Stripe: `docs/deploy.md`.

## BoardComposer Studio (`studio/`)

Aplicación PySide6 (Qt) para explorar y editar proyectos visualmente. Estructura interna:

- **`models/`** — `StudioProject`, `StudioBoard`, `StudioPiece`, `StudioPlacement`: modelos propios de Studio, distintos de los del Core.
- **`workspace/`** — `BoardWorkspace`, `BoardPieceItem`, `SelectionController`, `DragController`, `PlacementValidator`, cámara y grid: la superficie gráfica (`QGraphicsScene`/`QGraphicsView`) donde el usuario coloca piezas manualmente. `placement_fit.py` es el equivalente sin Qt de `PlacementValidator` (`piece_fits_on_board()`, `find_free_position()`), para las acciones que ocurren fuera de la escena — mover una pieza a otro tablero, editar dimensiones — y reutiliza `boardcomposer.geometry.Rectangle`.
- **`commands/`** — `CommandManager` + comandos (`MovePieceCommand`, `RotatePieceCommand`, `DeletePieceCommand`, `AddBoardCommand`/`EditBoardCommand`, `AddPieceCommand`/`EditPieceCommand`, `MoveToBoardCommand`, `SetKerfCommand`): patrón Command para undo/redo (ver ADR-008). Cada comando resuelve el proyecto actual en el momento de deshacer, no guarda una referencia.
- **`dialogs/`** — `BoardDialog`, `PieceDialog`, `MoveToBoardDialog`, `KerfDialog`: diálogos de alta/edición y de configuración, con la validación previa a construir el comando.
- **`events/`** — `EventBus` síncrono para desacoplar componentes de Studio (ver ADR-003).
- **`selection/`** — `SelectionManager`, seguimiento de qué objetos están seleccionados.
- **`project/`** — `ProjectManager` (ciclo de vida del proyecto abierto) + `project_io.py` (persistencia JSON `.bcstudio.json`).
- **`panels/`** — contenido de los paneles contextuales: `inspector_panel.py` (Proyecto/Tablero/Pieza), `comparator_panel.py` (comparación de varias soluciones), `chat_panel.py` (historial del Asistente, IDE-0007 Fase E) y `timeline_panel.py` (dock Timeline, dos pestañas — Resumen de tableros y Actividad en vivo vía `EventBus`, `IDE-0019`). `board_metrics.py::board_utilization()` es un cálculo compartido entre Inspector y Timeline, no un panel en sí. Funciones puras, sin Qt, testeadas directamente.
- **`export/`** — exportación del estado actual del workspace a fichero: `svg_export.py` reutiliza `boardcomposer.export.solution_to_svg()` del Core; `pdf_export.py` dibuja lo mismo vía `QPainter`/`QPdfWriter` (Qt, por eso vive en Studio y no en el Core). `solution_bridge.py` convierte `StudioProject` (piezas + colocaciones) a un `AssemblySolution` del Core para que ambos exportadores reutilicen la misma geometría.
- **`layout_service.py`** — **el puente explícito entre Studio y el solver del Core.** `LayoutService.to_core_project()` traduce un `StudioProject` a un `Project` del Core (con `ProjectConstraints(allow_rotation=True, allow_cutting=False)`), aplicando además: compensación de ancho de sierra (`kerf_mm`, ensancha piezas y tablero — `DEC-0016`, `DT-0020`), filtrado por grosor no coincidente, y exclusión de piezas ya colocadas en otro tablero. `solve_current_project()`/`compare_solutions()` invocan `GeometrySolver` sobre ese proyecto traducido; `apply_last_solution_to_current_project()`/`apply_comparison_solution()` vuelcan las `BoardPlacement` resultantes de vuelta a `StudioPlacement`, y `_fill_other_empty_boards_with_leftovers()` reparte las piezas sobrantes entre el resto de tableros completamente vacíos del proyecto.
- **`assistant_service.py`** — **el puente explícito entre Studio y `boardcomposer.ai` (IDE-0007 Fase E).** `AssistantService.ask(question)` construye un prompt con el contexto del proyecto abierto (nombre, nº de tableros/piezas/piezas colocadas) más la pregunta del usuario, lo envía a `AIProvider.complete()` (`default_provider()` por defecto) y guarda cada par pregunta/respuesta en `history`. No reutiliza `project_from_text()`/`explain_solution()`/`suggest_strategy()` — es una conversación abierta, no una de las tareas estructuradas de esas funciones.
- **`panel_plugins.py`** — cubre la Fase E de `IDE-0008` (`docs/masterplan/DOC-004-Backlog.md`). `discover_panel_plugins()` reutiliza `boardcomposer.plugins.discover_plugins()` sobre el grupo `boardcomposer.studio_panels`; a diferencia de generators.py/strategies.py/io.registry.py/export.registry.py, no hay nada integrado que fusionar — Explorer/Inspector/Timeline/Comparador/Asistente son parte fija de `MainWindow`, no plugins. Un plugin registra una factoría `(services: StudioServices) -> QWidget`.
- **`main_window.py`** — ventana principal, ensambla menú, paneles y workspace. `_build_plugin_panels()` (llamado al final de `_build_panels()`) crea un `QDockWidget` por cada panel de `discover_panel_plugins()`, lo añade al área derecha y publica su `toggleViewAction()` en el menú "Ver" (antes vacío). Un plugin que use un nombre reservado (`RESERVED_PANEL_NAMES`: los 5 docks integrados), que falle al cargarse (`PluginLoadError`) o cuya factoría lance una excepción al construir el widget, se ignora con un aviso en la barra de estado — nunca impide que el resto de Studio arranque.
- **`app.py`** — punto de entrada (`main() -> int`): construye `QApplication`, `StudioServices` y `MainWindow`, muestra la ventana y ejecuta el bucle de eventos. Expuesto como el script `boardcomposer-studio` (`pyproject.toml`).

### Empaquetado (IDE-0011)

Studio se distribuye como `.app` de macOS (arm64) generado con `pyside6-deploy` (herramienta oficial de PySide6, basada en Nuitka) — antes solo se ejecutaba desde código fuente (`DT-0008`, `docs/masterplan/DOC-006-DeudaTecnica.md`).

- Configuración en `studio/pysidedeploy.spec`: `input_file = app.py`, `exec_directory = ./dist` (el `.app` final queda en `studio/dist/BoardComposerStudio.app`, fuera del árbol de código). `icon`/`python_path` se dejan en blanco a propósito: son rutas absolutas de la máquina que hace el build — `python_path` se sobrescribe en cada ejecución con el intérprete activo (`Config.set_or_fetch` en `pyside_deploy`), e `icon` cae al icono por defecto de PySide6 si el campo está vacío; si un build local los deja escritos, hay que volver a dejarlos en blanco antes de comitear.
- `make package` lo genera localmente (`cd studio && pyside6-deploy -f app.py`); requiere `pip install -e ".[package]"` (dependencia opcional `nuitka`).
- `extra_args` fija el bundle identifier (`--macos-signed-app-name=com.efjdefrutos.boardcomposer.studio`) y la versión (`--macos-app-version`). Sin lo primero, Nuitka lo deriva del nombre del fichero de entrada y el `.app` sale con `CFBundleIdentifier = app`: ni único, ni notarizable. No debe cambiar nunca una vez publicada una release — macOS indexa ajustes y permisos por esa cadena. La versión la contrasta `scripts/check_project.py` contra `pyproject.toml` en cada `make check`, porque viven en ficheros distintos y se desincronizan solas.
- `.github/workflows/package-studio.yml` (`runs-on: macos-latest`): al crear un tag `v*`, corre los tests, compila el `.app`, lo firma si puede (ver abajo), lo comprime con `ditto` y lo publica como asset de una release de GitHub para ese tag.
- macOS por defecto usa `--standalone --macos-create-app-bundle` independientemente del `mode` configurado en el `.spec` (solo relevante en Windows/Linux).

#### Firma y notarización (`DEC-0017`, `DT-0011`)

El workflow tiene dos caminos según existan o no los secrets de firma, y los mismos comandos valen para ambos:

- **Con secrets** (`MACOS_CERTIFICATE_P12`, `MACOS_CERTIFICATE_PASSWORD`, `MACOS_SIGNING_IDENTITY`, `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD`): el certificado se importa en un llavero propio del runner y `scripts/sign_and_notarize.sh` firma *inside-out* —cada `.dylib`/`.so` primero, el bundle al final, porque la firma exterior sella los hashes de lo que hay dentro— con hardened runtime y *timestamp*, notariza con `notarytool --wait` y grapa el ticket con `stapler`. Deliberadamente **sin `--deep`**, que Apple desaconseja para firmar, y **sin entitlements**: la aplicación dibuja ventanas y hace HTTPS saliente, y ninguna de las dos cosas necesita uno fuera del App Sandbox.
- **Sin secrets** (situación actual): build sin firmar, y `docs/INSTALL-macos.md` viaja como segundo asset de la release con el `xattr -dr com.apple.quarantine` que hace falta para abrirla.

Un certificado autofirmado no es una alternativa: Gatekeeper solo confía en los emitidos por Apple, así que dejaría exactamente el mismo aviso (`DEC-0017`).

- Fuera de alcance: solo macOS/arm64, sin Windows/Linux ni Intel (`DT-0011`).

## Regla de dependencia

`studio/` importa desde `boardcomposer` (el Core); lo inverso nunca ocurre. `LayoutService` y `AssistantService` son las únicas clases de Studio que importan tipos de dominio del Core (`Board`/`Project`/`ProjectConstraints`/`GeometrySolver` la primera, `AIProvider`/`default_provider` la segunda) — el resto de Studio trabaja exclusivamente con sus propios modelos (`StudioProject`, `StudioBoard`, etc.). `panel_plugins.py` es una excepción distinta: no importa tipos de dominio, solo reutiliza la utilidad de infraestructura `boardcomposer.plugins.discover_plugins()` (igual que `solver/generators.py`, `solver/strategies.py`, `io/registry.py` y `export/registry.py` en el Core).
