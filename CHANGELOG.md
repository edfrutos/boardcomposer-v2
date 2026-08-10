# CHANGELOG - BoardComposer

## 0.3.20 - 2026-08-10

### Arreglado

- "Buscar actualizaciones" fallaba en el `.app` empaquetado con `<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate>`, reportado por el usuario con una captura (`DT-0024`). El binario congelado por Nuitka no localiza el almacén de certificados CA del sistema como sí lo hace un intérprete normal — `update_check.py` ahora fija el contexto SSL al bundle de `certifi` (ya instalado como dependencia transitiva de los SDKs de IA), y `pysidedeploy.spec` lo empaqueta completo (código y datos).
- `studio/_version.py` y el `--macos-app-version` de `pysidedeploy.spec` llevaban atascados en `0.3.15` desde `v0.3.16` — tres releases con la versión de "Acerca de" y del bundle equivocadas, y con el comparador de "Buscar actualizaciones" creyendo siempre desactualizada la última versión real. `scripts/check_project.py` ya detectaba justo este desfase, pero nunca se había enganchado a ningún workflow de CI; ahora corre en `ci.yml`, así que un desfase futuro rompe el pipeline en vez de pasar desapercibido.

---

## 0.3.19 - 2026-08-10

### Añadido

- Menú contextual (clic derecho) sobre una pieza o un tablero en el lienzo (`IDE-0040`): sobre una pieza, "Editar pieza…" y "Eliminar del proyecto…"; sobre el tablero, "Editar tablero…" y "Eliminar tablero…" — esta última no existía en ningún sitio hasta ahora. Eliminar un tablero desplaza sus piezas a "sin colocar" en vez de borrarlas, deshacible como cualquier otro comando. El botón derecho en el área vacía del lienzo sigue paneando exactamente igual que antes.

---

## 0.3.18 - 2026-08-10

### Añadido

- Inventario persistente de retales en Studio (`IDE-0039`): dos entradas nuevas en el menú "Proyecto" — "Añadir retal al inventario…" registra un resto de tablero (dimensiones, material, grosor, procedencia) en un almacén SQLite local que sobrevive entre proyectos y reinicios de Studio; "Usar retal del inventario…" lista los retales disponibles (ordenados por área ascendente) y añade el elegido como tablero del proyecto activo, deshacible como cualquier otro tablero. Un retal nunca se borra al usarse — se marca consumido, no se elimina, así que la historia queda registrada. Promovida desde una idea sin acotar en `DOC-999-Ideas.md` que en agosto se había dejado deliberadamente sin inventario persistente.

---

## 0.3.17 - 2026-08-09

### Añadido

- Columnas `quantity` y `material` (en ese orden) en el CSV del Core/CLI (`IDE-0038`), que hasta ahora no admitía ninguna de las dos: `quantity` expande una fila en N tablas idénticas, con ids derivados por sufijo si la fila trae `id` (sin él, las N tablas quedan sin id, igual que hoy). `material` se añade como campo nuevo y pasivo en `Board` — se guarda y se puede leer, pero sin efecto en el solver, porque el Core empaqueta las piezas sobre una única lámina implícita y no tiene varias tablas entre las que elegir por material.
- En Studio, `material` deja de ser una etiqueta decorativa: pasa a ser una restricción dura, exactamente el mismo patrón que ya existía para `thickness_mm` — una pieza de un material no encaja en un tablero de otro. Afecta al solver (`LayoutService.to_core_project()`, `apply_best_fit_distribution()`) y a las acciones manuales de `MainWindow` (mover pieza a otro tablero, editar pieza o tablero).

### Cambiado

- Documentación de los tres formatos de CSV (Core, piezas y tableros de Studio) reordenada a `quantity`, `material` — sin cambio funcional, `csv.DictReader` lee por nombre de columna, no por posición.

---

## 0.3.16 - 2026-08-08

### Añadido

- Columna `quantity` opcional en el import CSV de piezas y tableros de Studio (`IDE-0037`): una fila con `quantity` > 1 se expande a esa cantidad de piezas/tableros idénticos, con ids derivados por sufijo (`P-101`, `P-101-2`, `P-101-3`, ...) — mismo esquema que el campo "Cantidad" de `PieceDialog`/`BoardDialog`, pero determinista en vez de probar el siguiente sufijo libre en silencio: cualquier id derivado que choque con el fichero o con el proyecto abierto aborta toda la importación, igual que un id literal repetido. Ausente o vacía, equivale a `quantity=1` — mismo comportamiento que hasta ahora.

---

## 0.3.15 - 2026-08-08

### Arreglado

