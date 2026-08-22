
# NOTEBOOK - BoardComposer

Cuaderno de ingeniería del proyecto.

## 2026-06-26 - Sesión inicial de arquitectura

BoardComposer no será un optimizador de corte tradicional. Será un motor para generar composiciones 2D a partir de tablas disponibles, puntuarlas y explicar sus ventajas e inconvenientes.

### Alcance inicial

- Composición plana 2D.

- Tablas rectangulares.

- Medidas internas en milímetros.

- Motor independiente de la interfaz.

- Salida inicial por consola.

### Queda fuera por ahora

- Modelado 3D.

- Muebles completos.

- Interfaz gráfica.

- IA integrada.

- Uniones complejas de carpintería.

## 2026-07-13 - Actualización de alcance

De lo que "quedaba fuera por ahora" en la sesión inicial, dos puntos ya están construidos:

- **Interfaz gráfica**: BoardComposer Studio (PySide6), completa — workspace, comparador, inspector, gestión de proyectos, exportación SVG/PDF.

- **IA integrada**: Asistente IA (IDE-0007, 6 fases) sobre un proveedor de IA pluggable — todavía sin conectar un proveedor real (usa `MockAIProvider`).

Modelado 3D, muebles completos y uniones complejas de carpintería siguen fuera de alcance. Ver `docs/masterplan/DOC-004-Backlog.md` para el estado vivo de cada funcionalidad.

## 2026-07-22 - Release v0.2.0

Publicada la versión 0.2.0 con todos los cambios acumulados desde 0.1.0. Incluye:

- **IDE-0013–0015**: guía de plugins, receta de despliegue Cloud y visibilidad de plugins instalados (CLI + API).
- **IDE-0016**: tema visual claro/oscuro con detección automática, iconos de línea, toolbar principal y `PromptTextEdit` multilínea en el Asistente.
- **IDE-0017**: despliegue privado en VPS propio (Plesk + Docker): API en `bc.efjdefrutos.com` y Studio accesible por navegador vía noVNC en `studio.efjdefrutos.com`. Autenticación HTTP Basic (nginx) sumada a `BOARDCOMPOSER_API_KEY` y `VNC_PASSWORD`. Cuatro bugs reales detectados y corregidos probando el Studio remoto contra el despliegue real.
- **IDE-0018**: importación de piezas desde CSV en Studio (`Archivo → Importar piezas (CSV)…`), deshacible pieza a pieza.
- Múltiples correcciones de usabilidad detectadas probando datos reales: nodo Soluciones vacío quitado del Explorer, `DeletePieceCommand` que no eliminaba la pieza del inventario, diálogos que cerraban con id vacío/repetido, fila "Orden de piezas" en el Comparador.
- CI: 489 tests en verde. Build del `.app` macOS generado y publicado como asset de la release `v0.2.0` en GitHub Actions (19 min).

Todos los IDEs planificados (IDE-0001–IDE-0018) en 🟢. Próximos pasos sin acotar en `docs/masterplan/DOC-999-Ideas.md`.

## 2026-07-14 - Cierre de las prioridades P0/P1

La IA integrada (2026-07-13) pasa de proveedor simulado a proveedor real: `AnthropicProvider` (SDK `anthropic`, modelo `claude-haiku-4-5`) conectado y verificado con una clave real (IDE-0007). Además:

- Endurecimiento para producción de la API: autenticación por clave (`BOARDCOMPOSER_API_KEY`), rate limiting (Flask-Limiter) y `gunicorn` como servidor WSGI (IDE-0009).
- Importación desde Excel, junto al CSV ya existente (IDE-0010).
- BoardComposer Studio empaquetado como `.app` de macOS con `pyside6-deploy` (IDE-0011).

Con esto no quedan prioridades P0/P1 pendientes en `docs/masterplan/DOC-003-Roadmap.md`; solo P2 (exportación DXF, marketplace/comunidad, cloud).

## 2026-07-26 - Release v0.3.0

Primera versión sin ninguna capacidad nueva: 16 commits de corrección y endurecimiento sobre lo ya entregado en `v0.2.0`, más la revisión completa de la documentación. 673 tests en verde.

- **Números no finitos**: `json.loads()` interpreta `"NaN"`/`"Infinity"` como flotantes, y toda comparación contra `NaN` es falsa — las guardas `< 0`/`<= 0` los dejaban pasar hasta el solver, la puntuación o la exportación. Ahora se exige `math.isfinite()` en cada ruta de entrada externa (API, CSV/Excel, modelos del Core y de Studio, pesos devueltos por la IA). La lección: validar por el signo no basta si el tipo admite valores fuera del orden total.
- **Errores recuperables**: un proyecto con colocaciones colgantes se repara descartándolas y avisando, en vez de rechazar el fichero entero; un CSV malformado da número de fila y código de salida 1, no un traceback. Ambos casos venían de asumir que un fichero propio siempre está bien formado.
- **Multi-tablero**: siete correcciones de Studio con la misma raíz — `LayoutService` seguía razonando como si el proyecto tuviera un solo tablero, meses después de que `DT-0013` introdujera varios. Nació `studio/workspace/placement_fit.py`, el equivalente sin Qt de `PlacementValidator`, para validar lo que ocurre fuera de la escena gráfica.
- **Documentación**: auditada de arriba abajo. Faltaba lo más básico para quien usa la herramienta desde la terminal — ni `--strategy`, ni `--top`, ni `boardcomposer plugins` aparecían en ningún sitio orientado al usuario; ahora en `docs/cli.md`. `INDEX.md` del masterplan estaba vacío desde el primer día. `docs/studio.md` afirmaba todavía que "Studio solo soporta un tablero activo por proyecto".
- **Hallazgo de la auditoría** (`DT-0020`, abierto): el ancho de sierra se configura, se persiste y es deshacible, pero solo lo aplica el arrastre interactivo. Ni el solver ni la exportación lo tienen en cuenta, así que un plano exportado asume corte de anchura cero y el material real no cuadrará. Documentar sirvió para encontrarlo.

