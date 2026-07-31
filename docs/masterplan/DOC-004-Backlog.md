# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 31/07/2026

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
| IDE-0012 | Exportación DXF | 🟢 | P2 |
| IDE-0013 | Guía para desarrolladores de plugins | 🟢 | P2 |
| IDE-0014 | Receta de despliegue Cloud | 🟢 | P2 |
| IDE-0015 | Visibilidad de plugins instalados | 🟢 | P2 |
| IDE-0016 | Tema visual, iconos y toolbar de Studio | 🟢 | P2 |
| IDE-0017 | Despliegue privado de la API en VPS propio | 🟢 | P2 |
| IDE-0018 | Importación de piezas desde CSV en Studio | 🟢 | P2 |
| IDE-0019 | Resumen de tableros y log de actividad en el dock Timeline | 🟢 | P2 |
| IDE-0020 | Claves de API por cliente con cuota mensual (planes de pago) | 🟢 | P1 |

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

## IDE-0012 — Exportación DXF

**Estado:** 🟢 Completado. Cierra el punto P2 de `DOC-003-Roadmap.md` ("Exportación DXF").

- `solution_to_dxf()` (`src/boardcomposer/export/dxf_exporter.py`, SDK `ezdxf`): un `LWPolyline` cerrado por tabla colocada (rectángulo con las 4 esquinas de la colocación) más una etiqueta `TEXT` con el `board_id`, mismo criterio visual que `solution_to_svg()`. Escribe en un `io.StringIO()` con `doc.write()` para devolver `str`, igual que el resto de `Exporter = Callable[[AssemblySolution], str]` — sin cambiar ese contrato.
- Registrado en `EXPORTER_REGISTRY` (`src/boardcomposer/export/registry.py`) como `"dxf"`, junto a `"svg"` — `exporter_by_name()`/`available_exporters()` ya lo resuelven sin cambios adicionales (infraestructura de `IDE-0008` Fase D).
- Verificado con un fichero real (no solo tests): solución con 2 tablas colocadas exportada a `.dxf`, reabierta con `ezdxf.readfile()` y confirmadas las 2 polilíneas y las 2 etiquetas de texto.
- Fuera de alcance (mismo criterio que `IDE-0010`): no está expuesto ni en la API ni en el menú "Exportar" de Studio (que hoy solo ofrece SVG/PDF, `IDE-0005`) — decisión explícita para mantener el alcance mínimo.

---

## IDE-0013 — Guía para desarrolladores de plugins

**Estado:** 🟢 Completado. Cierra el punto P2 de `DOC-003-Roadmap.md` ("Marketplace, biblioteca de materiales, comunidad" de la Fase 5 — Ecosistema), primer paso concreto según `DOC-999-Ideas.md`. Decisión `DEC-0011` (`docs/masterplan/DOC-005-Decisiones.md`).

- `docs/plugins.md`: cómo crear y publicar un plugin para cada uno de los 5 grupos de entry point (`boardcomposer.generators`/`.strategies`/`.importers`/`.exporters`/`.studio_panels`) — forma exacta de la función/factoría esperada, ejemplo mínimo end-to-end por tipo, y cómo se resuelven colisiones de nombre con las capacidades integradas (`DEC-0008`).
- Los 5 ejemplos verificados con una instalación real (no solo revisión del markdown): paquete `mi-paquete` con los 5 entry points, instalado con `uv pip install -e .` en el entorno del proyecto, y cada plugin resuelto vía `available_generators()`/`strategy_by_name()`/`importer_by_name()`/`exporter_by_name()`/`discover_panel_plugins()` (este último instanciando un `MainWindow` real). Detectado y corregido en el proceso: una clave de entry point con tilde (`Métricas`) debe ir entre comillas en TOML o `pip install` falla con `TOMLDecodeError` antes de llegar a BoardComposer — documentado en `docs/plugins.md`.
- Enlazada desde `README.md` y `docs/architecture.md`.

**Fuera de alcance:** visibilidad de plugins instalados vía CLI/API (candidata siguiente en `DOC-999-Ideas.md`, aún sin promover) y marketplace público real (requiere decisión de producto previa).