- El `.app` de `v0.3.14` no arrancaba en absoluto tras descargarlo: `ModuleNotFoundError: No module named 'google.genai._gaos.utils.url'` al importar el Asistente IA. `google-genai` resuelve buena parte de su subsistema interno con `importlib.import_module()` sobre un nombre calculado en tiempo de ejecución en vez de sentencias `import` normales — invisible para el análisis estático de Nuitka, que solo empaqueta lo que puede ver siguiendo imports literales. La build había compilado, firmado y notarizado sin fallos (notarización solo valida la firma, nunca ejecuta el binario), así que CI en verde no lo detectó — el primer arranque real fue el del usuario tras descargar la release. `studio/pysidedeploy.spec` fuerza ahora el empaquetado completo de `google.genai` y `openai` (`--include-package`), no solo lo que Nuitka detecta por su cuenta.

---

## 0.3.14 - 2026-08-07

### Añadido

- Soporte multi-proveedor en el Asistente IA (`IDE-0036`): además de Anthropic (Claude), ahora se puede elegir OpenAI (GPT), Google Gemini u Ollama (local, sin clave — host/puerto + nombre de modelo) como proveedor activo, desde un desplegable nuevo en Preferencias. Verificado con una clave real de OpenAI: llamada real al SDK, resolución del proveedor a través del flujo completo de Preferencias, y una pregunta con contexto de proyecto real respondida correctamente por OpenAI.

### Corregido

- Elegir un proveedor de IA sin su clave configurada (p. ej. OpenAI o Gemini recién seleccionados en Preferencias, sin clave todavía) podía tumbar el arranque de Studio — los clientes de OpenAI/Gemini lanzan una excepción de inmediato si falta la clave, a diferencia de Anthropic. `AssistantService` ahora cae a respuestas de ejemplo con el motivo visible, en vez de crashear.

---

## 0.3.13 - 2026-08-07

### Añadido

- Acerca de BoardComposer Studio… en el menú Ayuda (`IDE-0033`), con la versión actual y "Desarrollado por EDF Developer".
- Clave de API de Anthropic configurable en Preferencias (`IDE-0034`) — un `.app` abierto con doble clic no hereda variables de entorno de una Terminal, así que sin esto el Asistente caía en respuestas de ejemplo sin ninguna pista de por qué.

### Cambiado

- "Eliminar pieza" (Backspace, sobre una pieza en el lienzo) ahora solo la quita del tablero activo — se queda en Piezas como "sin colocar", reubicable después (`IDE-0035`). Para borrarla del proyecto del todo, Explorer tiene un menú contextual nuevo (clic derecho sobre una pieza en Piezas → "Eliminar del proyecto…").

### Arreglado

- `ruff format --check .` fallaba en CI sobre el commit anterior — dos archivos nunca se habían pasado por `ruff format` (solo por `ruff check`, que no valida estilo).

---

## 0.3.12 - 2026-08-07

### Añadido

- Buscar actualizaciones desde el menú Ayuda (`IDE-0032`), que existía pero estaba completamente vacío desde siempre. Consulta la última release publicada en GitHub y ofrece el enlace si hay una versión más reciente — nunca descarga ni instala nada. Solo bajo demanda (clic en el menú), nunca en el arranque; un fallo de red se muestra como aviso, no como bloqueo.

### Arreglado

- Nombres largos recortados en el selector "Mover a tablero" y en la vista previa de importación CSV (piezas y tableros): con ids que comparten un prefijo largo (`TAB-A01`, `TAB-A02`, ...) todos se veían indistinguibles. El combo del selector ahora se ajusta a su elemento más ancho; en las tablas de vista previa, las columnas Id y Material se ajustan a su contenido en vez de repartirse el ancho a partes iguales con las numéricas.

---

## 0.3.11 - 2026-08-06

### Arreglado

- Etiqueta de pieza desbordaba el rectángulo en piezas estrechas: los nombres largos que genera el generador de contenedores (`caja_simple-lateral-izquierdo`, etc.) se dibujaban con el `piece_id` completo, sin ajustar al ancho real de la pieza — visible sobre todo en las piezas del borde, sin ninguna otra pieza que las tapara. `BoardPieceItem._update_label_elision()` (`studio/workspace/board_piece_item.py`) trunca la etiqueta con elipsis para caber siempre en el rectángulo, recalculando al rotar; el id completo queda disponible como tooltip si queda truncado.

---

## 0.3.10 - 2026-08-06

### Arreglado