## 2026-08-07 - Release v0.3.13

Trece releases de parche desde `v0.3.0` (27/07 a 07/08), todos los IDEs planificados hasta `IDE-0035` en 🟢, sin prioridades P0/P1/P2 pendientes en `DOC-003-Roadmap.md`. 926 tests en verde. Resumen por hilos, no cronológico — el detalle release a release está en `CHANGELOG.md`, el estado vivo de cada funcionalidad en `DOC-004-Backlog.md`.

- **Cierre del hallazgo `DT-0020`** (`v0.3.1`): el kerf pasa de ser solo una ayuda visual del arrastre interactivo a aplicarlo también el solver (`LayoutService.to_core_project()`) y `piece_fits_on_board()`, ensanchando cada pieza un corte a la derecha/abajo y el tablero igual para que se cancele — N piezas en fila exigen N-1 cortes, no N. El Core sigue sin saber qué es un kerf (`DEC-0016`); con `kerf_mm=0` nada cambia. Misma release: primera firma y notarización real del `.app` de macOS (`DEC-0017`), condicionada a que existan las credenciales — sin ellas, build sin firmar como hasta ahora.
- **El `EventBus` de `ADR-003` se usa por primera vez de verdad** (`v0.3.2`, `IDE-0019`): el dock "Timeline" llevaba desde su creación con el texto literal "Timeline / Consola / Eventos", ninguna de las tres cosas construida. Al cablearlo salió a la luz un `AttributeError` dormido (6 de 9 clases de `Command` sin `name`, nunca disparado hasta que el log de actividad lo leyó) y una duplicación entre Inspector y Timeline (extraída a `board_metrics.py`). Primer certificado real contra Apple Developer (`v0.3.3`) encontró y corrigió tres fallos que ningún build sin firmar podía revelar (datos sueltos de Nuitka fuera de `Resources/`, `notarytool --wait` que no comprobaba el estado, binarios de Qt sin extensión saltándose la firma).
- **Deuda de proceso repetida y registrada, no corregida a posteriori** (`DT-0021`/`DT-0022`): `IDE-0019` y `IDE-0020` (claves de API con cuota mensual + Stripe para overage, `v0.3.3`) se construyeron y comitieron antes de pasar por el Backlog, incumpliendo la norma 1 de `MASTERPLAN.md`. Sin impacto en usuario ni código — impacto en trazabilidad, registrado como tal en vez de fabricar un bloque previo ficticio. `IDE-0021` en adelante sí se dio de alta antes de construirse.
- **Barrido de gaps de Studio identificados en la auditoría de documentación del 01/08** (`v0.3.4`-`v0.3.7`): exportar DXF/JSON (`IDE-0022`), miniaturas/favorita/fragmentación/nº de cortes en el Comparador (`IDE-0023`), vista previa de import CSV (`IDE-0024`), diálogo de Preferencias con tema persistente (`IDE-0025`), categorías y filtro en el Timeline (`IDE-0026`), ids legibles de solución A/B/C+hash (`IDE-0027`), generador de piezas de contenedor — caja simple y luego cajón sin rieles (`IDE-0028`/`IDE-0031`), importar tableros CSV (`IDE-0029`) y reparto por mejor ajuste entre tableros (`IDE-0030`).
- **Pulido visual encontrado usando la app de verdad, no en revisión de código** (`v0.3.6`-`v0.3.11`): asset de macOS de `.zip` a `.dmg`; nombre del menú de macOS mostrando "app" en vez de "BoardComposer Studio"; iconos deshabilitados casi invisibles sobre el gradiente del toolbar; pestaña sin seleccionar de un dock tabificado ilegible en tema oscuro; botones flotar/cerrar de la cabecera de los docks casi invisibles en tema oscuro; etiqueta de pieza desbordando el rectángulo en piezas estrechas. Mismo patrón en los cuatro últimos: color explícito en vez de confiar en el pintado nativo de Qt, que ignora la paleta de la app.
- **Última tanda pedida directamente por el usuario en sesiones de UAT sobre releases reales** (`v0.3.9`/`v0.3.12`): buscar actualizaciones desde el menú Ayuda (`IDE-0032`, consulta la API de GitHub bajo demanda, nunca descarga ni instala nada), nombres largos indistinguibles en el selector "Mover a tablero" y en la vista previa de import CSV. Y en `v0.3.13`, en la misma pasada: "Acerca de" en el menú Ayuda (`IDE-0033`), clave de API de Anthropic configurable en Preferencias (`IDE-0034` — un `.app` abierto con doble clic no hereda variables de entorno de una Terminal, así que el Asistente caía en `MockAIProvider` sin ninguna pista de por qué) y separar "quitar del tablero" de "eliminar del proyecto" (`IDE-0035` — Backspace hacía las dos cosas a la vez, sin forma de recuperar la pieza salvo deshacer).

Todos los frentes P0-P2 de `DOC-003-Roadmap.md` completos. El único frente abierto es la Fase 5 (Ecosistema, 🟡 En curso): biblioteca de materiales y comunidad siguen sin empezar; marketplace público sigue sin acotar más allá de la guía de plugins (`IDE-0013`) y la visibilidad de plugins instalados (`IDE-0015`) ya construidas.

## 2026-08-08 - Release v0.3.16

Tres releases desde `v0.3.13` (07/08 a 08/08):

