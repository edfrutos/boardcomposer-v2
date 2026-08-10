# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 08/08/2026

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
| IDE-0021 | Integración de Stripe para cobro de overage | 🟢 | P1 |
| IDE-0022 | Exportar DXF y JSON desde Studio | 🟢 | P2 |
| IDE-0023 | Comparador: miniaturas, favorita, fragmentación y nº de cortes | 🟢 | P2 |
| IDE-0024 | Vista previa antes de confirmar import CSV | 🟢 | P2 |
| IDE-0025 | Pantalla de Preferencias (tema) | 🟢 | P3 |
| IDE-0026 | Timeline: eventos de actividad con categoría y filtro | 🟢 | P3 |
| IDE-0027 | IDs legibles de solución (etiqueta A/B/C + hash corto) | 🟢 | P3 |
| IDE-0028 | Generador de piezas de contenedor (caja simple) desde un retal | 🟢 | P3 |
| IDE-0029 | Importar tableros (CSV) en Studio | 🟢 | P3 |
| IDE-0030 | Reparto por mejor ajuste entre tableros | 🟢 | P3 |
| IDE-0031 | Cajón sin rieles en el generador de contenedores | 🟢 | P3 |
| IDE-0032 | Buscar actualizaciones (menú Ayuda) | 🟢 | P3 |
| IDE-0033 | Acerca de BoardComposer Studio (menú Ayuda) | 🟢 | P3 |
| IDE-0034 | Clave de API de Anthropic configurable en Preferencias | 🟢 | P2 |
| IDE-0035 | Separar "quitar del tablero" de "eliminar del proyecto" | 🟢 | P1 |
| IDE-0036 | Asistente IA: soporte multi-proveedor (OpenAI, Google Gemini, Ollama local) | 🟢 | P2 |
| IDE-0037 | Columna `quantity` opcional en el import CSV de piezas/tableros | 🟢 | P3 |
| IDE-0038 | `material`/`quantity` en el CSV del Core + restricción dura de material en Studio | 🟢 | P2 |
| IDE-0039 | Inventario persistente de retales en Studio | 🟢 | P3 |
| IDE-0040 | Menú contextual (clic derecho) en el lienzo: editar/eliminar pieza o tablero | 🟢 | P2 |

---

## IDE-0040 — Menú contextual (clic derecho) en el lienzo: editar/eliminar pieza o tablero

**Estado:** 🟢 Completada en `v0.3.19`. Pedido por el usuario el 10/08/2026: hoy
"Editar tablero…"/"Editar pieza…" solo son alcanzables desde el menú
"Proyecto" — quiere las mismas acciones (más eliminar) posicionándose
sobre el elemento en el lienzo y pulsando el botón derecho.

**Decisiones de alcance, resueltas con el usuario:**

1. El botón derecho hoy desplaza la vista (paneo) en cualquier punto del
   lienzo, incluida una pieza o el tablero (`BoardWorkspace.mousePressEvent()`).
   Pasa a abrir un menú **solo** sobre un elemento (pieza o tablero); en el
   área vacía del lienzo sigue paneando exactamente igual que hoy.
2. Menú sobre una pieza: "Editar pieza…" + "Eliminar del proyecto…" (misma
   acción completa que ya existe en el Explorer, `DeletePieceCommand`) —
   no "quitar del tablero" (eso ya tiene su propio atajo, Backspace).
3. **"Eliminar tablero" no existe hoy en ningún sitio** (ni menú, ni clic
   derecho) — se construye nuevo: `DeleteBoardCommand`, deshacible, borra
   el tablero y **desplaza sus piezas a "sin colocar"** (unplace, mismo
   criterio que `UnplacePieceCommand`) en vez de borrarlas también — nunca
   se pierden piezas por eliminar el tablero en el que estaban.

**Alcance:**

- `studio/commands/delete_board_command.py`: `DeleteBoardCommand` —
  quita el tablero de `project.boards` y sus colocaciones de
  `project.placements` (las piezas afectadas siguen en `project.pieces`);
  `undo()` restaura ambas listas.
- `studio/workspace/board_workspace.py`: dos señales Qt nuevas,
  `piece_context_menu_requested(str, QPoint)` y
  `board_context_menu_requested(QPoint)`. `mousePressEvent()` distingue,
  solo para el botón derecho: sobre un `BoardPieceItem` → señal de pieza;
  dentro de `self._board_item.sceneBoundingRect()` (no sobre una pieza) →
  señal de tablero; en cualquier otro punto → paneo, sin cambios. La
  distinción geométrica (no `itemAt()`) evita falsos positivos contra las
  líneas de la rejilla (`grid.py`), que cubren todo `sceneRect()`, no solo
  el tablero.
- `MainWindow._show_piece_context_menu()`/`_show_board_context_menu()`
  (conectadas en `_build_workspace()`): reutilizan `_edit_piece()`/
  `_edit_board()`/`_delete_piece_from_project()` tal cual (el de pieza
  selecciona primero con `workspace.select_piece()`, para que
  `_edit_piece()` opere sobre la pieza pulsada y no sobre la selección
  previa) más un `_delete_board_from_project()` nuevo para el
  `DeleteBoardCommand`.
- Documentación: `docs/studio.md`.

**Fuera de alcance:** distinguir clic derecho corto de arrastrar con el
botón derecho sobre un elemento (permitiría panear también desde ahí) —
descartado explícitamente por el usuario, más complejidad sin necesidad
clara.

---

## IDE-0039 — Inventario persistente de retales en Studio

**Estado:** 🟢 Completada en `v0.3.18`. Promovida el 09/08/2026 desde el punto 1 de la
"Candidata 1" de `docs/masterplan/DOC-999-Ideas.md` (aprovechamiento de
retales) — en su momento (`DEC-0019`, 03/08/2026) se acotó deliberadamente
sin inventario persistente ("solo alta manual, sin código nuevo que
construir"); esto construye justo esa pieza que quedó pendiente.

**Decisiones de alcance, resueltas con el usuario:**

1. Solo Studio, local — no toca el Core ni la API. El inventario es del
   taller de un usuario/máquina, no un recurso multi-cliente como
   `billing.py` (que sí es de la API de pago).
2. Flujo de uso: diálogo dedicado "Usar retal…" (no integrado en
   `BoardDialog`).
3. Un retal se marca consumido **en cuanto se usa** (se añade como
   `StudioBoard` al proyecto activo) — no espera a que el proyecto se
   guarde. Consecuencia documentada: deshacer el `AddBoardCommand`
   resultante no devuelve el retal al inventario (el inventario vive fuera
   del historial de undo/redo del proyecto).

**Alcance:**

- `studio/project/scrap_inventory.py`: capa pura sin Qt (mismo patrón que
  `billing.py`, SQLite) — `init_db(db_path)`, `add_scrap()`,
  `list_available()`, `consume()`. Nunca hace `DELETE`: consumir pone
  `consumed_at`, no borra la fila — mismo criterio de trazabilidad que el
  resto del proyecto ("nunca actúa en silencio/pierde datos"). Mismas
  validaciones de dimensiones que `Board`/`StudioBoard`
  (`math.isfinite`, positivas).
- `studio/inventory_service.py`: envoltorio con Qt — resuelve el fichero
  por defecto vía `QStandardPaths.AppDataLocation` (mismo mecanismo que
  `QSettings()` ya usa para tema/último proyecto, `studio/app.py`), lo crea
  si no existe. Registrado en `StudioServices.__post_init__` como
  `self.inventory`.
- `studio/dialogs/scrap_dialogs.py`: `AddScrapDialog` (mismos campos que
  `BoardDialog` + "Procedencia" libre) y `UseScrapDialog` (lista de
  retales disponibles, ordenados por área ascendente — mismo criterio que
  `apply_best_fit_distribution()`).
- `MainWindow`: dos entradas nuevas en el menú "Proyecto" — "Añadir retal
  al inventario…" (no exige proyecto abierto) y "Usar retal del
  inventario…" (exige proyecto abierto; ejecuta `AddBoardCommand`
  deshacible y luego `inventory.consume()`).