- Botones de flotar/cerrar en la cabecera de cualquier dock (Explorer, Inspector, Timeline, Comparador, Asistente, docks de plugin) casi invisibles en tema oscuro: usaban el icono nativo de Qt, que ignora la paleta de la app por completo (confirmado incluso forzando `QPalette.WindowText`/`ButtonText`, sin efecto). `MainWindow._style_dock_titlebar()` sustituye la cabecera nativa por una propia, con los botones dibujados vía `icons.py` — mismo patrón que el fix de las pestañas de dock tabificado (`0.3.9`).

---

## 0.3.9 - 2026-08-05

### Arreglado

- Pestaña sin seleccionar de un dock tabificado ("Timeline", "Inspector") casi ilegible: no tenía ninguna regla QSS propia, así que su fondo caía al color nativo del estilo de la plataforma en vez de la paleta de la app — `build_stylesheet()` (`studio/theme.py`) ahora fija fondo y color propios en `QTabBar`/`QTabBar::tab`, mismo patrón que ya usa `panel_html_stylesheet()` para el mismo tipo de problema (color explícito en vez de depender del pintado nativo).

---

## 0.3.8 - 2026-08-05

### Arreglado

- El menú de macOS (barra superior) mostraba "app" en vez de "BoardComposer Studio": `--macos-signed-app-name` fija el bundle identifier, no el nombre visible (`CFBundleName`) — falta `--macos-app-name` en `studio/pysidedeploy.spec`.
- Iconos de acciones deshabilitadas casi invisibles sobre el gradiente de color del toolbar (la mayoría en un proyecto nuevo: undo/redo, piezas, solver...). Qt genera el modo `Disabled` por defecto desaturando y bajando la opacidad al ~30%, borrando casi del todo un icono de trazo fino — `build_icons()` (`studio/icons.py`) ahora registra su propio pixmap en modo `Disabled` con opacidad fija al 45%.

---

## 0.3.7 - 2026-08-04

### Añadido

- Importar tableros (CSV) en Studio (`IDE-0029`): "Archivo → Importar tableros (CSV)…", mismo patrón que la importación de piezas ya existente (`IDE-0018`). Da de alta un lote de tableros de una vez (por ejemplo, varios retales medidos) sin repetir el diálogo "Nuevo tablero" uno a uno. No exige tablero activo — solo proyecto abierto.
- Reparto por mejor ajuste entre tableros (`IDE-0030`): "Herramientas → Repartir piezas entre tableros (mejor ajuste)" (`Ctrl+Alt+M`). A diferencia del reparto de sobrantes existente (que solo probaba tableros completamente vacíos, en el orden de la lista), considera todos los tableros del proyecto — incluidos los parcialmente usados — y prueba primero el más pequeño que sea suficiente para cada pieza, para aprovechar de verdad los retales antes que un tablero grande.
- Cajón sin rieles en el generador de contenedores (`IDE-0031`): nuevo tipo en el desplegable "Tipo de contenedor" del generador (`IDE-0028`). Sus dimensiones exteriores no se dan directas: se calculan a partir del hueco del mueble (ancho/alto) menos una holgura por lado, para que el cajón deslice madera-madera sin rieles metálicos. `studio/containers/drawer.py::build_drawer_no_rails_pieces()`, mismo cuerpo físico que la caja simple (base + 4 paredes a tope).

---

## 0.3.6 - 2026-08-03

### Cambiado

- El asset de macOS pasa de `.zip` a `.dmg` (`package-studio.yml`): la release ya no solo comprime el `.app`, sino que genera un volumen de instalación con un acceso directo a `Aplicaciones` (patrón estándar de arrastrar-para-instalar en macOS). `docs/INSTALL-macos.md`/`README.md` actualizados.

---

## 0.3.5 - 2026-08-03

### Añadido

- Generador de piezas de contenedor desde un retal (`IDE-0028`): "Herramientas → Generar piezas de contenedor…" abre un diálogo con las medidas exteriores (largo/ancho/alto), grosor y material, y añade a la placa activa las piezas de una caja simple (base + 4 paredes, unión a tope, sin divisores) — mismo patrón de vista previa y comandos deshacibles que la importación CSV (`IDE-0024`/`IDE-0018`). `studio/containers/simple_box.py` expone `CONTAINER_TEMPLATES`, un registro pensado para más tipos de contenedor (cajón, cajonera, estantería) y otras uniones/divisores más adelante, sin tocar el diálogo ni `MainWindow` al añadirlos.

---

## 0.3.4 - 2026-08-02

### Añadido