- **Soporte multi-proveedor en el Asistente IA** (`v0.3.14`, `IDE-0036`): además de Anthropic, ahora se puede elegir OpenAI, Google Gemini u Ollama (local, sin clave) desde Preferencias. Verificado con una clave real de OpenAI — SDK, resolución de proveedor y una pregunta con contexto de proyecto real respondidas correctamente. Elegir un proveedor sin clave configurada podía tumbar el arranque de Studio (OpenAI/Gemini lanzan de inmediato si falta la clave, a diferencia de Anthropic); `AssistantService` ahora cae a respuestas de ejemplo con el motivo visible.
- **El `.app` de `v0.3.14` no arrancaba en absoluto** (`v0.3.15`, `DT-0023`): `google-genai` resuelve buena parte de su subsistema interno con `importlib.import_module()` sobre un nombre calculado en tiempo de ejecución en vez de imports literales — invisible para el análisis estático de Nuitka. CI en verde no lo detectó porque notarizar solo valida la firma, nunca ejecuta el binario; el primer arranque real fue el del usuario tras descargar la release, diagnosticado pidiéndole que lo abriera desde Terminal para ver el traceback que Finder se traga en silencio. `studio/pysidedeploy.spec` fuerza ahora el empaquetado completo de `google.genai` y `openai`.
- **Columna `quantity` opcional en el import CSV** (`v0.3.16`, `IDE-0037`): pedido por el usuario porque el diálogo "Pieza"/"Tablero" ya tenía un campo "Cantidad" que nunca llegó al CSV — una fila con `quantity` > 1 se expande a N piezas/tableros idénticos con ids derivados por sufijo, determinista en vez de probar el siguiente sufijo libre en silencio como hace el diálogo: cualquier colisión aborta toda la importación.

## 2026-08-09 - Release v0.3.17

`IDE-0038`, pedido por el usuario para ampliar `IDE-0037` a los tres formatos de CSV (Core, piezas y tableros de Studio) con `quantity` y `material`, en ese orden. Investigar el alcance real sacó a la luz que el Core y Studio no son simétricos:

- **El Core nunca ha tenido `material`** — el único "material" que existía era `material_usage_score`, una métrica del solver (% de aprovechamiento), sin relación con un tipo de madera. Se añadió como campo pasivo en `Board` (se guarda, se expone, no afecta al solver) porque el Core solo empaqueta piezas sobre **una única lámina implícita** (`ProjectConstraints`) — no hay varias tablas entre las que el solver pueda elegir por material. Intentar que "afectara al solver" ahí, como se pidió al principio, no tenía nada que emparejar: hacerlo de verdad exigiría convertir el Core a multi-lámina con material, un cambio de arquitectura mucho mayor que quedó fuera de alcance, a registrar aparte si hace falta.
- **En Studio sí hay varias `StudioBoard` reales**, así que ahí `material` sí pasa de etiqueta a **restricción dura** — mismo patrón exacto que ya existía para `thickness_mm` desde hace varias releases (una pieza de un grosor no encaja en un tablero de otro): mismo `!=` sin comodín, en los mismos puntos de llamada (`LayoutService.to_core_project()`/`apply_best_fit_distribution()`, `MainWindow._edit_board()`/`_edit_piece()`/`_move_piece_to_board()`), nunca dentro de `piece_fits_on_board()` (geometría pura, tampoco comprueba grosor).
- **Lección de proceso**: la primera respuesta a "¿qué alcance debe tener material?" fue "con efecto en el solver" sin que existiera, en el Core, ningún mecanismo con el que ese efecto pudiera engancharse — el diseño se corrigió a mitad de camino, con el usuario, en cuanto se investigó el dominio real en vez de asumir que Core y Studio comparten arquitectura de colocación. 993 tests en verde (15 nuevos sobre `v0.3.16`).

## 2026-08-10 - Release v0.3.18

`IDE-0039`, inventario persistente de retales en Studio — no una idea nueva, sino la mitad que `DEC-0019` (03/08/2026) había dejado deliberadamente sin construir al acotar el aprovechamiento de retales a "solo alta manual, sin inventario persistente, ya cubierto por el modelo actual". Ahora sí: `studio/project/scrap_inventory.py` (capa pura, SQLite, mismo patrón que `billing.py` del Core pero para un recurso de un solo taller) guarda cada retal con `consumed_at` en vez de borrarlo al usarse — la historia sobrevive aunque ya no aparezca disponible. `ScrapInventoryService` resuelve el fichero por defecto vía `QStandardPaths.AppDataLocation`, mismo mecanismo que `QSettings()` ya usa para tema/último proyecto — deliberadamente fuera de `StudioServices`, porque el inventario es del taller, no de un proyecto. Dos diálogos nuevos en el menú "Proyecto" ("Añadir retal…"/"Usar retal…"); usar un retal ejecuta un `AddBoardCommand` deshacible normal, pero el consumo del inventario queda fuera del historial de undo a propósito — deshacer el tablero no lo devuelve al inventario, documentado como decisión, no como limitación descubierta después. 1022 tests en verde (29 nuevos sobre `v0.3.17`), incluida una fixture nueva en `conftest.py` (`QStandardPaths.setTestModeEnabled`) para que ningún test escriba en el perfil real del desarrollador — mismo motivo que ya tenía la fixture equivalente de `QSettings`.

## 2026-08-10 - Release v0.3.19

`IDE-0040`: clic derecho sobre una pieza o un tablero en el lienzo abre un menú contextual con las mismas acciones que ya existían en el menú "Proyecto", más una que no existía en ningún sitio — "Eliminar tablero" — construida de cero (`DeleteBoardCommand`, deshacible, desplaza las piezas del tablero a "sin colocar" en vez de borrarlas, mismo criterio que `UnplacePieceCommand`). Dos hallazgos de la sesión, ninguno obvio de antemano:

- **El botón derecho ya estaba ocupado** (paneo, en cualquier punto del lienzo, incluida una pieza o el tablero) — `BoardWorkspace.mousePressEvent()` tuvo que aprender a distinguir sobre qué se hace clic *antes* de decidir panear o abrir un menú, y la distinción no podía apoyarse en `itemAt()`: la rejilla (`grid.py`) son líneas que cubren todo `sceneRect()`, mucho más grande que el tablero, así que un clic fuera del tablero pero dentro de la rejilla parecía "sobre un elemento" si solo se miraba qué item había debajo. La comprobación real es geométrica, contra `sceneBoundingRect()` del tablero.
- **`QMenu.exec()` no se puede interceptar parcheando la clase** — para que los tests no se quedaran colgados esperando un clic que nunca llega (motivo por el que el menú contextual del Explorer, ya existente, nunca tuvo tests), `monkeypatch.setattr(QMenu, "exec", ...)` a nivel de clase resulta un no-op silencioso: PySide6 sigue despachando al `exec()` real y el test cuelga. Subclasear `QMenu` y parchear el nombre `QMenu` en el módulo de `MainWindow` sí funciona — mismo patrón de "sustituir lo que el código bajo prueba resuelve", no el método en sí.

