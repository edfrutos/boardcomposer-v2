# CHANGELOG - BoardComposer

## Sin publicar

---

## 0.2.0 - 2026-07-22

### Añadido

- Proveedor de IA real para el Asistente IA (`IDE-0007`): `AnthropicProvider` sobre el SDK `anthropic`, modelo `claude-haiku-4-5`, API key vía la variable de entorno `ANTHROPIC_API_KEY`. `default_provider()` lo activa automáticamente cuando esa variable está definida, con `MockAIProvider` como fallback; usado por defecto en la API (`create_app()`) y en el chat de Studio (`AssistantService`).
- Endurecimiento para producción de la API (`IDE-0009`): autenticación opcional por clave (`BOARDCOMPOSER_API_KEY` vía cabecera `X-API-Key`), rate limiting con Flask-Limiter (60 peticiones/minuto por IP, `/health` exenta) y `gunicorn` como servidor WSGI de producción (dependencia opcional `pip install -e ".[prod]"`, `make serve`).
- Importación desde Excel (`IDE-0010`, cierra RF-002): `load_project_from_excel()` (SDK `openpyxl`), mismas columnas que el CSV existente; registrada en `IMPORTER_REGISTRY` como `"xlsx"` y expuesta en la CLI con `--excel` (mutuamente excluyente con `--csv`).
- Empaquetado de BoardComposer Studio como `.app` de macOS (`IDE-0011`): `pyside6-deploy` (`make package`, dependencia opcional `pip install -e ".[package]"`), nuevo punto de entrada `boardcomposer-studio`, y publicación automática como asset de release de GitHub al crear un tag `v*` (`.github/workflows/package-studio.yml`).
- Exportación DXF (`IDE-0012`): `solution_to_dxf()` (SDK `ezdxf`), registrada en `EXPORTER_REGISTRY` como `"dxf"` junto a `"svg"`.
- Soporte multi-tablero en BoardComposer Studio (`DT-0013`, Fases A–E, PR #31–#35): `board_id` en `StudioPlacement` con migración retrocompatible (Fase A); `AddBoardCommand`/`EditBoardCommand`/`AddPieceCommand`/`EditPieceCommand` deshacibles vía `CommandManager` (Fase B); tablero activo rastreado y renderizado en `BoardWorkspace`, seleccionable desde el Explorer (Fase C); `BoardDialog`/`PieceDialog` y menús "Proyecto"/"Editar" para alta/edición con validación (Fase D); `LayoutService` resuelve el tablero objetivo a partir del tablero activo en vez de asumir siempre el primero (Fase E). Studio deja de depender de editar `.bcstudio.json` a mano para introducir datos reales.
- Guía para desarrolladores de plugins (`IDE-0013`): `docs/plugins.md`, con un ejemplo mínimo funcional por cada uno de los 5 grupos de entry point (generadores, estrategias, importadores, exportadores, paneles de Studio), verificado con una instalación real.
- Receta de despliegue Cloud (`IDE-0014`): `Dockerfile` (`python:3.13-slim`, `gunicorn`, usuario sin privilegios) y `docs/deploy.md` con despliegue en Fly.io o VPS+Caddy, verificado con una build y arranque de contenedor reales.
- Campo Material en `BoardDialog`/`PieceDialog` (ya existía en `StudioBoard`/`StudioPiece`, no se pedía en el formulario).
- Mover una pieza existente a otro tablero (menú "Proyecto" → "Mover a tablero…"): `MoveToBoardDialog` + `MoveToBoardCommand` (deshacible), reasigna `placement.board_id`. Hasta ahora la única forma de meter una pieza en el segundo tablero era crear una pieza nueva con ese tablero activo.
- Grosor y cantidad en `BoardDialog`/`PieceDialog` (`DT-0014`): campo "Grosor" (`thickness_mm`, nuevo en `StudioBoard`/`StudioPiece`, persistido con migración retrocompatible) y campo "Cantidad" (solo al añadir) que crea N tableros/piezas idénticos de una vez con ids derivados (`p1`, `p1-2`, `p1-3`…). `LayoutService.to_core_project()` usa ahora el grosor real de cada pieza en vez de un `19` fijo.
- Atajos de teclado para las acciones más usadas del menú "Proyecto"/"Herramientas"/"Comparar": Añadir/Editar tablero (`Ctrl+Alt+B`/`Ctrl+Alt+Shift+B`), Añadir/Editar pieza (`Ctrl+Alt+P`/`Ctrl+Alt+Shift+P`), Calcular/Aplicar layout (`Ctrl+Alt+L`/`Ctrl+Alt+Shift+L`), Generar comparación (`Ctrl+Alt+C`).
- Ancho de sierra configurable (menú "Proyecto" → "Ancho de sierra…"): `kerf_mm` nuevo en `StudioProject` (persistido, por defecto `0.0`), `KerfDialog` + `SetKerfCommand` (deshacible) para fijarlo. Representa el desperdicio de madera que se lleva cada corte.
- Efecto imán al arrastrar piezas en el workspace: si el borde de la pieza arrastrada queda a menos de 20 mm del borde de otra ya colocada (con solape en el eje perpendicular), `PlacementValidator` la sitúa justo al lado, separada por el ancho de sierra configurado, en vez de dejarla montarse encima o quedar colocada a ojo.
- Fila "Orden de piezas" en el Comparador de soluciones (`DT-0016`): varias candidatas pueden empatar en las 5 métricas agregadas (mismo aprovechamiento/puntuación) aunque sean geométricamente distintas — la nueva fila muestra el orden real de apilado de cada una, la única diferencia que antes no se veía en ningún sitio.
- Visibilidad de plugins instalados (`IDE-0015`): `boardcomposer.plugin_visibility.plugin_summary()`, subcomando `boardcomposer plugins` (`--json` opcional) en la CLI y ruta `GET /plugins` en la API, listando por cada uno de los 4 grupos de entry point del Core qué plugins de terceros están instalados y cuáles fallaron al cargar.
- Tema visual, iconos y toolbar de BoardComposer Studio (`IDE-0016`, PR #37): paleta clara/oscura (`studio/theme.py`) con detección automática del modo del sistema (`QStyleHints.colorScheme()`) y menú "Ver" → "Tema" para forzarlo (Automático/Claro/Oscuro); acento complementario ámbar (`accent2`) junto al azul original, usado en el degradado de la toolbar/botones primarios y como franja distintiva en los docks "Asistente"/"Comparador"; sombra de elevación (`apply_elevation()`, `QGraphicsDropShadowEffect`) en la toolbar y en cada panel acoplado; set de iconos de línea renderizados en tiempo de ejecución (`studio/icons.py`, SVG → `QPixmap`) aplicado al menú y a una nueva toolbar principal con las acciones más usadas agrupadas. Entrada del Asistente sustituida por `PromptTextEdit` (`studio/prompt_input.py`): caja multilínea, Intro para enviar, Mayús+Intro para nueva línea, y adjuntar un archivo por pegado/arrastre o selector de archivos (se incluye como texto en la pregunta si es legible, o solo por nombre si no lo es).
- Despliegue privado de la API en VPS propio (`IDE-0017`): tercera opción de despliegue en `docs/deploy.md` — VPS con panel Plesk y su extensión Docker (reutiliza el `Dockerfile` de `IDE-0014`), con el proxy inverso y el certificado TLS (Let's Encrypt) gestionados desde la propia interfaz de Plesk. Protegido con un allowlist de IP en nginx (`allow`/`deny`) en vez de un sistema de login (`DEC-0014`), sobre la autenticación por clave ya existente (`IDE-0009`). Verificado con un despliegue real y en marcha (subdominio, SSL, `/health` y `/strategies` respondiendo, `403` confirmado desde una IP fuera de la lista), no solo documentado.
- Importación de piezas desde CSV en BoardComposer Studio (menú "Archivo" → "Importar piezas (CSV)…"): `load_pieces_from_csv()` (`studio/project/csv_import.py`), mismas columnas que el CSV del Core/CLI (`id`/`length_mm`/`width_mm`/`thickness_mm`, con `material` opcional). Cada pieza se añade con un `AddPieceCommand` deshacible y colocada en el tablero activo, igual que el alta manual. Validación estricta: cualquier fila inválida (columna ausente, dimensión no numérica, id vacío o repetido — dentro del fichero o contra el proyecto abierto) aborta la importación completa sin tocar el proyecto.
- Acceso independiente de la IP a los despliegues privados (`IDE-0017`, `DEC-0015`): el allowlist de IP en nginx (`DEC-0014`) se sustituye por autenticación HTTP Basic (`auth_basic`/`htpasswd`) en `docs/deploy.md` (Opción C) y `docs/deploy-studio-remote.md` — funciona desde cualquier red, sin infraestructura nueva ni persistencia. Se suma a `BOARDCOMPOSER_API_KEY` y a `VNC_PASSWORD` como capas independientes, no las sustituye.
- Icono propio de la aplicación en el `.app` de macOS (`IDE-0011`, mejora): `studio/assets/icon.icns` generado desde el arte del propietario (`icon-source.jpg`, convertido con `sips` + `iconutil`), registrado en `studio/pysidedeploy.spec` con ruta relativa al repo — sustituye al icono genérico de PySide6 que usaba el empaquetado hasta ahora.
- BoardComposer Studio accesible por navegador vía escritorio remoto (`IDE-0017`, ampliación): `Dockerfile.studio` + `docker/studio-entrypoint.sh` corren el mismo Studio PySide6 sin modificar dentro de una pantalla X11 virtual (`Xvfb` + `fluxbox`), capturada por `x11vnc` y servida como página web con `noVNC`/`websockify` — sin reescritura web. `docs/deploy-studio-remote.md` documenta el despliegue en el mismo patrón VPS+Plesk (subdominio propio, proxy nginx con cabeceras de websocket y `proxy_read_timeout` alto, mismo allowlist de IP de `DEC-0014`, contraseña VNC obligatoria vía `VNC_PASSWORD`). Verificado con un despliegue real y en marcha: interfaz completa manejándose desde el navegador con IA real en el Asistente.

### Corregido

- `project_from_text()`/`suggest_strategy()` fallaban con un proveedor de IA real: Claude envuelve el JSON en un bloque ` ```json ... ``` ` pese a que el prompt pide lo contrario, y devuelve `thickness_mm: null` explícito en vez de omitir la clave. Corregido con `strip_json_fence()` y tratando el `null` explícito igual que una clave ausente.
- `MainWindow._new_project()` (Studio) llamaba a `_load_demo_project()` — "Nuevo proyecto" nunca creaba un proyecto vacío, siempre recargaba la demo. Detectado probando datos reales tras el empaquetado. Corregido: crea un `StudioProject` vacío con un `project_id` nuevo.
- Seis gaps de usabilidad detectados probando Studio a mano tras `DT-0013` (PR #36): "Añadir/Editar pieza" movidos del menú "Editar" al "Proyecto"; los 5 paneles integrados (Explorer/Inspector/Timeline/Comparador/Asistente) ahora tienen su acción de mostrar/ocultar en el menú "Ver" (antes solo los paneles de plugins la tenían, así que cerrar uno lo dejaba irrecuperable); `DeletePieceCommand` solo quitaba la colocación, nunca la pieza de `project.pieces` — asimétrico respecto a `AddPieceCommand`, ahora quita (y el undo restaura) ambas; `BoardDialog`/`PieceDialog` cerraban con un id vacío o repetido dependiendo de un aviso fugaz en la barra de estado, ahora validan antes de `accept()` y se quedan abiertos con un error inline; aplicar una solución que no coloca todas las piezas las hacía desaparecer del lienzo sin aviso (siguen en el inventario, solo pierden su colocación) — `_apply_layout`/`_apply_comparison_solution` ahora informan cuáles quedaron sin colocar.
- El nodo "Soluciones" del Explorer (`DT-0015`) se creaba y se añadía al árbol pero nunca se rellenaba — permanecía vacío siempre. Quitado del Explorer hasta que se acote qué debe mostrar realmente.
- Cuatro fallos detectados probando el Studio remoto (`IDE-0017`) contra el despliegue real: la barra de menú desaparecía en Linux/xcb — Qt intentaba exportarla a un servicio de menú global de escritorio inexistente en el contenedor headless, corregido con `setNativeMenuBar(False)` fuera de macOS; la ventana arrancaba flotando a 1400x900 en una esquina de la pantalla virtual — maximizada ahora vía `wmctrl` en el entrypoint (pantalla ampliada a 1920x1080) y fluxbox limitado a un único escritorio virtual (`docker/fluxbox-init`) para no acabar en uno vacío por error; un fallo del proveedor de IA (clave inválida, sin red…) dejaba el Asistente mudo con la excepción solo en `docker logs` — `AssistantService.ask()` lo captura ahora y lo muestra como respuesta en el propio chat; y los iconos de las opciones de menú eran invisibles (icono blanco compartido con la toolbar sobre la superficie clara del menú) — ahora se generan con el color de texto del tema para el menú, y la toolbar fuerza los suyos a blanco aparte (`widgetForAction`).

## 0.1.0 - 2026-07-13

### Añadido

- Motor: generadores skyline, MaxRects y beam search; estrategias `balanced`/`material`/`compact`.
- CLI: entrada CSV, salida texto/JSON, selección de estrategia (IDE-0004).
- BoardComposer Studio (PySide6): workspace interactivo (IDE-0001), comparador de algoritmos (IDE-0002), inspector de piezas (IDE-0003), gestión de proyectos `.bcstudio.json` (IDE-0004), exportación SVG/PDF (IDE-0005), aviso de cambios sin guardar al cerrar.
- API HTTP pública (IDE-0006): `/health`, `/strategies`, `/solve`.
- Asistente IA (IDE-0007, Fases A–F): puerto `AIProvider` pluggable, generación de proyecto desde texto libre, explicación de soluciones en lenguaje natural, sugerencia de estrategia, chat contextual en Studio, y las tres capacidades anteriores expuestas vía `/assist/*` — todo sobre `MockAIProvider`, sin proveedor real conectado todavía.
- Sistema de plugins (IDE-0008, Fases A–E): descubrimiento vía *entry points* de Python; generadores, estrategias, importadores/exportadores y paneles de Studio registrables por terceros.
- Límite de tamaño de proyecto en la API (`MAX_BOARDS = 100`) para evitar peticiones lentas con proyectos grandes.

### Decisiones

- Los plugins se registran vía *entry points* estándar de Python (`importlib.metadata`), no un cargador propio.
- La IA nunca genera geometría directamente: solo ajusta parámetros del solver determinista existente (pesos de puntuación, generadores a usar).
- Los nombres integrados (generadores, estrategias, importadores, exportadores) siempre tienen prioridad sobre un plugin que repita el nombre.

## 0.0.1 - 2026-06-26

### Añadido

- Documentación fundacional.
- Estructura base del proyecto.
- Backlog inicial.
- Documentación técnica v0.1.

### Decisiones

- Inicio con ensamblaje 2D.
- Núcleo independiente de la interfaz.
- Soluciones explicables.