- Exportar DXF y JSON desde Studio (`IDE-0022`): menú "Exportar" gana dos opciones nuevas junto a SVG/PDF. DXF reutiliza `boardcomposer.export.solution_to_dxf()` del Core (`IDE-0012`), sin código nuevo de exportación. JSON es un formato propio del layout actual de Studio (piezas colocadas, dimensiones totales, posición/rotación por pieza) — no el mismo formato que usa el CLI/API para varias soluciones candidatas.
- Comparador de soluciones: miniatura por candidata, marcar una como favorita (⭐), y dos métricas nuevas — fragmentación del material y nº de cortes aproximado (`IDE-0023`). `comparator_panel.py` ya avisaba explícitamente de que estas dos métricas no se calculaban para no inventar números; ahora se calculan con geometría real (`src/boardcomposer/solver/layout_metrics.py`), con el nº de cortes etiquetado como aproximación (asume corte guillotina, mismo supuesto que el kerf).
- Vista previa antes de confirmar un import CSV (`IDE-0024`): `CsvImportPreviewDialog` muestra la tabla de piezas parseadas (id/dimensiones/material/grosor) con OK/Cancelar, antes de comitear nada al proyecto. La validación todo-o-nada de `load_pieces_from_csv()` no cambia — solo se añade la confirmación explícita.
- Diálogo "Preferencias" (`Editar → Preferencias…`, `Ctrl+,`, `IDE-0025`), sustituyendo al submenú "Ver → Tema": el tema (único ajuste global real hoy) ahora persiste entre reinicios vía `QSettings`, antes se perdía cada vez. Sin idioma ni unidades — ninguno tiene infraestructura real detrás todavía.
- Eventos de actividad con categoría y filtro en el Timeline (`IDE-0026`): el evento único `"studio.activity"` del bus (`ADR-003`) gana un campo `category`, con 6 valores reales (`proyecto`, `tablero`, `pieza`, `deshacer`, `layout`, `import`) en vez de los 9 eventos con nombre aspiracionales que nunca se construyeron. La pestaña "Actividad" del Timeline gana un desplegable para filtrar por categoría.
- IDs legibles de solución (`IDE-0027`): `AssemblySolution` gana `solution_id`, un hash corto y determinista de sus colocaciones — dos soluciones con las mismas piezas en las mismas posiciones comparten id aunque el solver las genere en orden distinto. El Comparador y los mensajes de "aplicar solución"/"marcar favorita" ya no se refieren a cada candidata por su posición en la lista (`Solución 1`, `Solución 2`...), que cambiaba de significado cada vez que se regeneraba la comparación — ahora usan una etiqueta de sesión (A/B/C/D) más el id corto persistente junto a ella.

---

## 0.3.3 - 2026-08-01

### Añadido

- Claves de API por cliente con cuota mensual (`IDE-0020`, `src/boardcomposer/billing.py`): primer paso técnico del modelo de producto híbrido decidido con el usuario — Studio gratis, API de pago. Planes `free` (20 solves/mes, 0€), `basico` (300/mes, 9€/mes, overage 0,05€/solve) y `pro` (1500/mes, 29€/mes, overage 0,03€/solve), con registro de claves en SQLite (hasheadas SHA-256) y contador de cuota mensual pluggable (memoria en dev/test, Redis en producción — comparte el mismo problema de estado no compartido entre workers de `gunicorn` que ya tenía el rate limiter, y lo resuelve igual). La clave única legacy (`BOARDCOMPOSER_API_KEY`) sigue funcionando sin cambios, ahora como acceso admin sin medir. `scripts/manage_keys.py` para emitir/revocar/listar claves.
- Cobro del overage con Stripe (`IDE-0021`, `src/boardcomposer/stripe_billing.py`): cada request por encima de cuota en un plan de pago reporta una unidad de uso a Stripe (*best-effort* — un fallo de Stripe nunca rompe la petición real del cliente). `manage_keys.py create` da de alta el Customer+Subscription en Stripe automáticamente cuando el plan es de pago. Inactivo por defecto (mismo patrón que `REDIS_URL`): sin `STRIPE_SECRET_KEY`/`STRIPE_PRICE_BASICO`/`STRIPE_PRICE_PRO`, nada cambia.

### Corregido