1037 tests en verde (15 nuevos sobre `v0.3.18`).

## 2026-08-10 - Release v0.3.20

`DT-0024`, reportado por el usuario con una captura: "Buscar actualizaciones" fallaba con `CERTIFICATE_VERIFY_FAILED` en el `.app` real — mismo patrón que `DT-0023` (un intérprete normal no lo ve, un binario congelado por Nuitka sí, porque no localiza el almacén de certificados CA del sistema). `update_check.py` fija ahora el contexto SSL al bundle de `certifi`, ya presente como dependencia transitiva de los SDKs de IA; `pysidedeploy.spec` lo empaqueta completo (código y datos, `cacert.pem` no es un `.py` que Nuitka siga por su cuenta).

Investigar sacó a la luz un segundo bug, sin relación con SSL pero mismo tema de fondo: `studio/_version.py` y el `--macos-app-version` de `pysidedeploy.spec` llevaban **tres releases** (`v0.3.16`–`v0.3.19`) atascados en `0.3.15` — "Acerca de" mostraba la versión equivocada, y peor, el propio comparador de "Buscar actualizaciones" comparaba `"0.3.15"` contra el tag real más reciente, así que alguien ya en la última versión seguía viendo "hay una actualización". `scripts/check_project.py` existe justo para detectar este desfase y llevaba escrito desde hace semanas — nunca se enganchó a ningún workflow de CI, así que nadie lo vio fallar en rojo. Ahora corre en `ci.yml`.

Pendiente de confirmar contra una build real, igual que `DT-0023` — sin macOS/Nuitka en este entorno.

## 2026-08-11 - Release v0.3.21

El usuario probó `v0.3.20` en real y trajo tres cosas de vuelta en el mismo mensaje, ninguna la que se esperaba de entrada:

- **El SSL de `DT-0024` sí se arregló, pero destapó el problema real detrás** (`DT-0025`): con `certifi` puesto, "Buscar actualizaciones" pasó de `CERTIFICATE_VERIFY_FAILED` a `404` — `boardcomposer-v2` es privado, y GitHub devuelve `404` (no `403`) a quien pregunta sin credenciales, para no confirmar ni que el repo existe. La función llevaba rota así desde que se construyó (`IDE-0032`, `v0.3.12`); nunca se vio en este entorno porque el proxy del sandbox autentica toda petición a `api.github.com` de forma transparente, cosa que el `.app` real no tiene. Ni hacer público el repo (expondría `billing.py`/`stripe_billing.py`) ni un token embebido en el binario (extraíble) eran aceptables — decisión del usuario: un Gist público con un solo fichero (`version.json`, versión + URL de la release), nada del código. `update_check.py` apunta ahí ahora.
- **"Cantidad" en vez de "quantity"** (`DT-0026`): "el programa no lee el número de piezas que sí lleva puesto el archivo CSV" — los tres importadores CSV solo reconocían la columna en minúsculas y en inglés, mientras que todo lo demás en la interfaz está en español (el propio diálogo llama "Cantidad" al campo). Sin error, sin aviso: la columna no reconocida simplemente no contaba, quantity caía a 1 en silencio. Aceptan ahora `quantity`/`cantidad`, sin distinguir mayúsculas.
- **Magic Mouse** (`DT-0027`): el menú contextual de `IDE-0040`, publicado el día anterior, "no funciona" — el usuario usa un Magic Mouse de Apple. La detección vivía en `mousePressEvent()` comprobando `Qt.RightButton`, fiable con un botón físico pero no con el clic secundario táctil de un Magic Mouse en macOS. Movida a `contextMenuEvent()`, la abstracción que Qt ofrece precisamente para esto (botón derecho, Magic Mouse, trackpad, tecla Menú, todo normalizado a un único evento) — no un parche específico de dispositivo. Como un botón físico dispara los dos eventos para el mismo clic, `contextMenuEvent()` cancela cualquier paneo en curso antes de abrir el menú, para no dejar la vista atascada en modo paneo cuando `exec()` bloquea y el `mouseReleaseEvent()` nunca llega.

Ningún hallazgo de esta sesión salió de revisar código sin más — los tres vinieron de que el usuario probara la app de verdad. `DT-0025` y `DT-0026` verificados end-to-end en este entorno; `DT-0027` pendiente de confirmar contra un Magic Mouse real, igual que `DT-0023`/`DT-0024` seguían pendientes de macOS real.

## 2026-08-12 - Release v0.3.22

El usuario probó `v0.3.21` en real: `DT-0025` (Gist) y `DT-0027` (Magic Mouse) confirmados sin más — el clic derecho falló solo porque la primera prueba fue sobre el nombre de la pieza en el Explorer, que tiene su propio menú antiguo sin editar, no sobre el lienzo. `DT-0026` (columna `Cantidad`) también funcionaba, verificado con su mismo orden exacto de columnas — pero al comprobarlo salió el mismo bug en otra columna: `Material` con inicial mayúscula (como lo escribió el usuario) tampoco se reconocía, y caía en silencio a "Demo" en vez del material real. Mismo arreglo, generalizado: `_column_from_row()` (antes `_quantity_from_row()`) ahora respalda tanto `quantity`/`cantidad` como `material`, en los tres importadores. 1058 tests en verde.