- Documentación: `docs/studio.md` (nueva sección), `DOC-999-Ideas.md`
  (marcar el punto 1 de la Candidata 1 como promovido a `IDE-0039`).

**Fuera de alcance:** priorización automática del solver sobre el
inventario (punto 3 de la misma Candidata 1 en `DOC-999-Ideas.md`, sigue
sin acotar); retales no rectangulares (punto 2, cambio de modelo
geométrico mayor); CLI/API (decisión 1 de arriba).

---

## IDE-0038 — `material`/`quantity` en el CSV del Core + restricción dura de material en Studio

**Estado:** 🟢 Completada en `v0.3.17`. Pedido por el usuario el 09/08/2026, ampliando
`IDE-0037`: los tres formatos de CSV (Core, piezas de Studio, tableros de
Studio) deben admitir `quantity` y `material`, en ese orden. Al investigar
salieron dos decisiones de diseño reales, resueltas con el usuario:

1. El Core nunca ha tenido `material` en `Board` (el único "material" que
   existe hoy es `material_usage_score`, una métrica del solver, sin
   relación). Se añade como campo pasivo — se guarda y se expone, pero sin
   efecto en el solver — porque el Core solo empaqueta piezas sobre **una
   única lámina implícita** (`ProjectConstraints`), sin varias tablas entre
   las que el solver pueda elegir por material. Convertir el Core a
   multi-lámina con material queda fuera de alcance, es un cambio de
   arquitectura mayor que se registrará como su propio ticket si hace falta.
2. En Studio sí hay varias `StudioBoard` reales, así que ahí `material` pasa
   de etiqueta pasiva a **restricción dura**, exactamente el mismo patrón que
   ya existe para `thickness_mm` (`piece.material == board.material`, sin
   comodín): una pieza de un material no encaja en un tablero de otro.

**Alcance — Core:**

- `src/boardcomposer/domain/board.py`: campo `material: str = ""` en
  `Board`, sin validación más allá del tipo — pasivo, igual que `id`.
- `src/boardcomposer/io/csv_loader.py` (`load_project_from_csv`): columnas
  opcionales `quantity` y `material`, en ese orden. `quantity` > 1 expande
  la fila en N `Board`; con `id` presente, ids derivados por sufijo
  (`T-101-2`...) sin comprobar colisión (el Core nunca ha validado ids
  únicos, ni siquiera literales); sin `id`, las N boards quedan con
  `id=None`, igual que hoy con `quantity=1`. `quantity` no entero o no
  positivo, error con número de fila, mismo patrón que las dimensiones.
- `data/samples/basic_boards.csv` y tests (`tests/test_models.py`,
  `tests/test_csv_loader.py`) sin tocar salvo los casos nuevos.

**Alcance — Studio:**

- `studio/project/csv_import.py`/`board_csv_import.py`: sin cambio
  funcional (ya soportaban `material`+`quantity` desde `IDE-0037`, el
  `DictReader` lee por nombre de columna, no por posición) — se reordenan
  los docstrings y `docs/studio.md` a `quantity,material`.
- `studio/layout_service.py`: `to_core_project()` filtra piezas también por
  `piece.material == source_board.material`, junto al filtro de
  `thickness_mm` ya existente (mismo comentario, misma razón física: una
  pieza de roble no tiene nada que hacer en un tablero de pino).
  `apply_best_fit_distribution()` añade el mismo criterio al *skip*
  temprano por tablero.
- `studio/main_window.py`: `_edit_board()` y `_edit_piece()` comprueban
  también el material contra las colocaciones/tablero existentes, junto al
  `thickness_mm` que ya comprueban; `_move_piece_to_board()` filtra
  `matching_boards` también por material.
- `studio/workspace/placement_fit.py` **no** cambia — `piece_fits_on_board()`
  es geometría pura (solape/límites/kerf); `thickness_mm` tampoco se
  comprueba ahí, sino en cada punto de llamada de `main_window.py`/
  `layout_service.py` — mismo patrón para `material`.

**Fuera de alcance:** Excel (`excel_loader.py`) — el usuario pidió los tres
formatos de CSV, no Excel. Multi-lámina con material en el Core (ver punto 1
de más arriba).

---

## IDE-0037 — Columna `quantity` opcional en el import CSV de piezas/tableros

**Estado:** 🟢 Completada en `v0.3.16`. Pedido por el usuario el 08/08/2026: la
cabecera del CSV de importación (piezas y tableros, `IDE-0018`/
`IDE-0029`) no tiene forma de indicar varias unidades idénticas por
fila — solo el diálogo "Pieza"/"Tablero" tiene un campo "Cantidad"
(`PieceDialog`/`BoardDialog`), y es una comodidad del propio diálogo,
no un campo persistido: al aceptar con Cantidad = N, `MainWindow` llama
N veces al comando de añadir con ids derivados
(`_generate_ids()`, `main_window.py`) — `StudioPiece`/`StudioBoard` no
tienen ningún atributo `quantity`.

**Alcance:**

- Columna `quantity` opcional (como `material`) en `load_pieces_from_csv()`
  (`studio/project/csv_import.py`) y `load_boards_from_csv()`
  (`studio/project/board_csv_import.py`) — mismas dos columnas
  obligatorias sin cambios (`id`/`length_mm`/`width_mm`/`thickness_mm`).
  Ausente o vacía = 1, mismo comportamiento que hoy.