- Primera build de macOS realmente firmada y notarizada desde que existe la infraestructura (`v0.3.1`, `DEC-0017`) — nunca se había podido probar contra un certificado real hasta activar la cuenta de Apple Developer. Tres fallos reales encontrados y corregidos en `scripts/sign_and_notarize.sh`, ninguno visible sin un certificado de verdad:
  - Datos planos que Nuitka deja sueltos en `Contents/MacOS/` (p.ej. `certifi/cacert.pem`) hacían fallar la firma del bundle completo con `code object is not signed at all` — `codesign` exige que todo lo que hay en esa carpeta sea código real. Se mueven a `Contents/Resources/` (la convención de Apple) con un symlink relativo en su sitio original, para que el código que los busca por ruta relativa a su propio paquete (`certifi.where()`) los siga encontrando igual en tiempo de ejecución.
  - `notarytool submit --wait` devuelve éxito aunque Apple rechace la build (`status: Invalid`) — el script seguía adelante y fallaba después, al grapar, con un `Record not found` que no explicaba nada. Ahora comprueba el estado explícitamente y, si no es `Accepted`, saca el log detallado de Apple (`notarytool log`) antes de fallar.
  - Varios binarios de Qt sin extensión (`QtCore`, `QtGui`, `QtQml`, `QtQuick`, `QtOpenGL`, `QtQmlModels`...) se saltaban la firma explícita porque el bucle solo buscaba `*.so`/`*.dylib` por nombre — Apple los rechazaba en notarización ("no firmado con un certificado Developer ID válido", "sin *timestamp* seguro"). Se detectan ahora por contenido (Mach-O), no por extensión.

---

## 0.3.2 - 2026-07-30

### Añadido

- El dock "Timeline" mostraba desde su creación el texto literal "Timeline / Consola / Eventos" — ninguna de las tres cosas que nombraba estaba construida (`IDE-0019`). Pasa a `QTabWidget` con dos pestañas, ambas funciones puras (`studio/panels/timeline_panel.py`) pintadas con el mismo `panel_html_stylesheet()` que Inspector/Comparador: **Resumen**, cada tablero con dimensiones, material, nº de piezas, % de uso y qué piezas contiene, con las sin colocar aparte; **Actividad**, un log en vivo alimentado por `ActivityLog` (`studio/activity_log.py`, hasta 200 mensajes), primer uso real del `EventBus` de ADR-003 — instanciado en `StudioServices` desde el principio sin que nada llamara nunca a `publish()`/`subscribe()`. `MainWindow` se suscribe al mismo evento y se redibuja sola cuando algo publica, en vez de un par fijo publish+setHtml: cualquier código con `services` puede loguear actividad sin necesitar una referencia a `MainWindow`, incluido el arrastre de piezas en el lienzo (`BoardWorkspace._finish_piece_drag()`), que antes se saltaba el log por completo. Queda registrado: añadir/editar/eliminar/rotar tablero o pieza, mover a otro tablero, cambiar el kerf, deshacer/rehacer, resolver/aplicar layout, comparar soluciones, importar CSV, proyecto nuevo/abrir/guardar.

### Corregido

- 6 de 9 clases de comando (`AddBoardCommand`, `EditBoardCommand`, `AddPieceCommand`, `EditPieceCommand`, `RotatePieceCommand`, `DeletePieceCommand`) heredaban del Protocol `Command` —que declara `name: str`— sin definirlo nunca: un `AttributeError` dormido desde que existen, nunca disparado porque nada había leído `.name` hasta que el log de actividad lo necesitó. Añadido un `name` de instancia a las 6, y traducidas a español dinámico las 3 que ya lo tenían (estático, en inglés — "Move piece"), ya que ahora es la primera vez que se muestra al usuario.
- `MainWindow._undo()`/`_redo()` llegaban a `self.services.commands.redo_stack[-1]`/`undo_stack[-1]` para saber qué comando se acababa de deshacer/rehacer — tres niveles dentro de la representación interna de `CommandManager`. `CommandManager.undo()`/`redo()` devuelven ahora el comando (antes `None`), así que `MainWindow` no necesita saber que las pilas existen.
- El cálculo de utilización (área usada / área del tablero) estaba duplicado casi literal entre `inspector_panel.render_board()` y el nuevo `timeline_panel.render_overview()`. Extraído a `studio/panels/board_metrics.py::board_utilization()`, usado por ambos.

---

## 0.3.1 - 2026-07-27

### Añadido

- Firma y notarización del `.app` de macOS, condicionadas a que existan las credenciales (`DEC-0017`, mitiga `DT-0011`). `scripts/sign_and_notarize.sh` firma *inside-out* —cada `.dylib`/`.so` primero y el bundle al final, porque la firma exterior sella los hashes de lo que hay dentro— con hardened runtime y *timestamp*, notariza con `notarytool --wait` y grapa el ticket con `stapler`, de modo que el `.app` descargado abre sin avisos incluso sin conexión. Sin `--deep`, que Apple desaconseja para firmar, y sin entitlements: la aplicación dibuja ventanas y hace HTTPS saliente, y ninguna de las dos cosas necesita uno fuera del App Sandbox. `package-studio.yml` detecta los secrets (`MACOS_CERTIFICATE_P12`, `MACOS_CERTIFICATE_PASSWORD`, `MACOS_SIGNING_IDENTITY`, `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD`): si están, firma; si no, publica la build sin firmar. Contratar la cuenta de Apple Developer pasa a ser añadir secrets, sin tocar código. **Descartado firmar con un certificado autofirmado**: Gatekeeper solo confía en los emitidos por Apple, así que dejaría exactamente el mismo aviso al descargar y solo aparentaría estar resuelto.
- `docs/INSTALL-macos.md`, publicado como segundo asset de cada release sin firmar: el `xattr -dr com.apple.quarantine` que hace falta para abrir la aplicación, la alternativa sin Terminal (clic derecho → Abrir), y la explicación de por qué una build compilada en local sí se abre sin avisos — nunca llevó el atributo de cuarentena que añade el navegador al descargar.