**Confirmado (12/08/2026):** el usuario probó `v0.3.22` real y reportó de entrada que el problema de `cantidad` seguía ahí — pero la reproducción con su CSV real (`BCS-v2_retales_garaje.csv`, 26 filas, saltos de línea `\r` sueltos en vez de `\n`) confirmó que la importación sí funciona: 26 tableros creados, cantidad expandida en las filas con `cantidad > 1` (`TAB-A01-2`, `TAB-A04-2`, `TAB-A05-2`, `TAB-A11-2`, `TAB-C04-2`, `TAB-C05-2`) y material aplicado tal cual el CSV. El reporte inicial no coincidía con el resultado real ya obtenido — al pedir el detalle exacto (cabecera, fila, síntoma en pantalla) y reproducirlo con el archivo real, resultó estar ya resuelto.

## 2026-08-13 - Release v0.3.23

Con `v0.3.22` cerrado y `DT-0026` confirmado, el usuario pidió empezar la Fase 5 (Ecosistema) del Roadmap — el único frente todavía abierto tras `v0.3.13`. Antes de escribir código: dos de los tres objetivos de la fase (biblioteca de materiales, comunidad) no tenían ninguna definición en `DOC-999-Ideas.md`, ni siquiera una candidata sin acotar — justo el patrón que `DT-0021`/`DT-0022` ya habían dejado registrado como error a evitar ("no funcionalidad sin bloque definido"). Se acotó con el usuario, en la misma sesión, por qué frente empezar y qué alcance darle antes de tocar código, dejando `DEC-0020` y `IDE-0041`.

- **Biblioteca de materiales** (`IDE-0041`): catálogo de materiales del taller — mismo patrón SQLite que el inventario de retales (`IDE-0039`, `v0.3.18`), campos básicos más proveedor y precio, exportable/importable como CSV. `studio/project/materials_library.py` (capa pura) trata cada entrada como dato de referencia sin ciclo de vida — a diferencia de un retal, eliminarla es un `DELETE` real, no un flag de "consumido"; `add_materials_bulk()` inserta la importación completa en una única transacción SQLite, para que una fila mala no deje el catálogo a medias. `studio/project/materials_csv.py` aplicó la lección de `DT-0026` de forma proactiva, sin esperar a que alguien lo reportara: columnas aceptadas también en español y en mayúsculas desde el primer commit.
- **Un diálogo que rompe el patrón del resto del proyecto, a propósito**: todos los demás diálogos de Studio son puros (reciben valores, los validan, los devuelven — el servicio lo llama `MainWindow`). `MaterialsLibraryDialog` no: posee `MaterialsLibraryService` directamente y persiste cada alta/edición/baja/importación al momento, mismo patrón que un gestor de contactos o marcadores. Decisión de diseño, no un descuido — el catálogo no participa del undo/redo de ningún proyecto, así que no hay ningún historial que proteger diferiendo la escritura.
- **El campo "Material" en `BoardDialog`/`PieceDialog` pasa de texto libre a un desplegable editable** con los nombres del catálogo — sigue aceptando cualquier texto no listado, para que un catálogo vacío (instalación nueva) no bloquee crear tableros o piezas.

1215 tests en verde (90 nuevos sobre `v0.3.22`).

## 2026-08-14 - Release v0.3.24

El usuario probó `v0.3.23` con un CSV real de retales de garaje y encontró dos cosas en la misma sesión:

- **Confusión entre dos importadores CSV distintos, no un bug**: "la biblioteca de materiales no me coge los CSV, dice que faltan columnas" — el fichero era `BCS-v2_retales_garaje.csv` (columnas `id,length_mm,width_mm,thickness_mm,cantidad,material`), formato de **importar tableros**, no de la biblioteca de materiales (que exige `id,name,thickness_mm`). No hacía falta tocar código — generar un CSV nuevo con una fila por combinación única de material+grosor (9, luego 8 tras fusionar un typo real del usuario, `Crontachapado`/`Contrachapado`) resolvió la confusión. Verificado ejecutando el mismo camino de código que usa el diálogo (`MaterialsLibraryService.import_csv()`) contra una base de datos aislada, ya que este entorno no puede lanzar la Studio real con ventana — corre en la Mac del usuario, no en el sandbox de desarrollo.
- **Enlace de consulta con el inventario de retales** (`IDE-0042`): el usuario pidió que el catálogo detallara "la medida de cada tablero", esperando que mejorara el aprovechamiento y la colocación automática. Acotado con el usuario antes de programar (mismo patrón que `IDE-0041`): no es un tamaño estándar por material, es vincular el catálogo con el inventario de retales real (`IDE-0039`) — y explícitamente **solo información de consulta**, sin tocar el solver ni `apply_best_fit_distribution()`, descartando la expectativa inicial del usuario de que esto afectara al reparto automático. Columna "Retales" (recuento) y botón "Ver retales…" (dimensiones, procedencia) nuevos en `MaterialsLibraryDialog`.

1136 tests en verde (11 nuevos sobre `v0.3.23`).

## 2026-08-16 - Release v0.3.25

El usuario probó `v0.3.24` en real y dos hallazgos independientes en la misma sesión, ninguno del código de esa release:

- **Regresión de estilo en el Explorer**: `QTreeWidget::item:selected` reutilizaba el degradado de 3 paradas de la toolbar como fondo de la fila seleccionada — sobre la columna estrecha de rama/icono se veía como una mancha de color fuera de lugar, no un resaltado de selección normal. Arreglado a `p.accent` plano.
- **`DT-0028`**: "Buscar actualizaciones" no avisaba de `v0.3.24` teniendo instalada `v0.3.23` — no un fallo del comparador, sino que el Gist público que lee (`DT-0025`) llevaba **dos releases sin actualizarse a mano** (`v0.3.23`, `v0.3.24`), el mismo tipo de paso-manual-que-se-olvida que ya había pasado con `studio/_version.py` en `DT-0024`. Mitigado a mano en el momento (Gist actualizado vía API); pero al preguntar el usuario por qué "Buscar actualizaciones" no descargaba e instalaba automáticamente, salió que **nunca lo había hecho** — solo comparaba versiones y mostraba un enlace, documentado ya en `DOC-999-Ideas.md` pero nunca comunicado con claridad.