---

## IDE-0014 — Receta de despliegue Cloud

**Estado:** 🟢 Completado. Cierra el punto P2 de `DOC-003-Roadmap.md` ("Cloud"), primer paso concreto según `DOC-999-Ideas.md`. Decisión `DEC-0012` (`docs/masterplan/DOC-005-Decisiones.md`).

- `Dockerfile` (raíz del repo, `python:3.13-slim`): instala `boardcomposer[prod]`, corre como usuario sin privilegios (`appuser`), sirve vía `gunicorn "boardcomposer.api:create_app()"` en el puerto `5050`. No incluye Studio en tiempo de ejecución (solo el paquete `boardcomposer`, aunque `pyside6` se instala igualmente por ser dependencia obligatoria del paquete — ver aviso de tamaño en `docs/deploy.md`).
- `docs/deploy.md`: build/prueba local con Docker, despliegue en Fly.io (PaaS, `fly launch --dockerfile Dockerfile` + `fly secrets set`) y alternativa VPS + Caddy (proxy inverso con TLS automático vía Let's Encrypt), configuración de `BOARDCOMPOSER_API_KEY`/`ANTHROPIC_API_KEY` como secretos, y troubleshooting (401/429/fallback a `MockAIProvider`).
- Verificado con una build y despliegue local reales (no solo revisión del `Dockerfile`): imagen construida, contenedor arrancado con `BOARDCOMPOSER_API_KEY`, `/health` sin clave (`200`), `/strategies` sin clave o con clave incorrecta (`401`), con la clave correcta (`200`), `/solve` con una solución real de vuelta, y logs de `gunicorn` confirmando que corre como `appuser`.
- Enlazada desde `README.md` y `docs/architecture.md`.

**Fuera de alcance:** instancia demo pública mantenida (implica coste de infraestructura recurrente) y SaaS real (proyectos persistentes por usuario, cuentas, facturación — requiere decisión de producto previa). No se ha ejecutado un despliegue real contra Fly.io ni un VPS (crearía recursos facturables en una cuenta externa) — los pasos de la Opción A/B están verificados contra la documentación oficial de cada herramienta, no contra una cuenta real.

---

## IDE-0015 — Visibilidad de plugins instalados

**Estado:** 🟢 Completado. Cierra el siguiente punto P2 de `DOC-003-Roadmap.md` ("Marketplace, biblioteca de materiales, comunidad" de la Fase 5 — Ecosistema), segunda candidata de `DOC-999-Ideas.md` para ese grupo. Decisión `DEC-0013` (`docs/masterplan/DOC-005-Decisiones.md`).

- `boardcomposer.plugin_visibility.plugin_summary()` (nuevo, `src/boardcomposer/plugin_visibility.py`): plugins de terceros instalados y errores de carga para cada uno de los 4 grupos de entry point del Core (`boardcomposer.generators`/`.strategies`/`.importers`/`.exporters`) — reutiliza `available_*()`/`*_plugin_errors()` ya existentes, sin cargador propio. Los paneles de Studio (`boardcomposer.studio_panels`) quedan fuera a propósito: solo importan dentro de la app de escritorio, no en un contexto CLI/API.
- CLI: subcomando `boardcomposer plugins` (`--json` opcional), vía `argparse.add_subparsers(dest="command")` opcional — no rompe la invocación existente sin subcomando (`--csv`/`--excel`/etc.).
- API: `GET /plugins`, mismo formato de respuesta que la CLI, sujeta a la misma autenticación/rate limiting que el resto de rutas salvo `/health` (`IDE-0009`).
- Verificado con el binario/servidor reales, no solo tests: `boardcomposer plugins` y `boardcomposer plugins --json` contra el entorno instalado; `GET /plugins` y `GET /health` contra `python -m boardcomposer.api` arrancado de verdad (`200` en ambos).

**Fuera de alcance:** marketplace público real (requiere decisión de producto previa, sin cambios). Paneles de Studio (grupo `boardcomposer.studio_panels`) no incluidos en esta visibilidad CLI/API.

---

## IDE-0016 — Tema visual, iconos y toolbar de Studio

**Estado:** 🟢 Completado (PR #37). Cierra un gap de UX de `DOC-007-UX-Studio.md`: Studio no tenía identidad visual propia (estilo por defecto de Qt, sin iconos, sin toolbar) ni ningún atajo visual para las acciones más usadas.

- Tema claro/oscuro (`studio/theme.py`): paleta (`Palette`, `LIGHT`/`DARK`) aplicada como hoja de estilos Qt (`build_stylesheet()`/`apply_theme()`); detección automática del modo del sistema vía `QStyleHints.colorScheme()` (`detect_color_scheme()`), y menú "Ver" → "Tema" (`Automático`/`Claro`/`Oscuro`) para forzarlo manualmente.
- Acento complementario ámbar (`accent2`/`accent2_hover`, complementario del azul original en el círculo cromático): degradado de 3 paradas azul→turquesa→ámbar en la toolbar y los botones primarios, y franja de color distintiva en el título de los docks "Asistente"/"Comparador" (el resto de paneles se queda en la franja azul) — feedback directo tras revisar la primera versión, percibida como plana y con poco color.
- Sombra de elevación (`apply_elevation()`, `QGraphicsDropShadowEffect`) en la toolbar y en cada panel acoplado, para dar sensación de profundidad frente al borde de 1px plano anterior. Limitación conocida: Qt recorta la mayor parte de la sombra mientras el panel permanece acoplado — se aprecia sobre todo en la toolbar y de forma completa si un panel se "flota" como ventana propia.
- Set de iconos de línea (`studio/icons.py`): trazado SVG por acción, renderizado en tiempo de ejecución a `QPixmap` vía `QSvgRenderer` (sin pipeline de assets binarios), coloreado según el tema activo; aplicado a las acciones del menú y a una nueva toolbar principal (`_build_toolbar()`, `studio/main_window.py`) con las acciones más usadas agrupadas por bloques.
- Entrada del Asistente (`studio/prompt_input.py`, `PromptTextEdit`): sustituye al `QLineEdit` de una sola línea por una caja multilínea con altura mínima cómoda; Intro envía la pregunta, Mayús+Intro inserta un salto de línea; pegar o arrastrar un archivo (o elegirlo con un botón de clip vía `QFileDialog`) lo adjunta en vez de volcar su ruta como texto — se incluye como contenido en la pregunta si es un archivo de texto legible (`.txt`/`.md`/`.json`/`.csv`/`.py`/`.log`), o solo referenciado por nombre si no lo es (el `AIProvider` es solo texto, sin soporte multimodal). `chat_panel.py` renderiza los saltos de línea como `<br>` para que las preguntas multilínea y los adjuntos se lean bien en el historial.
- Verificado con la app real (no solo tests): capturas de la toolbar, la franja de color de los docks y la nueva entrada del Asistente con los botones de adjuntar/enviar.

---

## IDE-0017 — Despliegue privado de la API en VPS propio

**Estado:** 🟢 Completado. Extiende `IDE-0014` con una tercera opción de despliegue (Opción C, `docs/deploy.md`) y, a diferencia de `IDE-0014`, verificada contra un despliegue real y en marcha — no solo documentación. Decisión `DEC-0014` (`docs/masterplan/DOC-005-Decisiones.md`).

- **Opción C — VPS con Plesk (extensión Docker)** (`docs/deploy.md`): despliegue de la misma imagen de `IDE-0014` (sin cambios en el `Dockerfile` salvo añadir `Svg` a `studio/pysidedeploy.spec` para `IDE-0016`) en un VPS con panel Plesk, usando su extensión Docker en vez de Caddy manual (Opción B) — Plesk gestiona el dominio, el proxy inverso (directivas nginx adicionales) y el certificado TLS (Let's Encrypt) desde su propia interfaz.
- Desplegado en real contra `bc.efjdefrutos.com` (Vultr + Ubuntu + Plesk): subdominio creado, imagen construida y contenedor arrancado por SSH (`docker build`/`docker run --env-file`, evitando comillas con las claves para no romper la línea de comandos), certificado Let's Encrypt emitido, proxy nginx conectado tras desactivar "Modo proxy" (evita el conflicto `duplicate location "/"` entre el `location /` que genera Plesk hacia Apache y el nuestro hacia el contenedor).
- `ANTHROPIC_API_KEY` real configurada (sin restringir a `MockAIProvider`) — decisión explícita del propietario, con el límite de gasto mensual fijado en la propia consola de Anthropic (`DEC-0014`).
- Protección por IP en vez de login (`DEC-0014`): directiva nginx `allow <IP>; deny all;` antes del `proxy_pass`, para un uso personal de un único usuario — corta en `403` antes de que la petición llegue a la API, incluso si `BOARDCOMPOSER_API_KEY` se filtrara. `BOARDCOMPOSER_API_KEY` se mantiene igualmente como defensa en profundidad.
- **Actualización (`DEC-0015`):** el allowlist de IP ataba el acceso a una única red — se sustituye por autenticación HTTP Basic en nginx (`auth_basic`/`htpasswd`) en ambos subdominios (`bc.`/`studio.`), que funciona desde cualquier red sin depender de una IP fija. Sigue sumándose a `BOARDCOMPOSER_API_KEY` y a `VNC_PASSWORD`, no los sustituye.
- Verificado en real, no solo local (a diferencia de `IDE-0014`, que solo probó Docker/local): `/health` sin clave (`200`) y `/strategies` con la clave correcta (`200`, lista de estrategias) desde la IP permitida; `403` de nginx al probar desde datos móviles (IP distinta, fuera del `allow`); Fail2Ban y el Web Application Firewall (mod_security) de Plesk descartados como causa de falsos positivos durante el diagnóstico — ambos estaban desactivados para este dominio.
- `docs/deploy.md` actualizado con la Opción C completa (pasos, directiva nginx con IP allowlist, verificación, actualización tras un cambio de código) y una entrada de troubleshooting para el `403` de la allowlist (IP dinámica o no actualizada).

**Ampliación — Studio por navegador (escritorio remoto):** tras verificar la API, el propietario aclaró que su objetivo real era usar la **interfaz visual** de Studio desde fuera de su Mac, no solo la API. De las dos vías posibles (escritorio remoto de la app existente vs. reescritura web completa), se eligió la primera — la segunda es el salto "SaaS real" ya descartado.

- `Dockerfile.studio` + `docker/studio-entrypoint.sh`: el mismo Studio PySide6 sin modificar corre dentro de una pantalla X11 virtual (`Xvfb`, 1920x1080, renderizado por software), gestionada por `fluxbox` (limitado a 1 escritorio virtual vía `docker/fluxbox-init`), capturada por `x11vnc` (contraseña obligatoria vía `VNC_PASSWORD`) y servida como página web con `noVNC`/`websockify` (puerto `6080`). El entrypoint maximiza la ventana con `wmctrl` al arrancar y tumba el contenedor si muere cualquiera de los procesos clave (para que `--restart unless-stopped` lo levante entero).
- `docs/deploy-studio-remote.md`: despliegue en el mismo patrón VPS+Plesk que la Opción C — subdominio propio, proxy nginx con las cabeceras de websocket (`Upgrade`/`Connection`) y `proxy_read_timeout` alto (sin ellas noVNC se queda en "Connecting…"/corta la sesión), mismo allowlist de IP de `DEC-0014`, TLS de Let's Encrypt.
- Cuatro fallos reales detectados y corregidos probando contra el despliegue real (registrados también en `CHANGELOG.md`): barra de menú desaparecida en Linux/xcb (`setNativeMenuBar(False)` fuera de macOS), ventana sin maximizar, Asistente mudo ante un fallo del proveedor de IA (ahora el error se muestra en el propio chat — detectado por una `ANTHROPIC_API_KEY` inválida que solo aparecía en `docker logs`), e iconos de menú invisibles (blanco sobre superficie clara; ahora tematizados para el menú, blanco solo en la toolbar).
- Verificado extremo a extremo por el propietario en su navegador: interfaz completa (menú, toolbar, Explorer, lienzo, Comparador) manejándose en remoto, con IA real en el Asistente.

**Fuera de alcance:** esto es una instancia **privada** de un único usuario, no la candidata "instancia demo pública" de `DOC-999-Ideas.md` (que por definición implica acceso abierto sin restricción de IP) — esa sigue sin acotar. Tampoco un SaaS real con cuentas de usuario (se decidió explícitamente no construir login/registro por email para este caso, `DEC-0014`), ni sesiones multiusuario simultáneas del Studio remoto (una sesión VNC compartida, un contenedor).

---

## IDE-0018 — Importación de piezas desde CSV en Studio

**Estado:** 🟢 Completado. BoardComposer Studio solo tenía el CSV como formato de proyecto de la CLI (`--csv`, cierra RF-002) — no había forma de meter piezas desde un CSV externo en un proyecto ya abierto en Studio sin editar `.bcstudio.json` a mano.

- `load_pieces_from_csv()` (`studio/project/csv_import.py`, función pura sin Qt): mismas columnas obligatorias que el importador CSV del Core/CLI (`id`/`length_mm`/`width_mm`/`thickness_mm`), más `material` opcional. Validación estricta — cualquier fila con una columna ausente, una dimensión no numérica, un id vacío o un id repetido (en el propio fichero o contra el proyecto abierto) aborta toda la importación con `CsvImportError` y el número de fila, sin devolver piezas parciales.
- `MainWindow._import_pieces_csv()`: nueva acción "Importar piezas (CSV)…" en el menú Archivo. Exige un tablero activo (igual que "Añadir pieza…"), y añade cada pieza válida con un `AddPieceCommand` deshacible (uno por pieza, igual que al añadir varias a mano con "Cantidad"), colocada en el tablero activo.
- Verificado con tests (`tests/test_csv_import.py`, `tests/test_main_window_import_csv.py`): carga básica, columna `material` opcional, las cuatro validaciones de rechazo, deshacer pieza a pieza, y que un fichero inválido deja el proyecto intacto.

---

## IDE-0019 — Resumen de tableros y log de actividad en el dock Timeline

**Estado:** 🟢 Completado. Registrado a posteriori: el bloque se construyó y comitió (PR #58) antes de darlo de alta aquí, incumpliendo la norma 1 de `MASTERPLAN.md` ("No añadir funcionalidad sin bloque definido") — detectado por `/code-review` sobre el propio diff. El bloque queda formalizado ahora, sin deshacer nada; ver `DOC-006-DeudaTecnica.md` para el registro del incumplimiento de proceso.

El dock "Timeline" mostraba desde su creación el texto literal "Timeline / Consola / Eventos" — ninguna de las tres cosas que nombraba estaba construida. El `EventBus` de ADR-003 (`studio/events/event_bus.py`) estaba instanciado en `StudioServices` sin que nada llamara nunca a `publish()`/`subscribe()` (documentado explícitamente en `docs/studio.md`).

- El dock pasa a `QTabWidget` con dos pestañas, ambas funciones puras (`studio/panels/timeline_panel.py`), pintadas con el mismo `panel_html_stylesheet()` que Inspector/Comparador:
  - **Resumen** (`render_overview()`) — cada tablero con dimensiones, material, nº de piezas, % de uso (`studio/panels/board_metrics.py::board_utilization()`, extraído para compartirlo con `inspector_panel.render_board()`) y qué piezas contiene; piezas sin colocar aparte.
  - **Actividad** (`render_activity()`) — log en vivo alimentado por `ActivityLog` (`studio/activity_log.py`), suscrita a un único evento `"studio.activity"`, hasta 200 mensajes. `MainWindow` se suscribe también y se redibuja sola cuando algo publica — desacoplado de verdad, no un par fijo publish+setHtml.
- Queda registrado: añadir/editar/eliminar/rotar tablero o pieza (incluido el arrastre en el lienzo, `BoardWorkspace._finish_piece_drag()`, publicando directamente sin necesitar una referencia a `MainWindow`), mover a otro tablero, cambiar el kerf, deshacer/rehacer, resolver/aplicar layout, comparar soluciones, importar CSV, proyecto nuevo/abrir/guardar.
- Cierra un bug de verdad, no solo de estilo: 6 de 9 clases de comando (`AddBoardCommand`, `EditBoardCommand`, `AddPieceCommand`, `EditPieceCommand`, `RotatePieceCommand`, `DeletePieceCommand`) heredaban del Protocol `Command` —que declara `name: str`— sin definirlo nunca; un `AttributeError` dormido que nadie había disparado hasta que el log de actividad necesitó leerlo. `CommandManager.undo()`/`redo()` devuelven ahora el comando en vez de `None`, para que `MainWindow` no tenga que asomarse a `undo_stack`/`redo_stack`.
- Verificado con tests (`tests/test_activity_log.py`, `tests/test_timeline_panel.py`, `tests/test_board_metrics.py`, `tests/test_main_window_timeline.py`, más los nuevos casos en `tests/test_command_manager.py` y `tests/test_board_workspace.py`) y contra una ventana renderizada de verdad (`grab()`), claro y oscuro. 712 tests en verde.

---

## IDE-0020 — Claves de API por cliente con cuota mensual (planes de pago)

**Estado:** 🟢 Completado. Registrado a posteriori: el bloque se construyó y comitió (`043caf1`) antes de darlo de alta aquí, incumpliendo la norma 1 de `MASTERPLAN.md` ("No añadir funcionalidad sin bloque definido") — mismo incumplimiento que `IDE-0019`. Ver `DT-0022` en `DOC-006-DeudaTecnica.md`.

Primer paso técnico de la decisión de producto "Studio gratis, API de pago" (ver `Próxima decisión` de `MASTERPLAN.md`, ahora resuelta a favor del modelo híbrido). Modelo de planes cerrado con el usuario: `free` (20 solves/mes, 0 €), `basico` (300/mes, 9 €/mes, overage 0,05 €/solve), `pro` (1500/mes, 29 €/mes, overage 0,03 €/solve).

- `src/boardcomposer/billing.py` (nuevo): registro de claves por cliente en SQLite (`key_hash` con SHA-256, nunca la clave en claro), `PLAN_LIMITS`, contador de cuota mensual pluggable — `InMemoryQuotaStore` (dev/test) o `RedisQuotaStore` (producción, comparte estado entre workers de `gunicorn`, a diferencia del rate limiter existente — ver `DT-0006`/`DOC-006`).
- `src/boardcomposer/api.py`: `_authenticate_and_meter()` sustituye a `_require_api_key()`. La clave única legacy (`BOARDCOMPOSER_API_KEY`) sigue funcionando igual, ahora tratada como clave admin sin medir. Las claves nuevas se resuelven contra el registro SQLite (`db_path`/`BOARDCOMPOSER_DB_PATH`); la cuota solo se cuenta en `billing.METERED_ENDPOINTS` (`/solve`, `/assist/*`) — `/health`, `/strategies`, `/plugins` quedan fuera por ser metadata sin coste de cómputo real. Plan `free` agotado responde `402`; `basico`/`pro` siguen respondiendo por encima de su cuota y acumulan overage (sin cobro automático — integración de pagos pendiente, fuera de alcance de este bloque).
- `scripts/manage_keys.py` (nuevo): CLI admin `create`/`revoke`/`list` sobre el mismo `billing.py`.
- `docs/deploy.md`: sección nueva con variables de entorno (`BOARDCOMPOSER_DB_PATH`, `REDIS_URL`) y ejemplo de despliegue.
- Verificado con tests nuevos (`tests/test_billing.py`, `tests/test_api_billing.py`) más los ya existentes de auth/rate-limit (`tests/test_api_auth.py`, `tests/test_api_rate_limit.py`). Los propios tests cazaron un bug real antes de comitear: `check_quota()` trataba cualquier plan no reconocido como ilimitado en vez de bloquearlo — corregido con `PAID_PLANS` explícito. 732 tests en verde.

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