- Con `quantity` = N > 1, una fila expande a N piezas/tableros
  idénticos (mismas dimensiones/material/grosor), con ids derivados del
  id de la fila: el primero tal cual, los siguientes con sufijo `-2`,
  `-3`... — mismo esquema de sufijo que `_generate_ids()`, pero
  **determinista, sin saltarse colisiones**: a diferencia del diálogo
  (que prueba el siguiente sufijo libre en silencio), aquí una colisión
  de cualquier id derivado con el fichero o el proyecto abierto es un
  error que aborta toda la importación — mismo criterio "todo o nada,
  nunca magia silenciosa" que ya rige el resto del validador.
- `quantity` no entero, cero o negativo: error con el número de fila,
  mismo patrón que las dimensiones.
- Vista previa (`CsvImportPreviewDialog`/`BoardCsvImportPreviewDialog`)
  sin cambios — la expansión ocurre dentro del loader, así que la
  vista previa ya muestra las N piezas resultantes sin saber nada de
  "quantity".
- Documentación: `docs/studio.md` (columnas del importador).

**Fuera de alcance:** el CSV/CLI del Core (`src/boardcomposer/io/csv_loader.py`)
no se toca — "Cantidad" solo existe en los diálogos de Studio, nunca
existió en el CLI/API, y el usuario preguntó específicamente por el
import de Studio.

---

## IDE-0036 — Asistente IA: soporte multi-proveedor (OpenAI, Google Gemini, Ollama local)

**Estado:** 🟢 Completado. Propuesta por el usuario el 07/08/2026 al abrir
la conversación de alcance de la Fase 5 (Ecosistema): el Asistente IA
(`IDE-0007`) solo podía usar `AnthropicProvider` como proveedor real —
`MockAIProvider` aparte, sin alternativa si el usuario prefiere, ya tiene
crédito en, o quiere comparar contra otro proveedor.

**Alcance acotado con el usuario** antes de construir: OpenAI y Google
Gemini como proveedores cloud con clave de API, más Ollama como
proveedor local sin clave; selección del proveedor activo por
desplegable explícito en Preferencias (no prioridad automática); Ollama
configurado con host/puerto + nombre de modelo en vez de clave.

- `src/boardcomposer/ai/openai_provider.py`/`gemini_provider.py` —
  mismo patrón exacto que `AnthropicProvider`: SDK oficial (`openai`,
  `google-genai`, añadidos a las dependencias del proyecto), clave leída
  del entorno por el propio cliente (`OPENAI_API_KEY`/`GEMINI_API_KEY`),
  sin gestión propia de credenciales. `ollama_provider.py` no trae SDK
  propio — reutiliza el cliente de `openai` apuntado a la API de Ollama
  compatible con el formato de OpenAI (`OLLAMA_HOST` + `/v1`), con
  `OLLAMA_MODEL` obligatorio (sin uno no hay nada coherente que llamar,
  a diferencia de los otros tres que sí tienen un modelo por defecto
  razonable).
- `registry.py`: `BOARDCOMPOSER_AI_PROVIDER` elige explícitamente el
  proveedor activo cuando está definida, por encima del fallback previo
  a este bloque (`anthropic` si hay `ANTHROPIC_API_KEY`, si no `mock`) —
  Preferencias la bridgea igual que ya hacía con la clave de Anthropic
  (`IDE-0034`), el Core sigue leyendo solo el entorno (`ADR-001`).
- **Hallazgo real verificando contra los SDKs reales** (no solo
  documentación): `OpenAI()`/`genai.Client()` lanzan una excepción de
  inmediato si falta su clave — a diferencia de `Anthropic()`, que
  construye sin queja y solo falla en la llamada real. Elegir un
  proveedor sin su clave configurada habría tumbado el arranque de
  Studio (`AssistantService.__init__` resuelve el proveedor de forma
  entusiasta). `AssistantService._resolve_provider()` (nuevo) envuelve
  `default_provider()` en un `try/except`, cayendo a `MockAIProvider`
  con el motivo visible — mismo espíritu que `ask()` ya tenía para un
  fallo del proveedor a media conversación, extendido ahora al momento
  de construcción.
- `PreferencesDialog` gana un desplegable "Proveedor de IA activo" y una
  fila de campos por proveedor (clave enmascarada para
  Anthropic/OpenAI/Gemini, host+modelo para Ollama), visible solo la del
  proveedor seleccionado — `QFormLayout.setRowVisible()`, mismo patrón
  que `ContainerGeneratorDialog` (`IDE-0028`/`IDE-0031`).
  `MainWindow._set_ai_preferences()` generaliza el antiguo
  `_set_anthropic_api_key()` (`IDE-0034`) a los 6 ajustes nuevos, mismo
  bridge QSettings → `os.environ`; `studio/app.py` aplica los 6 al
  arrancar, antes de construir `StudioServices()`.
- Sin tocar `json_response.py`: `strip_json_fence()` ya se aplica de
  forma incondicional en `project_from_text()`/`suggest_strategy()`,
  independientemente del proveedor activo — si OpenAI/Gemini/Ollama
  necesitan algún tratamiento propio de su respuesta solo se sabrá
  probando contra la API real con una clave real, no en esta sesión.
- 34 tests nuevos (`test_openai_provider.py`, `test_gemini_provider.py`,
  `test_ollama_provider.py`, más los ampliados en `test_ai_provider.py`,
  `test_preferences_dialog.py`, `test_assistant_service.py` y
  `test_main_window_ai_preferences.py`, que sustituye a
  `test_main_window_anthropic_api_key.py`). 960 tests en verde,
  `ruff check`/`ruff format --check` limpios. Detectado y corregido en
  el proceso: `_set_ai_preferences()` escribe directo en `os.environ`
  (no vía `monkeypatch`), así que un test que elegía un proveedor dejaba
  su clave filtrada al resto de la sesión de tests — los fixtures
  afectados limpian ahora las 6 variables de entorno relevantes, no solo
  la que cada test cree usar.
- Verificado contra los SDKs reales de OpenAI y Google Gemini (llamada a
  su constructor sin clave, confirmando el fallo inmediato que motiva
  `_resolve_provider()`).
- **OpenAI verificado con una clave real** (07/08/2026, sesión
  posterior): llamada real al SDK (`gpt-4o-mini`), `default_provider()`
  con `BOARDCOMPOSER_AI_PROVIDER=openai` resolviendo a `OpenAIProvider`
  real, y el flujo completo de Preferencias
  (`MainWindow._set_ai_preferences(provider="openai", ...)`) pasando de
  `MockAIProvider` a `OpenAIProvider` real — verificado además con
  contexto de proyecto real: "¿Cuántas piezas tiene mi proyecto actual?"
  sobre un proyecto de 1 pieza respondido correctamente por OpenAI real,
  confirmando que el contexto llega al prompt y la respuesta vuelve por
  el camino real. Captura del diálogo de Preferencias con OpenAI
  seleccionado: solo la fila "Clave API de OpenAI" visible, el resto
  ocultas, como se diseñó. Gemini y Ollama siguen sin verificar con
  credenciales/servidor reales.