### Corregido

- El bundle identifier del `.app` era `app`: Nuitka lo derivaba del nombre del fichero de entrada (`app.py`) porque nadie había fijado `--macos-signed-app-name`. No identifica a nada, lo comparte cualquier otra aplicación empaquetada con el mismo descuido, y la notarización lo habría rechazado. Ahora es `com.efjdefrutos.boardcomposer.studio`, y no debe volver a cambiar: macOS indexa ajustes y permisos por esa cadena. Añadido también `--macos-app-version`, cuya coherencia con `pyproject.toml` comprueba `scripts/check_project.py` en cada `make check` — viven en ficheros distintos y se desincronizan solas.

- El ancho de sierra (kerf) solo lo aplicaba el arrastre interactivo: el solver y el encaje fuera del lienzo lo ignoraban, así que "Generar" producía disposiciones con las piezas pegadas y el plano exportado no se podía cortar (`DT-0020`). Ahora `LayoutService.to_core_project()` entrega al solver cada pieza ensanchada un corte a la derecha y otro abajo, **y el tablero también**: lo segundo cancela lo primero, de forma que N piezas en fila exigen los N-1 cortes que realmente hacen falta y no N. Sin agrandar el tablero, una pieza del ancho completo del tablero —el caso más común, cortes transversales— dejaba de caber, porque reservaba un corte contra el borde del propio tablero donde no hay nada que cortar. `piece_fits_on_board()` y `find_free_position()` (`studio/workspace/placement_fit.py`) aceptan ahora `kerf_mm`: los límites del tablero se comprueban contra la pieza real y el solape contra la pieza y su vecina, ambas ensanchadas —ensanchar solo la candidata no veía a la vecina de la izquierda, cuyo corte es el que se invadía—, con lo que la separación exigida es exactamente un corte en cualquier dirección, nunca dos. El kerf no llega al plano exportado: `studio_project_to_solution()` sigue dibujando las dimensiones reales, porque la holgura es espacio reservado en el tablero, no parte de la pieza. El Core no sabe qué es un kerf y sigue sin saberlo (`DEC-0016`): con `kerf_mm` a 0 —el valor por defecto— nada cambia respecto a `v0.3.0`.

---

## 0.3.0 - 2026-07-26

### Añadido

- Reapertura del último proyecto al arrancar Studio: `_save_project()`/`_open_project()` recuerdan la ruta del fichero vía `QSettings` (por usuario, persistente entre lanzamientos) y `MainWindow` la carga al arrancar. Hasta ahora Studio siempre abría el proyecto demo, incluso justo después de guardar y cerrar. Cae al proyecto demo solo si no hay ruta recordada, o si el fichero desapareció o está corrupto — nunca falla al arrancar por ello. Los tests aíslan `QSettings` en un directorio temporal por test (`tests/conftest.py`), para no leer los ajustes reales de la máquina de desarrollo.
- Etiqueta del tablero en el lienzo: `create_board_item()` añade el `board_id` como texto sobre el rectángulo del tablero (fuera de sus propios límites, para no solaparse con una pieza colocada cerca del origen). Antes las piezas se etiquetaban a sí mismas pero el tablero no — la única forma de saber qué tablero se estaba mirando era el Explorer o el Inspector.
- Recolocación automática al rotar o mover una pieza a otro tablero: `find_free_position()` (`studio/workspace/placement_fit.py`) busca el primer hueco libre (heurística por esquinas: origen del tablero más el borde derecho/inferior de cada colocación existente) cuando la pieza no cabe en su posición actual. `RotatePieceCommand`/`MoveToBoardCommand` aceptan las coordenadas nuevas para que la recolocación viaje con la rotación/cambio de tablero como un único paso deshacible. Solo se rechaza cuando no cabe en ninguna parte del tablero. No es empaquetado completo — resolver una disposición entera sigue siendo trabajo del solver.
- Cobertura de tests del Asistente: `dropEvent`, la tecla Intro del teclado numérico y el filtrado de URLs no locales en `PromptTextEdit`; y el lado de `MainWindow` del adjunto (el chip aparece/desaparece, de varios ficheros soltados solo se queda el primero, un fichero de texto legible se incrusta en la pregunta y uno binario se marca como no legible).