Acotado con el usuario antes de programar, mismo patrón que el resto del proyecto: de las dos candidatas de auto-actualización, se construye la de menor alcance — descargar el `.dmg` y abrirlo (Finder monta la imagen), no una instalación completa estilo Sparkle (`DEC-0021`). Al acotarlo salió un bloqueo real, no anticipado: los assets de una release de un repo **privado** exigen autenticación para descargarse (`404` sin ella, mismo patrón que `DT-0025` pero para el binario, no la versión) — verificado en directo contra la release real (`curl` sin credenciales devolvió `404` en el repo privado). El Gist público resuelve *saber* la versión, pero no sirve para *distribuir* el binario. Ni hacer público el repo entero (expondría `billing.py`/`stripe_billing.py`) ni embeber un token en el binario eran aceptables — mismo criterio que `DT-0025` — así que se creó un segundo repo, público y sin código, `edfrutos/boardcomposer-releases`, solo para alojar los `.dmg`.

Construido como `IDE-0043`: `studio/update_installer.py` (nuevo, sin Qt, mismo patrón de separación que `update_check.py`) descarga con progreso y cancelación cooperativa, y abre el `.dmg` con `open`; `MainWindow._check_for_updates()` pide confirmación antes de descargar, con `QProgressDialog` cancelable corriendo síncrono con `QApplication.processEvents()` — mismo patrón que ya usa el Asistente IA, sin introducir `QThread` nuevo en la base de código. `package-studio.yml` sube el `.dmg` también al repo público y actualiza el Gist (`scripts/update_version_gist.py`) en cada release, con un secret de alcance mínimo (`RELEASES_REPO_TOKEN`, fine-grained: solo escritura sobre `boardcomposer-releases` + Gists) — cierra `DT-0028` de raíz, ya no depende de que nadie se acuerde.

Verificado en vivo el mismo día, sin esperar a que este release lo empaquetara: `.dmg` de `v0.3.24` subido a mano al repo público con el token real, Gist actualizado, y `check_for_update("0.3.23")` devolviendo el `dmg_url` real con descarga pública confirmada sin autenticación (`302` a una URL firmada de S3).

1149 tests en verde (13 nuevos sobre `v0.3.24`).

## 2026-08-18 - Release v0.3.26

El usuario probó `v0.3.25` en real y confirmó que el flujo de auto-actualización funciona (sin más detalle posible: una vez en la última versión, no hay contra qué probar la descarga). Con eso cerrado, preguntó abiertamente qué más podría dejar la aplicación con "servicios más potentes" — no un bug ni una petición concreta, una invitación a proponer.

De las dos candidatas propuestas (presupuesto automático desde la biblioteca de materiales, o priorización de retales en el solver), el usuario eligió retomar la segunda — la que `DEC-0019` (03/08/2026) había dejado deliberadamente sin acotar como "posible ampliación futura, si el uso real lo pide". Acotado con el usuario antes de programar, mismo patrón que el resto del proyecto: descartó que el solver decida solo qué retal usar (`DEC-0022`) — prefiere seguir eligiendo él, pero en el momento justo, no en un menú aparte del que hay que acordarse.

Construido como `IDE-0044`: "Usar retal del inventario…" desaparece como entrada de menú independiente; su selector (`UseScrapDialog`) gana un botón "Tablero nuevo…" y pasa a abrirse **desde** "Añadir tablero…" cuando el inventario tiene algo disponible — un único diálogo, no un selector previo seguido de otro. `MainWindow._add_board()` pasa de "abrir BoardDialog" a orquestador: con inventario vacío no cambia nada; con inventario disponible, distingue tres salidas del diálogo (retal elegido → `_apply_scrap_as_board()`, nueva; "Tablero nuevo…" pulsado → cae al `BoardDialog` de siempre, ahora `_add_new_board()`; cancelado → no hace nada). Sin tocar `LayoutService` ni el solver en absoluto — la decisión sigue siendo 100% manual, solo mejor situada.

1153 tests en verde (4 nuevos sobre `v0.3.25`).

## 2026-08-20 - Release v0.3.27

El usuario probó `v0.3.26` en real: "Buscar actualizaciones" ya descargaba y abría el `.dmg` (`IDE-0043`), pero seguía teniendo que cerrar la app a mano y arrastrar el icono a Aplicaciones — la fricción real de vivir con `v0.3.25`/`v0.3.26` en producción llevó a pedir directamente retomar la candidata de mayor alcance de `DOC-999-Ideas.md` ("Auto-actualización de BoardComposer Studio"): "hay que depurar el producto y minimizar tarea al usuario".

Acotado con el usuario antes de programar (`DEC-0023`), dos decisiones reales:

- **Sparkle de verdad, descartado.** El framework está pensado para bundles construidos con Xcode; empotrarlo en un `.app` de Nuitka habría exigido firmar componentes de terceros dentro del bundle — la misma categoría de fragilidad que ya dio tres bugs reales la primera vez que este proyecto firmó contra un certificado real (`DT-0011`). En su lugar, un actualizador propio que consigue el mismo resultado sin el framework: no hace falta ninguna clave de firma de actualizaciones nueva, el `.dmg` que instala ya está firmado y notarizado por el CI (`IDE-0043`).
- **"Copia directa, sin respaldo"**, elección explícita del usuario frente a la alternativa recomendada (swap atómico con `.bak` restaurable). La implementación sí hace un rename atómico intermedio dentro del mismo directorio — no para conservar un respaldo tras completar, sino para no dejar nunca la ruta sin ningún `.app` válido si algo falla a mitad, que es un riesgo distinto del que el usuario descartó.