**Fuera de alcance:** modelo configurable por el usuario para
OpenAI/Gemini/Anthropic (fijo por constante `DEFAULT_MODEL`, igual que
ya era el caso solo con Anthropic); comparar respuestas de varios
proveedores a la vez; cualquier parche de `json_response.py` específico
de un proveedor nuevo, pendiente de necesidad real.

**Actualización (`DT-0023`, 08/08/2026):** el `.app` publicado en
`v0.3.14` no arrancaba en absoluto — `ModuleNotFoundError: No module
named 'google.genai._gaos.utils.url'` al importar el Asistente IA.
`google-genai` resuelve buena parte de su subsistema interno con
`importlib.import_module()` sobre un nombre calculado en tiempo de
ejecución en vez de sentencias `import` normales, invisible para el
análisis estático de Nuitka. CI en verde (compiló, firmó y notarizó sin
fallos) no lo detectó porque notarizar solo valida la firma del
binario, nunca lo ejecuta — el primer arranque real fue el del usuario
tras descargar la release. Detectado pidiéndole que ejecutara el
binario desde Terminal en vez de con doble clic, para ver el traceback
que Finder/`open` se traga en silencio. Arreglado en `v0.3.15`
añadiendo `--include-package=google.genai --include-package=openai` a
`extra_args` (`studio/pysidedeploy.spec`) — fuerza el empaquetado
completo de ambos paquetes, ignorando lo que Nuitka no puede ver por su
cuenta. Ver `DT-0023` (`DOC-006-DeudaTecnica.md`) para el detalle
completo; pendiente de que el usuario confirme que `v0.3.15` arranca,
sin macOS/Nuitka disponibles para verificarlo en el entorno donde se
hizo el fix.

---

## IDE-0032 — Buscar actualizaciones (menú Ayuda)

**Estado:** 🟢 Completado. Detectada como hueco el 06/08/2026 durante la
checklist de verificación visual de `v0.3.9`
(`docs/RELEASE-SMOKE-v0.3.9.md`): el menú **Ayuda** existía en
`main_window.py` (`_build_menu()`, `menus["Ayuda"]`) pero sin ninguna
acción registrada — no había "Acerca de", ni "Buscar actualizaciones",
ni nada. No era una regresión de ningún fix anterior; nunca se había
construido.