### Corregido

- Números no finitos aceptados en todas las rutas de entrada externa: `json.loads()` interpreta `"NaN"`/`"Infinity"` como flotantes y toda comparación contra `NaN` es falsa, así que las guardas `< 0`/`<= 0` los dejaban pasar hasta el solver, la puntuación o la exportación. Ahora exigen `math.isfinite()`: `Board`, `ProjectConstraints`, `BoardPlacement`, `SolutionScore` y sus componentes, los pesos que devuelve la IA en `suggest_strategy()`, el importador CSV de Studio (`csv_import.py`, con el valor infractor en el mensaje y la promesa de todo-o-nada intacta) y los modelos `StudioBoard`/`StudioPiece` (que no tenían ninguna validación, así que un `.bcstudio.json` podía sembrar un tablero de -500 mm). `StudioPlacement` solo comprueba finitud, no signo: una coordenada negativa es un estado transitorio legítimo mientras se arrastra una pieza fuera del tablero. `/solve`, `/assist/strategy` y `/assist/explain` responden `400` con mensaje en vez de `500`.
- Colocaciones colgantes al cargar un proyecto: `project_from_dict()` aceptaba colocaciones que apuntaban a piezas o tableros ausentes del fichero — la carga "tenía éxito" y solo fallaba después, sin protección, al renderizar el workspace. Ahora se descartan en vez de rechazar el fichero entero (un proyecto dañado sigue siendo recuperable) y cada descarte se informa por el nuevo callback opcional `on_warning`, que `MainWindow` muestra en un diálogo — el siguiente guardado escribirá el proyecto sin ellas.
- Deshacer tras cambiar de proyecto aplicaba un comando obsoleto al proyecto nuevo: los comandos resuelven ahora el proyecto actual en el momento de deshacer en vez de guardar una referencia, y `CommandManager.clear()` se llama en cada transición de proyecto.
- Ficheros de entrada malformados volcaban un traceback de Python desde la CLI (`ValueError` de `float()`, `KeyError` por una columna ausente, `FileNotFoundError`), sin indicar qué fila fallaba — el importador de Studio ya lo hacía bien, los cargadores del Core no. Ambos comprueban ahora las columnas obligatorias por adelantado y envuelven cada fila, lanzando `LoaderError` con el número de línea (la cabecera es la fila 1, así que los números coinciden con lo que el usuario ve en su editor). `LoaderError` hereda de `ValueError`, así que quien ya capturaba `ValueError` sigue funcionando. El cargador de Excel cubre además la hoja vacía (`StopIteration` escapándose de un generador) y la fila con un número de celdas distinto al de la cabecera (`zip(strict=True)`). La CLI los convierte, junto a `OSError`, en un mensaje de una línea y código de salida 1.
- Aplicar una disposición vaciaba el resto de tableros: `_apply_solution()` limpiaba la lista completa de colocaciones antes de escribir la solución. Ahora sustituye solo las del tablero que se está resolviendo.
- Piezas sobrantes descartadas con otros tableros vacíos disponibles: `to_core_project()` empaquetaba todas las piezas del proyecto sin mirar dónde estaban ya colocadas (resolver el tablero B podía reempaquetar una pieza ya puesta en el A, dejando dos colocaciones para la misma pieza), y aplicar una disposición solo resolvía el tablero activo. Ahora se excluyen del candidato las piezas ya colocadas en otro tablero, y `apply_last_solution_to_current_project()`/`apply_comparison_solution()` prueban después los demás tableros del proyecto — solo los que están completamente vacíos, para no rebarajar uno que alguien ya había ordenado.
- Piezas empaquetadas en tableros de otro grosor: ni la resolución del tablero activo ni la distribución de sobrantes comprobaban `thickness_mm`. `to_core_project()` excluye ahora cualquier pieza cuyo grosor no coincida con el del tablero que se resuelve; una pieza sin tablero de su grosor queda correctamente sin colocar en vez de forzada donde no corresponde.
- Rotar una pieza a mano exportaba en su orientación original: `RotatePieceCommand` solo tocaba `placement.rotation`, mientras que la exportación SVG/PDF (`studio_project_to_solution()`) intercambia largo/ancho según `placement.rotated`, un campo que solo mantenía sincronizado el solver. Ahora se fijan los dos a la vez.
- Mover una pieza a otro tablero sin validar nada: `MoveToBoardCommand` reasignaba el `board_id` sin comprobar grosor, límites del tablero ni solapes — la pieza conserva su x/y y su rotación, así que podía acabar fuera del tablero destino o encima de otra pieza. `PlacementValidator` no lo cubría porque solo corre en el arrastre/rotación interactivos del lienzo. Nuevo `piece_fits_on_board()` (`studio/workspace/placement_fit.py`, sin dependencia de Qt, reutilizando `boardcomposer.geometry.Rectangle.overlaps()`); el diálogo ofrece solo tableros del mismo grosor y cada rechazo tiene su mensaje concreto.
- Editar una pieza o un tablero podía corromper la disposición: `EditPieceCommand`/`EditBoardCommand` sustituían la dataclass sin validar que las colocaciones existentes siguieran encajando. `_edit_piece()` comprueba ahora que las dimensiones/grosor nuevos siguen cabiendo en su tablero sin solapar a un vecino, y `_edit_board()` que todas las piezas ya colocadas siguen encajando (y en grosor) con las dimensiones nuevas.
- El Asistente del Studio remoto respondía siempre "Respuesta simulada del asistente IA" en el VPS: `default_provider()` cae a `MockAIProvider` si falta `ANTHROPIC_API_KEY`, y los ejemplos de `docker run` de `docs/deploy-studio-remote.md` nunca la pasaban ni la mencionaban. Añadida `-e ANTHROPIC_API_KEY` a los tres ejemplos y una entrada de troubleshooting, igual que ya tenía `docs/deploy.md` para la API.