Construido como `IDE-0045`: `studio/self_update.py` monta el `.dmg` (`hdiutil`), copia el `.app` con `ditto` (preserva los atributos extendidos de los que depende la firma — `shutil.copytree` no), valida `CFBundleShortVersionString` contra la versión esperada, y sustituye con dos renames atómicos. Instala siempre en la ruta desde la que se ejecuta hoy, nunca fuerza `/Applications` — respeta dónde la tenga cada usuario sin pedir privilegios que no tenga ya. `closeEvent()` se refactorizó para exponer `_maybe_save_and_confirm_close()`, reutilizada por el nuevo flujo: sustituir la app con un proyecto sin guardar sería pérdida de datos real, no solo mala UX, así que la misma comprobación que ya protegía el cierre de la ventana protege ahora la actualización. Fuera de un `.app` empaquetado (fuente, tests), el flujo cae intacto al de `IDE-0043` — nadie que corra desde código pierde nada.

1165 tests en verde (12 nuevos sobre `v0.3.26`).

## 2026-08-20 - Release v0.3.28

El usuario instaló `v0.3.27` (primera con `IDE-0045`) y pidió probar el auto-update de verdad. Sin nada más pendiente en el backlog en ese momento, esta release es solo el número de versión subido — la única forma de darle a `v0.3.27` algo que detectar y ejercitar el flujo completo en real: descarga, comprobación de cambios sin guardar, sustitución del `.app` en marcha y relanzado, todo sin cerrar nada a mano.

## 2026-08-20 - Release v0.3.29

Primera prueba real de `IDE-0045` (`v0.3.27` → `v0.3.28`), y salió a medias: la app descargó la actualización, se cerró y se sustituyó a sí misma — pero no volvió a abrirse. Dos preguntas de seguimiento acotaron el fallo antes de tocar nada: la sustitución del `.app` sí se había completado ("se instaló"), así que el problema estaba solo en `relaunch()`, no en `install_update()`.

Causa (`DT-0029`): `relaunch()` llamaba a `open <ruta>` **antes** de `QApplication.quit()` — con el proceso viejo todavía vivo en ese mismo `bundle path`, Launch Services de macOS puede tratar la petición como "esta app ya está en marcha" (activar la instancia casi muerta, o no hacer nada) en vez de arrancar una nueva. Exactamente el problema que Sparkle resuelve con un proceso auxiliar separado que espera a que el padre termine de verdad antes de relanzar — este proyecto no tiene ese auxiliar (`IDE-0045` lo descartó por la fragilidad de firmar componentes de terceros en el bundle), así que hizo falta el mismo tipo de espera, pero minimalista: `relaunch()` gana `wait_for_pid`, que en vez de llamar a `open` directamente lanza un `/bin/sh -c` desacoplado sondeando `kill -0 <pid>` hasta que el proceso indicado desaparece de verdad, y solo entonces `open -n` (fuerza una instancia nueva, por si Launch Services sigue confundido sobre un bundle identifier recién liberado). `MainWindow` le pasa `os.getpid()`.

Pendiente de confirmar contra esta release, mismo patrón que `DT-0023`/`DT-0024`/`DT-0027`: un fallo que solo se ve en real, corregido con la mejor hipótesis disponible, a la espera de que el usuario lo pruebe.

1166 tests en verde (1 nuevo sobre `v0.3.27`).

## 2026-08-20 - Release v0.3.30

El tag `v0.3.29` nunca llegó a construirse: el job ni arrancó, "recent account payments have failed or your spending limit needs to be increased" — límite de gasto de GitHub Actions agotado. Runners de macOS en un repo privado cuestan ~10x un minuto de Linux, y con builds de ~60-70 min y varias releases en dos días (una de ellas solo para probar, sin cambio de código), el gasto se disparó rápido.

Tres salidas sobre la mesa: hacer el repo público (Actions gratis e ilimitadas, pero expone `billing.py`/`stripe_billing.py` — justo lo que `DT-0025` decidió no hacer), subir el límite de gasto (sigue constando, no arregla nada de fondo), o un runner autoalojado en el propio Mac del usuario (gratis, repo sigue privado, usa hardware que de todas formas está encendido para instalar cada build a mano). El usuario eligió la tercera.

`package-studio.yml` pasa de `runs-on: macos-latest` a `runs-on: [self-hosted, macOS]`. Un detalle que solo importa en un runner persistente, nunca en uno efímero de GitHub: el paso de firma cambiaba el keychain **por defecto** del sistema y nunca lo restauraba — en una VM que se destruye tras el job da igual, pero en el Mac real del usuario, reutilizado release tras release, iría dejando el keychain por defecto apuntando a una ruta de build y acumulando ficheros sueltos. Arreglado: el keychain temporal pasa a tener un nombre único por ejecución (`$GITHUB_RUN_ID`), y un paso nuevo con `if: always()` restaura el keychain por defecto original y borra el temporal — incluso si el job falla a mitad.

Sin cambios de producto — esta release es solo para que el tag correspondiente lleve ya el workflow corregido; `v0.3.29` (el arreglo real, `DT-0029`) sigue pendiente de confirmar contra un build de verdad, ahora sí posible.

## 2026-08-20 - Release v0.3.31

Primera ejecución real de `v0.3.30` en el runner nuevo: falló en `actions/setup-python@v5` con `mkdir: /Users/runner: Permission denied`. Causa, típica de runners autoalojados: `setup-python` asume por defecto que puede instalar en `/Users/runner` — el nombre de la cuenta que usan los runners macOS *alojados por GitHub*, no una ruta genérica. En este Mac la cuenta es `edefrutos`, no `runner`, así que ese directorio ni existe ni es escribible por el usuario que ejecuta el runner. Arreglado apuntando `AGENT_TOOLSDIRECTORY` (la variable que `setup-python` respeta para el toolcache) a `${{ runner.temp }}/toolcache` — siempre dentro del propio árbol de trabajo del runner, escribible sea cual sea la cuenta real.

Segundo problema de fondo del mismo momento, sin arreglo de código posible: `ci.yml` (Linux, gratis) también falló, mismo motivo que bloqueó `v0.3.29` en macOS — "recent account payments have failed" en la cuenta de GitHub del usuario. Un pago fallido bloquea *todos* los runners alojados por GitHub, no solo los que superan cuota; el runner autoalojado no depende de eso, así que `Package Studio` sigue funcionando aunque `ci.yml` no.