Construida con el alcance acotado en el borrador original, sin
cambios: `studio/update_check.py::check_for_update()` — Qt-free, mismo
patrón que `studio/panels/` — consulta
`GET /repos/edfrutos/boardcomposer-v2/releases/latest` de la API de
GitHub, compara el `tag_name` contra la versión actual, y devuelve un
`UpdateCheckResult` (nunca lanza excepción: red caída, timeout de 5s o
JSON inesperado vuelven como `checked_ok=False` con `error`, no como
un traceback). `MainWindow._check_for_updates()` (acción "Buscar
actualizaciones…" en Ayuda) traduce ese resultado a un `QMessageBox`:
actualización disponible con enlace a la release, ya al día, o aviso
de que no se pudo comprobar — nunca descarga ni instala nada,
solo apunta a la página de GitHub.

Solo bajo demanda (clic en el menú), nunca en el arranque — cumple el
criterio de aceptación original de no bloquear el inicio de Studio.

**Versión actual:** `studio/_version.py::__version__` es la única
fuente fiable de la versión en ejecución — `importlib.metadata`
necesita el dist-info de una instalación normal, que un `.app`
empaquetado con Nuitka (onefile) no lleva. `scripts/check_project.py`
gana un segundo guard (`_check_studio_version_matches_pyproject()`),
mismo patrón que ya vigilaba `pysidedeploy.spec` contra
`pyproject.toml`, para que este tercer sitio con la versión tampoco
pueda desincronizarse sin que el build falle.

Verificado con una llamada real a la API de GitHub (sin mocks) además
de los tests con red simulada, y con una captura real disparando la
acción desde `MainWindow`. 11 tests nuevos (`test_update_check.py` +
wiring en `test_main_window_check_for_updates.py`).

---

## IDE-0033 — Acerca de BoardComposer Studio (menú Ayuda)

**Estado:** 🟢 Completado. Pedida por el usuario el 07/08/2026 junto con
`IDE-0034`/`IDE-0035` en la misma pasada de UAT sobre `v0.3.12`.

Acción "Acerca de BoardComposer Studio…" en el menú Ayuda, con
`QAction.MenuRole.AboutRole` (mismo patrón que `preferences` con
`PreferencesRole` desde `IDE-0025`) para que macOS la reubique en el
menú de la app. `MainWindow._show_about()` muestra nombre de la app,
`studio._version.__version__` (`IDE-0032`) y "Desarrollado por EDF
Developer", vía `QMessageBox.about()`. 3 tests nuevos.

---

## IDE-0034 — Clave de API de Anthropic configurable en Preferencias

**Estado:** 🟢 Completado. `boardcomposer.ai.default_provider()` ya leía
`ANTHROPIC_API_KEY` del entorno, pero un `.app` abierto con doble clic
no hereda las variables exportadas en una Terminal — sin forma de
configurarla desde Studio, el Asistente caía en `MockAIProvider` en
silencio, sin ninguna pista de por qué.

`PreferencesDialog` gana un campo de texto enmascarado (`QLineEdit`,
`EchoMode.Password`) para la clave. `MainWindow._set_anthropic_api_key()`
la persiste en `QSettings` y la vuelca a `os.environ["ANTHROPIC_API_KEY"]`
— el Core (`boardcomposer.ai`) no se toca, sigue leyendo solo el
entorno (`ADR-001`, Core inmutable/environment-driven); Studio es quien
tiende el puente. `AssistantService.reload_provider()` (nuevo) vuelve a
resolver el proveedor sin reiniciar Studio. `studio/app.py` aplica la
clave guardada al arrancar, antes de construir `StudioServices()`, sin
pisar una variable ya exportada externamente. 12 tests nuevos
(diálogo, wiring en `MainWindow`, `reload_provider()`).

**Observaciones:** guardada en texto plano vía `QSettings` (plist en
macOS), no en el llavero del sistema — suficiente para el alcance
pedido, pero un almacén más seguro (Keychain) queda como posible mejora
futura si hace falta.

---

## IDE-0035 — Separar "quitar del tablero" de "eliminar del proyecto"

**Estado:** 🟢 Completado. Reportado por el usuario el 07/08/2026:
"Eliminar pieza" (Backspace, sobre una pieza seleccionada en el
lienzo) era la única forma de borrar una pieza en toda la app, y
borraba las dos cosas a la vez — la quitaba del tablero **y** la
hacía desaparecer del catálogo "Piezas" del Explorer, sin forma de
recuperarla salvo deshacer.

`DeletePieceCommand` (borra pieza + colocación juntas) se conserva sin
tocar, pero deja de ser lo que dispara Backspace. Comando nuevo,
`UnplacePieceCommand` (`studio/commands/unplace_piece_command.py`):
quita solo la colocación, la pieza se queda en el proyecto como "sin
colocar" — mismo estado en el que ya deja piezas el solver cuando no
caben (`_unplaced_piece_ids()`, ya usado por "Calcular layout" y el
reparto por mejor ajuste). `_delete_selected_piece` (Backspace/menú
Editar, sin cambios en el texto ni el atajo) pasa a usarlo.

Para poder seguir borrando una pieza del proyecto del todo,
`Explorer` gana su primer menú contextual (clic derecho sobre una
pieza en Piezas → "Eliminar del proyecto…"), que sí usa
`DeletePieceCommand`. Ambos caminos deshacen con `Ctrl+Z` igual que el
resto de comandos. 8 tests nuevos (`UnplacePieceCommand` + los dos
caminos desde `MainWindow`); el test existente que daba por buena la
fusión de ambos comportamientos se corrigió para reflejar el nuevo
(y correcto) comportamiento.

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

## IDE-0021 — Integración de Stripe para cobro de overage

**Estado:** 🟢 Completado. Dado de alta *antes* de construirse, a diferencia de `IDE-0019`/`IDE-0020` (`DT-0021`, `DT-0022`).

Cierra el hueco que dejaba `IDE-0020`: los planes `basico`/`pro` acumulaban overage (`QuotaResult.overage`) pero no se cobraba nada. El usuario ya tiene una cuenta Stripe usada en comercios de prueba, pendiente de pasar a producción — sin Price IDs de `básico`/`pro` creados todavía, así que la integración se construye completa pero inactiva por defecto (mismo patrón que `REDIS_URL`): sin `STRIPE_SECRET_KEY`/`STRIPE_PRICE_BASICO`/`STRIPE_PRICE_PRO`, todo sigue funcionando exactamente igual que antes de este bloque.

- `src/boardcomposer/stripe_billing.py` (nuevo): `is_configured(plan)`, `create_customer_and_subscription(customer_id, plan)` (Customer + Subscription sobre el Price del plan, devuelve `(stripe_customer_id, subscription_item_id)`) y `report_overage(subscription_item_id)` (`SubscriptionItem.create_usage_record`, *best-effort* — atrapa cualquier excepción de Stripe y solo la registra en log, para que un fallo de facturación no tumbe la petición real del cliente). `stripe` se importa de forma perezosa dentro de `_client()`, así que no hace falta el paquete instalado salvo en producción (`[prod]`).
- `src/boardcomposer/billing.py`: `api_keys` gana `stripe_customer_id`/`stripe_subscription_item_id`, migrados con `ALTER TABLE ... ADD COLUMN` envuelto en `try/except` — necesario porque la `keys.db` real de la VPS ya existía con el esquema de `IDE-0020` antes de este bloque. `create_key()` acepta ambos campos como opcionales.
- `src/boardcomposer/api.py`: en `_authenticate_and_meter()`, cada vez que `check_quota()` devuelve `overage > 0` se llama a `stripe_billing.report_overage()` con el `subscription_item_id` de la clave — una unidad de overage reportada por request por encima de cuota, coherente con el pricing por-solve ya cerrado con el usuario.
- `scripts/manage_keys.py`: `create` crea automáticamente el Customer + Subscription en Stripe cuando el plan es de pago y Stripe está configurado; si no lo está, avisa y emite la clave igual, sin facturación automática.
- `docs/deploy.md`: sección nueva con las tres variables de entorno y el flujo completo.
- Verificado con tests nuevos (`tests/test_stripe_billing.py`, más los añadidos a `tests/test_billing.py` y `tests/test_api_billing.py`) que mockean el módulo `stripe` vía `sys.modules` — no depende del paquete real ni de credenciales de Stripe para pasar en CI. 748 tests en verde.

---

## IDE-0022 — Exportar DXF y JSON desde Studio

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Primer punto de la lista de gaps de Studio identificados en la auditoría de documentación del 01/08/2026 (`SCR-007-Exportación.md`), priorizado por ser el más barato: reutiliza código del Core ya existente sin nada nuevo que inventar. `src/boardcomposer/export/dxf_exporter.py::solution_to_dxf()` (`IDE-0012`) ya existía; solo faltaba conectarlo al flujo de exportación de Studio, que hasta ahora solo tenía SVG/PDF (`studio/export/svg_export.py`/`pdf_export.py`). JSON es un formato nuevo específico de Studio (el `solutions_to_json()` del CLI/API está pensado para varias candidatas con estrategia, no encaja con el layout único y manual de Studio).

- `studio/export/dxf_export.py::export_project_to_dxf()` — mismo patrón exacto que `svg_export.py`: `studio_project_to_solution()` + `solution_to_dxf()` del Core.
- `studio/export/json_export.py::export_project_to_json()` — formato propio (`project_name`, `placed_pieces`, dimensiones totales, `placements` con `piece_id`/posición/rotación), sin la envoltura de estrategia/pesos que no aplica a un layout manual.
- `MainWindow`: dos acciones nuevas en el menú "Exportar" (`Exportar DXF…`, `Exportar JSON…`), mismo patrón que las existentes de SVG/PDF.
- Verificado con tests nuevos (`tests/test_dxf_export.py`, `tests/test_json_export.py`, mismo patrón que `test_svg_export.py`) y con la app real corriendo en macOS: menú "Exportar" confirmado con las 4 opciones, clic en "Exportar DXF…" disparado sin error. 752 tests en verde.

---

## IDE-0023 — Comparador: miniaturas, favorita, fragmentación y nº de cortes

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Segundo punto de la lista de gaps de Studio (auditoría de documentación del 01/08/2026, `SCR-003-Comparador.md`). Cuatro piezas:

- **Miniaturas**: `src/boardcomposer/solver` no interviene aquí — vive en Studio, `studio/export/thumbnail.py::render_solution_thumbnail()`, mismo mecanismo `QPainter` que `pdf_export.py`, escalado a 120×90 px y codificado como `data:image/png;base64,...` embebido directamente en la tabla HTML del Comparador. `comparator_panel.py` recibe la cadena ya renderizada, sigue sin depender de Qt.
- **Favorita**: `MainWindow._mark_favorite_solution()`, 4 acciones nuevas en el menú "Comparar" (mismo patrón que "Aplicar solución N"). Marca con ⭐ en la cabecera de columna. Estado de sesión — se resetea al generar una comparación nueva, no persiste entre reinicios (no hay dónde guardarlo sin decidir antes un modelo de persistencia de soluciones, fuera de alcance).
- **Fragmentación** (`src/boardcomposer/solver/layout_metrics.py::fragmentation_ratio()` — `comparator_panel.py` ya documentaba explícitamente que no se calculaba, a propósito, para no inventar números): `1 - (mayor_rectángulo_libre_mm² / espacio_libre_total_mm²)`, descomponiendo el espacio libre del rectángulo envolvente en rectángulos disjuntos (subtracción rectángulo-menos-rectángulo en 4 partes) tras restar cada pieza colocada. Geometría estándar, sin ambigüedad. Verificado a mano con 3 piezas y dos huecos de tamaño distinto (`tests/test_layout_metrics.py`).
- **Número de cortes** (`layout_metrics.py::cut_count()`, aproximada — avisado al usuario antes de construir): cuenta de líneas de corte interiores distintas (verticales + horizontales) entre bordes de pieza que no coinciden con el borde del rectángulo envolvente, asumiendo corte guillotina de línea completa — mismo supuesto que ya usa el kerf (`DEC-0016`: N piezas en fila = N-1 cortes). Layouts no-guillotina (posibles en MaxRects/Skyline) pueden infracontar; etiquetado "(aprox.)" en la UI, no como cifra exacta.
- Verificado con tests nuevos (`tests/test_layout_metrics.py`, `tests/test_thumbnail.py`, más los ampliados en `tests/test_comparator_panel.py`). 765 tests en verde. Verificación visual en vivo no concluyente esta vuelta — automatización de macOS Accessibility inestable en la sesión (proceso corriendo y confirmado por `lsappinfo`, pero sin ventanas expuestas a `System Events`), no relacionado con el código; se apoya en la cobertura de tests, incluida la generación real de `QPixmap`/`QPainter` en `test_thumbnail.py`.

---

## IDE-0024 — Vista previa antes de confirmar import CSV

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Tercer punto de la lista de gaps de Studio (auditoría de documentación del 01/08/2026, `FLW-002-Importar-CSV.md`). `_import_pieces_csv()` iba directa del selector de fichero a comitear las piezas (`AddPieceCommand` por pieza) — `load_pieces_from_csv()` ya validaba todo-o-nada antes de eso, pero el usuario no veía qué iba a importarse hasta que ya estaba hecho. Un diálogo modal (`CsvImportPreviewDialog`) se interpone entre parseo y comisión: la validación no cambia, solo se añade una confirmación explícita antes de comprometer el proyecto.

- `studio/dialogs/csv_import_preview_dialog.py` — tabla de solo lectura (id/largo/ancho/material/grosor), botones OK/Cancelar, mismo patrón `QDialogButtonBox` que `KerfDialog`. No construye ningún `Command`; solo decide si se sigue adelante.
- `MainWindow._import_pieces_csv()`: tras el `try/except` de `load_pieces_from_csv()` (sin cambios), `preview.exec() != QDialog.DialogCode.Accepted` cancela antes de tocar el proyecto — mismo patrón que los diálogos de alta/edición ya usan para su propio OK/Cancelar.
- Verificado con tests nuevos (`tests/test_csv_import_preview_dialog.py`) y los existentes de `tests/test_main_window_import_csv.py` actualizados para simular la confirmación del diálogo (antes no existía ese paso) más un caso nuevo de vista previa rechazada. 770 tests en verde.

---

## IDE-0025 — Pantalla de Preferencias (tema)

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Cuarto punto de la lista de gaps de Studio (`SCR-006-Preferencias.md`), acotado antes de construir: hoy Studio tiene un único ajuste global real (tema claro/oscuro/automático), ni siquiera persistido entre reinicios — todo lo demás que describe `SCR-006` (idioma, unidades, zoom/grid, defaults de algoritmo/exportación, rendimiento) exigiría infraestructura que no existe (i18n, conversión de unidades en todo el dominio) y no un simple control. Se mueve el ajuste real a un diálogo "Preferencias" dedicado en vez de inventar controles sin efecto — decidido explícitamente con el usuario en vez de rellenar la pantalla con placeholders.

- `studio/dialogs/preferences_dialog.py::PreferencesDialog` — un `QComboBox` (Automático/Claro/Oscuro), mismo patrón `QDialogButtonBox` que el resto de diálogos.
- `MainWindow`: sustituye el antiguo `_build_theme_menu()` (submenú "Ver → Tema" con `QActionGroup`) por una acción "Preferencias…" en el menú "Editar" con `QAction.MenuRole.PreferencesRole` — en macOS, Qt la mueve sola al menú de la aplicación, convención nativa, sin depender de que el texto esté en inglés. `_set_theme()` persiste ahora la elección en `QSettings` (`preferences/theme`) — antes se perdía en cada reinicio; `MainWindow.__init__` la restaura tras construir los paneles (`_apply_panel_stylesheets()` necesita que ya existan).
- Verificado con tests nuevos (`tests/test_preferences_dialog.py`) y los de `tests/test_main_window_view_menu.py` reescritos para el diálogo en vez del submenú — incluido un test de persistencia real: construir una `MainWindow` nueva tras fijar el tema recupera la misma elección. Arreglado de paso un fallo real mío en esta misma sesión: una edición anterior de este documento se había comido la cabecera "## Reglas de mantenimiento". 776 tests en verde. Verificación en la app real: arranque limpio confirmado con ejecución directa (sin errores, bloqueado en su bucle de eventos como se espera) — la introspección de Accessibility de macOS volvió a fallar por el entorno, no por el código (mismo problema que en `IDE-0023`).

---

## IDE-0026 — Timeline: eventos de actividad con categoría y filtro

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Quinto y último punto de la lista de gaps de Studio, y el más costoso: `ADR-003` listaba 9 eventos con nombre (`ProjectCreated`, `SolutionGenerated`, etc.) que nunca se construyeron — solo existe un evento genérico, `"studio.activity"`, publicado desde ~17 sitios distintos con un mensaje en español sin más estructura. `ADR-005` prometía filtrar el Timeline por tipo de evento/algoritmo/intervalo temporal, tampoco construido.

Alcance acotado explícitamente con el usuario antes de construir, distinto del catálogo de `ADR-003` (no encaja con la granularidad real del código): mismo evento único en el bus, con un campo `category` nuevo en el payload en vez de eventos con nombre separados; filtro solo por categoría en la pestaña Actividad, sin filtro por algoritmo (no aplica a la mayoría de entradas) ni por intervalo temporal (ya hay timestamp por línea).

Categorías: `proyecto` (nuevo/abrir/guardar), `tablero` (`AddBoardCommand`/`EditBoardCommand`), `pieza` (`AddPieceCommand`/`EditPieceCommand`/`DeletePieceCommand`/`MovePieceCommand`/`RotatePieceCommand`/`MoveToBoardCommand`), `deshacer` (categoría propia para deshacer/rehacer, no heredada del comando subyacente), `layout` (resolver/aplicar/comparar/favorita), `import` (CSV). Cada clase `Command` declara su `category` igual que ya declara `.name` (`Command` Protocol, `command.py`).

- `studio/commands/command.py`: `Command` Protocol gana `category: str` junto a `name`. Las 9 clases de comando (`AddBoardCommand`, `EditBoardCommand`, `AddPieceCommand`, `EditPieceCommand`, `DeletePieceCommand`, `MovePieceCommand`, `RotatePieceCommand`, `MoveToBoardCommand`, `SetKerfCommand`) declaran su `category` como propiedad, igual patrón que `.name`.
- `studio/activity_log.py`: `ActivityLog` guarda `ActivityEntry` (`timestamp`, `category`, `message`) en vez de strings sueltos; `CATEGORIES` centraliza las 6 categorías reales, no las 9 aspiracionales de `ADR-003`.
- `studio/panels/timeline_panel.py::render_activity()` acepta `entries: list[ActivityEntry]` y un `category: str | None` opcional para filtrar antes de renderizar.
- `MainWindow._log_activity()` ahora exige `category` explícito en cada uno de sus ~15 sitios de llamada; `_execute()` reenvía `command.category`, `_undo()`/`_redo()` fuerzan `"deshacer"`. Pestaña "Actividad" del Timeline gana un `QComboBox` ("Todas" + las 6 categorías) por encima del `QTextEdit`, conectado a `_filter_activity()`.
- Verificado con `tests/test_activity_log.py` (adaptado a `ActivityEntry`), `tests/test_timeline_panel.py` (filtro por categoría), `tests/test_main_window_timeline.py` (nuevo test del combo de filtro). 778 tests en verde.

---

## IDE-0027 — IDs legibles de solución

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Sexto punto aplazado de la lista de gaps de Studio: hoy `AssemblySolution` no tiene ningún identificador — Comparador, mensajes de aplicar/favorita y log de actividad se refieren a cada candidata solo por su posición en la lista (`Solución 1`, `Solución 2`...), que cambia cada vez que se regenera la comparación y no sirve para referenciar una solución concreta más allá de la sesión.

Alcance acotado con el usuario (opción "ambas cosas" de las tres planteadas): una etiqueta de sesión legible (A/B/C/D) sustituye al índice numérico en toda la UI de Studio, más un id corto persistente basado en el contenido (hash de las colocaciones) para poder referenciar la misma solución de forma estable en logs/exports aunque se recalcule en otra sesión.

- `src/boardcomposer/domain/solution.py::AssemblySolution.solution_id` — propiedad calculada (no campo del constructor, para no tocar los ~12 sitios del solver que construyen `AssemblySolution`), hash corto (8 hex) de las colocaciones ordenadas de forma determinista — dos soluciones con las mismas piezas en las mismas posiciones comparten id aunque el solver las genere en órdenes distintos.
- `studio/solution_labels.py::solution_label(index)` — nuevo módulo sin Qt, letras A-Z por índice (con `MAX_COMPARISON_SOLUTIONS = 4` nunca pasa de D).
- `studio/panels/comparator_panel.py`: cabeceras y explicaciones usan la etiqueta en vez de `índice + 1`, con el id corto visible junto a ella.
- `studio/main_window.py`: mensajes de aplicar solución/marcar favorita y sus entradas de `_log_activity` (categoría `layout`) usan la etiqueta para el usuario y el id corto para la traza persistente.
- Verificado con `tests/test_solution.py` (id estable ante reordenación, distinto ante contenido distinto), `tests/test_solution_labels.py` (nuevo), `tests/test_comparator_panel.py` (cabeceras con etiqueta+id) y `tests/test_main_window_apply_layout.py` (mensaje de actividad con etiqueta+id). 784 tests en verde.

---

## IDE-0028 — Generador de piezas de contenedor (caja simple) desde un retal

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Candidata 2 de aprovechamiento de retales (`DOC-999-Ideas.md`, 03/08/2026) — distinta de la Candidata 1 (`DEC-0019`, ya cubierta sin código): en vez de encajar piezas ya definidas contra un retal, genera automáticamente el despiece de un contenedor de almacenaje a partir de sus medidas exteriores. Alcance acotado con el usuario, dejando la puerta abierta a ampliarlo después sin rediseñar el patrón:

- **Tipo v1**: caja simple (base + 4 paredes, sin tapa ni divisores) — el patrón más simple para validar generador → piezas → solver → export antes de generalizar a cajón/cajonera/estantería.
- **Unión v1**: a tope (sin rebaje) — las paredes laterales se recortan `2 × thickness_mm` para encajar entre frontal y trasera; la única regla paramétrica de esta versión.
- **Divisores v1**: ninguno.
- **Ubicación**: diálogo en Studio, mismo patrón que la importación CSV (`IDE-0018`/`IDE-0024`), no un plugin nuevo — sin casos de uso externos todavía que justifiquen esa infraestructura.

Diseño explícitamente extensible sin rediseño: `CONTAINER_TEMPLATES` (`studio/containers/simple_box.py`) es un registro nombre → función, con un único tipo hoy (`caja_simple`); `build_simple_box_pieces()` ya acepta `joint`/`dividers` como parámetros (solo `"a_tope"`/`0` soportados, `ContainerTemplateError` en cualquier otro valor) para que un cajón, una unión rebajada o divisores internos sean una rama nueva en la función y una entrada nueva en el registro, no un sitio de llamada nuevo en Studio — `ContainerGeneratorDialog` ya puebla su desplegable "Tipo de contenedor" desde `CONTAINER_TEMPLATES.keys()`.

- `studio/containers/simple_box.py` — función pura sin Qt (mismo patrón que `csv_import.py`): a partir de largo/ancho/alto exteriores y grosor, calcula 5 `StudioPiece` (`<prefijo>-base`, `-pared-frontal`, `-pared-trasera`, `-lateral-izquierdo`, `-lateral-derecho`). Valida dimensiones finitas positivas, que el ancho exterior admita el grosor de pared (`ancho - 2×grosor > 0`) y que el prefijo de id no choque con piezas ya existentes en el proyecto.
- `studio/dialogs/container_generator_dialog.py::ContainerGeneratorDialog` — largo/ancho/alto exterior, grosor, material y prefijo de id, mismo patrón `QFormLayout`/`QDialogButtonBox` que `PieceDialog`.
- `MainWindow._generate_container_pieces()`: nueva acción "Generar piezas de contenedor…" en el menú "Herramientas" (antes de "Calcular layout"). Exige un tablero activo, reutiliza `CsvImportPreviewDialog` para la confirmación previa (misma tabla genérica de piezas que ya usa `IDE-0024`, sin duplicar código) y añade cada pieza con un `AddPieceCommand` deshacible, igual que `_import_pieces_csv`.
- Verificado con tests nuevos (`tests/test_simple_box.py`, `tests/test_main_window_container_generator.py`) y con la app real: acción confirmada en el menú "Herramientas" (`MainWindow._actions["generate_container"]`, texto y posición correctos). 813 tests en verde.

---

## IDE-0029 — Importar tableros (CSV) en Studio

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

El usuario pidió CSV de tableros/tablas además del de piezas ya existente (`IDE-0018`) — dar de alta un lote de tableros (por ejemplo, retales medidos de una vez, ver `DEC-0019`) exigía repetir el diálogo "Nuevo tablero" uno a uno. Mismo patrón exacto que `IDE-0018`, con `StudioBoard` en vez de `StudioPiece`:

- `studio/project/board_csv_import.py::load_boards_from_csv()` — función pura sin Qt, mismas columnas obligatorias (`id`/`length_mm`/`width_mm`/`thickness_mm`, `material` opcional) y misma validación todo-o-nada que `load_pieces_from_csv()` (`BoardCsvImportError`).
- `studio/dialogs/board_csv_import_preview_dialog.py::BoardCsvImportPreviewDialog` — misma tabla genérica id/dimensiones/material/grosor que `CsvImportPreviewDialog` (`IDE-0024`), adaptada a `board_id`.
- `MainWindow._import_boards_csv()`: nueva acción "Importar tableros (CSV)…" en el menú Archivo, junto a "Importar piezas (CSV)…". A diferencia de la importación de piezas, no exige tablero activo — solo proyecto abierto. Un `AddBoardCommand` deshacible por tablero, mismo patrón que `_import_pieces_csv`. El primer tablero importado queda activo al terminar (mismo comportamiento que `_add_board()`).
- Verificado con tests nuevos (`tests/test_board_csv_import.py`, `tests/test_main_window_import_boards_csv.py`) y con la app real: acción confirmada en el menú Archivo. 832 tests en verde.

---

## IDE-0030 — Reparto por mejor ajuste entre tableros

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

El usuario reportó que "la funcionalidad de aprovechamiento de tablas residuales... no veo que funcione". El mecanismo existente (`LayoutService._fill_other_empty_boards_with_leftovers()`, de `IDE-0019`/anterior) ya repartía piezas sobrantes a otros tableros, pero con dos límites que explican la queja: solo prueba tableros **completamente vacíos** (uno ya parcialmente usado se descarta como candidato) y en el **orden de la lista del proyecto**, sin preferir el retal más ajustado. Acotado con el usuario (opción "mejor ajuste real" de tres alternativas planteadas): considerar todos los tableros a la vez, incluidos los parcialmente usados, priorizando el más pequeño que sea suficiente.

- `LayoutService.apply_best_fit_distribution()` (`studio/layout_service.py`) — ordena todos los tableros del proyecto por área ascendente y, para cada uno con al menos una pieza sin colocar de su mismo grosor, llama a `solve_current_project(board_id)` (el mismo método de un solo tablero que ya usa "Calcular layout"). Heurística voraz (greedy best-fit), no un óptimo global — probar el tablero más pequeño suficiente primero maximiza el aprovechamiento de retales sin explorar combinaciones alternativas. Un tablero sin piezas nuevas que ofrecerle se salta sin invocar al solver, así que nunca se toca de más.
- `BestFitResult` (dataclass nueva) — `boards_used`/`pieces_placed`/`pieces_unplaced`, para que `MainWindow` informe qué pasó sin tener que inspeccionar el proyecto por su cuenta.
- `MainWindow._apply_best_fit_distribution()`: nueva acción "Herramientas → Repartir piezas entre tableros (mejor ajuste)" (`Ctrl+Alt+M`). Exige proyecto abierto, no tablero activo (a diferencia de "Calcular layout"/"Aplicar layout").
- No sustituye al flujo existente (`Calcular layout`/`Aplicar layout`, tablero por tablero) — se añade como alternativa, sin tocar comportamiento ya verificado.
- Verificado con tests nuevos (`tests/test_layout_service.py`, 5 casos nuevos incluido uno que prueba explícitamente que el tablero más pequeño gana aunque esté después en la lista; `tests/test_main_window_best_fit.py`) y con la app real: acción confirmada en el menú Herramientas. 841 tests en verde.

---

## IDE-0031 — Cajón sin rieles en el generador de contenedores

**Estado:** 🟢 Completado. Dado de alta antes de construirse.

Tercera y última pieza pedida junto a `IDE-0029`/`IDE-0030` en la misma
conversación (04/08/2026). Acotado con el usuario (opción "holgura por
hueco de mueble" de tres alternativas planteadas): un cajón que desliza
madera-madera sin rieles metálicos necesita holgura respecto al hueco del
mueble donde va montado, así que sus dimensiones exteriores no se dan
directas — se derivan del hueco (ancho/alto) menos la holgura por lado.

- `studio/containers/drawer.py::build_drawer_no_rails_pieces()` — recibe
  `opening_length_mm`/`opening_height_mm` (hueco del mueble),
  `clearance_mm` (holgura por lado, se resta dos veces de cada dimensión)
  y `depth_mm` (profundidad, independiente del hueco — el hueco solo
  define ancho y alto). Calcula `outer_length_mm`/`outer_height_mm` y
  delega en `build_simple_box_pieces()` (`IDE-0028`) para la lista de
  piezas — mismo cuerpo físico (base + 4 paredes a tope), solo cambia
  cómo se especifican las dimensiones exteriores. Valida holgura
  no-negativa y que no deje el cajón con dimensiones nulas o negativas.
- `CONTAINER_TEMPLATES` pasa a vivir en `studio/containers/__init__.py`
  (antes solo en `simple_box.py`) para que sea el registro combinado de
  ambos módulos, con `"cajon_sin_rieles"` como segunda entrada — ninguna
  otra parte del código cambia para reconocer el tipo nuevo.
- `ContainerGeneratorDialog` — el combo "Tipo de contenedor" ya tenía dos
  huecos (`caja_simple`/`cajon_sin_rieles` en `CONTAINER_TEMPLATES`); las
  filas del formulario cambian con `QFormLayout.setRowVisible()` según el
  tipo elegido (dimensiones exteriores directas vs. hueco+holgura+
  profundidad) y `values()` devuelve la forma de kwargs que espera cada
  función del registro. El prefijo de id por defecto (`caja`/`cajon`)
  cambia con el tipo salvo que el usuario ya lo haya personalizado.
  `MainWindow._generate_container_pieces()` no cambia — ya era genérico
  sobre `CONTAINER_TEMPLATES`.
- Verificado con tests nuevos (`tests/test_drawer.py`,
  `tests/test_container_generator_dialog.py`, caso nuevo en
  `tests/test_main_window_container_generator.py`) y con la app real
  (offscreen): el combo ofrece ambos tipos y `values()` cambia de forma
  correcta al alternar. 873 tests en verde.

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