### Documentación

- Referencia de usuario de la línea de comandos (`docs/cli.md`, nueva): opciones, formato de entrada CSV/Excel, salida de texto y JSON, subcomando `plugins`, mensajes de error y códigos de salida. Hasta ahora el uso desde terminal solo estaba cubierto por cuatro líneas del `README.md` y los atajos del `Makefile` — ni `--strategy`, ni `--top`, ni `--allow-rotation`, ni `boardcomposer plugins` aparecían en ningún sitio orientado a quien usa la herramienta.
- `docs/masterplan/INDEX.md` (estaba vacío, 0 bytes): índice de los documentos maestros, ADR, especificaciones de interfaz y documentación técnica, con cuándo consultar cada uno.
- Corregido en `README.md`: el recuento de tests (decía "300+", son 673) y las columnas obligatorias de entrada (`id` no lo es en el CSV/Excel del Core, solo en el importador de piezas de Studio).
- `docs/studio.md` puesto al día tras el trabajo multi-tablero: tabla de comandos completa (faltaban `AddBoardCommand`/`EditBoardCommand`/`AddPieceCommand`/`EditPieceCommand`/`MoveToBoardCommand`/`SetKerfCommand`), secciones nuevas para `placement_fit.py`, reapertura del último proyecto, colocaciones colgantes, ancho de sierra y etiquetas del lienzo, y retiradas dos afirmaciones ya falsas ("Studio solo soporta un tablero activo por proyecto", "el Comparador aún sin construir").
- `DT-0017`–`DT-0019` registran en `docs/masterplan/DOC-006-DeudaTecnica.md` las correcciones posteriores a `v0.2.0`; `DT-0020` registra una limitación no documentada hasta ahora: el ancho de sierra solo lo aplica el arrastre interactivo, no el solver ni la exportación.

### Cambiado

- `ruff` y `pytest` fijados a versión exacta (`ruff==0.15.21`, `pytest==9.1.1`) en el extra `[dev]` de `pyproject.toml`, y CI instala `pip install -e ".[dev]"` en vez de una línea `pip install ruff pytest` aparte y también sin fijar. Ambas resolvían a lo último publicado en PyPI en el momento de instalar, así que CI podía empezar a fallar sin ningún cambio de código: el PR #45 (solo documentación) falló con 29 errores de lint en ficheros que no tocaba.
- `.gitignore` ignora los directorios de configuración de asistentes de código (`.agent/`, `.claude/` salvo `launch.json`, `.codebuddy/`, `.codex/`, `.continue/`, `.cursor/`, `.gemini/`, `.github/prompts/`, `.kiro/`, `.opencode/`, `.qoder/`, `.roo/`, `.trae/`, `.windsurf/`) y el fichero `Icon?` de macOS. Un instalador de skills externo había volcado el mismo paquete con scripts de Python en los 14 directorios a la vez, y `make check` fallaba con 196 errores de `ruff` en código ajeno al proyecto (`ruff` respeta `.gitignore`, así que no hace falta configurar nada más). El código propio nunca tuvo esos errores.

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