## 2026-08-20 - Release v0.3.32

`v0.3.31` rompió el workflow entero, no solo el paso de `setup-python` que intentaba arreglar (`DT-0031`): el arreglo anterior puso `AGENT_TOOLSDIRECTORY: ${{ runner.temp }}/toolcache` en el `env:` de nivel de job — pero el contexto `runner` (necesario para `runner.temp`) solo está disponible dentro de `steps`, no en el `env:` del job. El resultado no fue un error de sintaxis YAML genérico (el fichero es YAML válido de sobra, verificado con PyYAML sin problema) sino un fallo de validación específico de GitHub Actions: el workflow ni llegó a parsear como Acciones válidas — cero jobs listados, y el propio nombre "Package Studio" se mostró como la ruta del fichero, señal clásica de que GitHub ni siquiera pudo leer el `name:` del workflow. Confirmado el diagnóstico contra un issue real y conocido de `actions/runner` (#2204, "Runner context non available in expression in jobs.<job_id>.env") antes de volver a taggear, para no fallar una tercera vez a ciegas.

Arreglado moviendo `AGENT_TOOLSDIRECTORY` al `env:` del paso `actions/setup-python@v5` en concreto, donde `runner` sí es un contexto válido. Lección para el futuro: los contextos de GitHub Actions no son intercambiables entre los distintos niveles de un workflow (job vs step) aunque la sintaxis `${{ }}` sea idéntica en ambos sitios — y una expresión inválida en un sitio equivocado puede tumbar el workflow entero sin dejar ningún job ni log al que agarrarse, solo una anotación en el check-run del commit.

## 2026-08-20 - Release v0.3.33

`v0.3.32` arregló el parseo del workflow (`DT-0031`) pero no el problema de fondo: `setup-python` volvió a fallar con el mismo `mkdir: /Users/runner: Permission denied`, ahora con `AGENT_TOOLSDIRECTORY` resuelto correctamente en el log (`/Users/edefrutos/actions-runner/_work/_temp/toolcache`) — la variable ni se estaba leyendo para este paso concreto. Investigado antes de un tercer intento a ciegas: los binarios de Python para macOS que descarga `actions/python-versions` están compilados con rutas de librería compartida fijas, **no relocalizables**, hardcodeadas a `/Users/runner/hostedtoolcache` — ninguna variable de entorno (`AGENT_TOOLSDIRECTORY`, `RUNNER_TOOL_CACHE`) lo evita de verdad en macOS, confirmado contra varios issues abiertos de `actions/setup-python` (#792, #974, entre otros) sobre exactamente este mismo síntoma en runners autoalojados de Mac.

Resuelto quitando `actions/setup-python@v5` del job por completo: un runner autoalojado, a diferencia de uno efímero de GitHub, se espera que ya tenga sus prerrequisitos — mismo criterio que ya aplica el propio Studio para el entorno de un desarrollador. El paso nuevo comprueba que `python3.13` existe en el Mac (si no, falla rápido con un mensaje claro en vez de otro error confuso de 10 minutos) y crea un venv aislado en `$RUNNER_TEMP` por cada ejecución, añadido a `$GITHUB_PATH` — ni toca el Python del sistema ni depende de un mecanismo pensado para provisionar VMs desde cero.

## 2026-08-20 - Release v0.3.34

Con `v0.3.33` el pipeline llegó, por primera vez, hasta compilar y empezar a firmar — y ahí falló con un error nuevo: `Warning: unable to build chain to self-signed root for signer` / `errSecInternalComponent`. No tenía nada que ver con Python; era el certificado intermedio de Apple (Developer ID Certification Authority G2), ausente en este Mac — en los runners alojados por GitHub viene preinstalado, en una máquina que nunca ha firmado con Xcode, no. Primer intento: pedir al usuario que lo instalara a mano en su llavero de sesión (`security add-certificates -k ~/Library/Keychains/login.keychain-db`). Falló exactamente igual al reintentar — el runner, corriendo como servicio en segundo plano (`launchd`), no tiene necesariamente el llavero de sesión en su lista de búsqueda efectiva, así que `codesign` seguía sin verlo.

Arreglo definitivo, más robusto que depender del estado de un llavero externo: el propio `package-studio.yml` descarga el certificado intermedio de Apple e lo importa **dentro del llavero temporal de la build**, junto al certificado de firma — autocontenido, sin ninguna configuración manual por máquina, y válido igual para cualquier otro runner autoalojado que se añada en el futuro.

Quinto intento seguido de arreglar el pipeline en el mismo runner (`DT-0030` a `DT-0033`) — cada fallo llegó más lejos que el anterior (permisos → parseo del workflow → binarios no relocalizables → cadena de certificados), señal de que el proceso de depurar contra un entorno real, aunque lento (cada vuelta son ~40 min de build), sí iba convergiendo.

## 2026-08-22 - Release v0.3.36

El usuario confirmó `v0.3.35` en real en su Mac: arranque con doble clic y `.dmg` sin bloqueo de Gatekeeper, ambos checks de `CHECKLIST-operativa.md` que solo se pueden verificar fuera de CI. Quedaba el tercero, el ciclo completo de auto-actualización (`IDE-0045`) — pero necesita una versión más nueva que la ya instalada para tener algo que ofrecer. Esta release es solo el número de versión subido, mismo patrón que `v0.3.28` para el mismo propósito.

De paso, primer tag empujado junto con su rama desde `d999825` (21/08/2026): la concurrencia (`cancel-in-progress`) añadida a `package-studio.yml` para evitar la build duplicada que ya se vio en `v0.3.31`/`v0.3.35` (mismo `head_sha`, dos eventos `push` para rama y tag) sigue sin confirmarse contra un push real de los dos juntos — este lo es.

Sin cambios de producto ni de tests.
