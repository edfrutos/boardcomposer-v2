# BoardComposer — MASTERPLAN

**Última revisión:** 26/08/2026

> Este documento resume el estado del proyecto y las normas de trabajo.
> El detalle vivo de cada funcionalidad está en `DOC-004-Backlog.md`, la
> dirección del producto en `DOC-003-Roadmap.md` y la deuda técnica en
> `DOC-006-DeudaTecnica.md`. Si algo aquí contradice a esos tres, mandan ellos.

## Estado actual

Rama: `main`
Versión publicada: `0.3.40` (26/08/2026, tag `v0.3.40`) — dos arreglos
de facturación encontrados y corregidos *antes* de activar Stripe con
dinero real, ninguno reportado por un cliente (`DT-0038`/`DT-0039`,
ver `Deuda técnica` abajo). Studio sin cambios desde `v0.3.38`
(`DT-0036`/`DT-0037`, etiqueta de tablero + notarización con clave de
App Store Connect). Detalle release a release en `CHANGELOG.md`;
narrativa completa por hilos en `NOTEBOOK.md`. Última verificación
operativa completa: `CHECKLIST-operativa.md` (21/08/2026).

Fases del Roadmap (`DOC-003-Roadmap.md`):

| Fase | Estado |
|------|--------|
| 1 — Core | 🟢 Completada |
| 2 — BoardComposer Studio | 🟢 Completada |
| 3 — Plataforma (API, servicios remotos, Cloud) | 🟢 Completada |
| 4 — Inteligencia (IA) | 🟢 Completada |
| 5 — Ecosistema | 🟡 En curso (biblioteca de materiales e inventario de retales completos; marketplace público y comunidad sin empezar) |

Backlog (`DOC-004-Backlog.md`): `IDE-0001`–`IDE-0045`, todos 🟢
completados y en `main`.

Deuda técnica (`DOC-006-DeudaTecnica.md`): 39 registros, los 39
resueltos. `DT-0038` (25/08/2026): encontrado revisando el diseño de
facturación antes de activar Stripe en real, no reportado por nadie —
`report_overage()` solo reportaba las unidades ya por encima de cuota,
así que un único Price graduado con el corte en la cuota incluida
(300/1500) nunca llegaría a cruzarlo, facturando 0€ de overage en
silencio. Corregido a dos Price por plan (cuota fija recurrente +
overage medido sin tramos) antes de crear nada real en Stripe.
`DT-0039` (26/08/2026): al crear esos Price reales, Stripe exigió un
*Meter* — la cuenta usa el sistema nuevo de Billing Meters, incompatible
con la API antigua (`SubscriptionItem.create_usage_record`) que usaba
el código. `report_overage()` pasa a reportar por `stripe_customer_id`
+ un `event_name` fijo (`billing.MeterEvent.create`), confirmado contra
la documentación oficial de Stripe antes de tocar código. `DT-0029`
(relanzado tras la auto-sustitución del `.app`,
`IDE-0045`) confirmado del todo el 24/08/2026: ciclo completo
`v0.3.35`→`v0.3.38` probado en real por el usuario — descarga,
sustitución en marcha y relanzado sin intervención manual. `DT-0011`
(el `.app` de macOS sin firmar/notarizar) cerrada del todo el
01/08/2026; sigue sin cubrir Windows/Linux/Intel, fuera de alcance de
este ítem. `DT-0034`/`DT-0035` (23/08/2026): tanto la API (`v0.3.9`, 27 versiones
de desfase) como Studio por navegador (`studio.efjdefrutos.com`,
noVNC, igual de desfasado — le faltaban `IDE-0039`/`IDE-0041`)
llevaban meses sin reconstruirse en la VPS. Ambos reconstruidos y
confirmados en `v0.3.36`; `docs/deploy.md` gana el paso de `chown` que
causó el fallo de la API. `DT-0036` (23/08/2026): etiqueta de tablero
delgado desbordando su rectángulo, mismo tipo de bug que ya se había
corregido una vez para las piezas — resuelto en `v0.3.37`. `DT-0037`
(23-24/08/2026): la contraseña de aplicación del Apple ID usada para
notarizar se revocó sin aviso; migrado a una clave de App Store
Connect, scoped solo a notarización — cinco vueltas de depuración
contra el pipeline real hasta confirmarlo en `v0.3.38`. Ninguno de los
dos despliegues de la VPS tiene CI/CD propio — sigue dependiendo de
que alguien se acuerde de reconstruir los dos contenedores, no
automatizado.

Runners de CI/CD: ambos workflows (`ci.yml`, `package-studio.yml`)
migrados de runners alojados por GitHub a un runner autoalojado en el
Mac del usuario (`v0.3.30`–`v0.3.35`, `DT-0030`–`DT-0033`), tras
agotarse el límite de gasto de Actions en el repo privado — cinco
intentos seguidos hasta que el pipeline de firma llegó a completarse de
verdad. Concurrencia (`cancel-in-progress`) añadida a `package-studio.yml`
para evitar la build duplicada al empujar rama+tag juntos, pendiente de
confirmar contra el push que produjo `v0.3.36`.

Despliegue privado en marcha (`IDE-0017`): API en `bc.efjdefrutos.com` y
Studio por navegador (noVNC) en `studio.efjdefrutos.com` — dos
contenedores independientes, cada uno con su propio ciclo de
reconstrucción manual. Ambos reconstruidos y verificados el 23/08/2026
(`DT-0034`/`DT-0035`): la API corría `v0.3.9` desde el 31/07/2026
(commit `043caf1`), Studio remoto igual de desfasado (le faltaban
`IDE-0039`/`IDE-0041` en el menú "Proyecto") — los dos confirmados en
`v0.3.36`, con paridad completa entre la web y la app local. `docs/deploy.md`
gana el paso de `chown` del volumen que causó el fallo de la API; el de
Studio remoto no lo necesitó. Ningún CI/CD de despliegue todavía —
sigue dependiendo de que alguien reconstruya los dos contenedores a
mano.

Credenciales rotadas el 23/08/2026, mismo día: `BOARDCOMPOSER_API_KEY`,
la contraseña de `auth_basic` de nginx (`bc-studio`), `VNC_PASSWORD`
(ya no coincide con `BOARDCOMPOSER_API_KEY` — antes reutilizaba el
mismo valor) y `ANTHROPIC_API_KEY` (clave vieja revocada en la consola
de Anthropic, nueva en uso) — las cuatro se habían compartido en texto
plano durante el diagnóstico de `DT-0034`/`DT-0035`. Confirmado por el
usuario contra los contenedores reales tras recrearlos.

## Trabajo en curso

Ninguno abierto en desarrollo activo. Pendiente real hoy, de
`CHECKLIST-operativa.md` (24/08/2026):

- Activar Stripe en producción (`IDE-0021`, ya construido, inactivo sin
  `STRIPE_SECRET_KEY`/`STRIPE_PRICE_*`).
- Al menos una clave real de Gemini/Ollama probada en producción (hoy
  solo Anthropic y OpenAI verificados con credenciales reales,
  `IDE-0036`).
- Considerar automatizar (o al menos dar un guardarraíl tipo
  `scripts/check_project.py`) la reconstrucción de ambos contenedores
  de la VPS — es la segunda vez en la vida del proyecto que se
  descubren meses de desfase solo al pedir explícitamente comprobarlo.

## Historial hasta el 08/08/2026

Las siguientes entradas documentan el trabajo hasta `v0.3.15`
(08/08/2026), última vez que esta sección se mantuvo al día
release a release. A partir de ahí, el detalle vivo pasó a
`NOTEBOOK.md`/`CHANGELOG.md` (narrativa) y `DOC-004-Backlog.md`
(`IDE-0032`–`IDE-0045`) — no duplicado aquí para no repetir la misma
brecha de mantenimiento que motivó esta revisión (22/08/2026).

Últimas tres piezas pedidas juntas el 04/08/2026
(`IDE-0029`/`IDE-0030`/`IDE-0031`), las tres 🟢 completadas y en `main`.

- `IDE-0029` — importar tableros (CSV) en Studio: mismo patrón que la
  importación de piezas (`IDE-0018`),
  `studio/project/board_csv_import.py::load_boards_from_csv()` +
  `BoardCsvImportPreviewDialog` + acción "Archivo → Importar tableros
  (CSV)…".
- `IDE-0030` — reparto por mejor ajuste entre tableros: el usuario reportó
  que el aprovechamiento de retales "no veo que funcione" —
  `_fill_other_empty_boards_with_leftovers()` (`IDE-0019`) solo probaba
  tableros completamente vacíos, en el orden de la lista, sin priorizar
  el más ajustado. `LayoutService.apply_best_fit_distribution()` ordena
  todos los tableros por área ascendente (incluidos los parcialmente
  usados) y prueba el más pequeño suficiente primero — heurística voraz,
  no óptimo global. Acción nueva "Herramientas → Repartir piezas entre
  tableros (mejor ajuste)" (`Ctrl+Alt+M`), no sustituye al flujo
  tablero-por-tablero existente.
- `IDE-0031` — cajón sin rieles en el generador de contenedores: acotado
  con el usuario ("holgura por hueco de mueble"). Dimensiones exteriores
  no se dan directas, se derivan del hueco del mueble (ancho/alto) menos
  la holgura por lado necesaria para deslizar madera-madera sin rieles
  metálicos — `studio/containers/drawer.py::build_drawer_no_rails_pieces()`
  delega en `build_simple_box_pieces()` (`IDE-0028`) para la lista de
  piezas. `CONTAINER_TEMPLATES` pasa a vivir en
  `studio/containers/__init__.py` como registro combinado de ambos
  templates; `ContainerGeneratorDialog` alterna las filas del formulario
  según el tipo elegido.

873 tests en verde. Las tres dadas de alta en el Backlog antes de
construirse.

Publicada `v0.3.5` (03/08/2026): `IDE-0028` — generador de piezas de
contenedor desde un retal. Candidata 2 de aprovechamiento de retales
(`DOC-999-Ideas.md`), acotada con el usuario: caja simple (base + 4
paredes, unión a tope, sin divisores), como diálogo en Studio, no plugin.
`studio/containers/simple_box.py` (`CONTAINER_TEMPLATES`, registro nombre
→ función) + `studio/dialogs/container_generator_dialog.py` + acción
nueva "Herramientas → Generar piezas de contenedor…" en `MainWindow`,
reutilizando `CsvImportPreviewDialog` (`IDE-0024`) para la confirmación y
`AddPieceCommand` para el alta deshacible pieza a pieza, mismo patrón que
`IDE-0018`. `joint`/`dividers` ya son parámetros de
`build_simple_box_pieces()` (solo `"a_tope"`/`0` soportados) para que un
cajón, una unión rebajada o divisores sean una entrada nueva en el registro,
no un sitio de llamada nuevo. Verificado con tests nuevos
(`tests/test_simple_box.py`, `tests/test_main_window_container_generator.py`)
y con la app real (acción confirmada en el menú, `.app` local recompilado
y arrancado). 813 tests en verde. Dado de alta en el Backlog antes de
construirse.

Publicada `v0.3.4` (02/08/2026): los seis puntos de la lista de gaps de
Studio que destapó la auditoría de documentación del 01/08/2026, en el
orden acordado con el usuario.

`IDE-0022` — exportar DXF y JSON desde Studio
(`studio/export/dxf_export.py`/`json_export.py`, dos entradas nuevas en el
menú "Exportar"), primer punto de la lista de gaps de Studio que destapó la
auditoría de documentación del 01/08/2026 (`SCR-007-Exportación.md`). DXF
reutiliza `solution_to_dxf()` del Core (`IDE-0012`) sin código nuevo; JSON
es un formato propio del layout manual de Studio, no el de varias
candidatas que usa el CLI/API. Verificado con la app real corriendo:
las 4 opciones del menú "Exportar" confirmadas, clic en DXF sin error.
Dado de alta en el Backlog antes de construirse.

`IDE-0023` — segundo punto de la misma lista de gaps (`SCR-003-Comparador.md`):
miniatura por candidata (`studio/export/thumbnail.py`, `QPainter` →
`data:image/png;base64,...` embebido en el HTML), marcar una como favorita
(⭐, `MainWindow._mark_favorite_solution()`), y dos métricas que
`comparator_panel.py` documentaba explícitamente como no calculadas para
no inventar números — fragmentación (descomposición del hueco libre en
rectángulos disjuntos) y nº de cortes (aproximación etiquetada como tal,
asume corte guillotina como ya hace el kerf, `DEC-0016`), ambas en
`src/boardcomposer/solver/layout_metrics.py`, verificadas a mano con
geometría conocida. Verificación visual en vivo no concluyente esta vez
(automatización de Accessibility inestable en la sesión, no del código) —
se apoya en tests, incluida la generación real de `QPixmap`/`QPainter`.
Dado de alta en el Backlog antes de construirse.

`IDE-0024` — tercer punto de la misma lista de gaps (`FLW-002-Importar-CSV.md`):
vista previa antes de confirmar un import CSV, `studio/dialogs/csv_import_preview_dialog.py`
(tabla id/dimensiones/material/grosor, OK/Cancelar) interpuesto entre el
parseo de `load_pieces_from_csv()` —validación todo-o-nada sin cambios— y
la comisión de piezas al proyecto. Dado de alta en el Backlog antes de
construirse.

`IDE-0025` — quinto y último punto de la lista de gaps que destapó la
auditoría (`SCR-006-Preferencias.md`): diálogo "Preferencias"
(`Editar → Preferencias…`, `Ctrl+,`, `QAction.MenuRole.PreferencesRole`
para que macOS lo mueva solo al menú de la app), sustituyendo al submenú
"Ver → Tema". Alcance acotado explícitamente con el usuario antes de
construir: solo tema (único ajuste global real hoy), ahora persistido en
`QSettings` — antes se perdía en cada reinicio. Sin idioma/unidades: no
hay i18n ni conversión de unidades en el dominio, un control ahí no
haría nada. Dado de alta en el Backlog antes de construirse. De paso,
arreglado un fallo real mío en `DOC-004-Backlog.md`: una edición anterior
en esta misma sesión se había comido la cabecera "## Reglas de
mantenimiento".

`IDE-0026` — sexto y último punto de la lista de gaps que destapó la
auditoría (`ADR-003-Event-Bus.md`, `ADR-005-Timeline.md`): el evento único
`"studio.activity"` del bus gana un campo `category` (`proyecto`,
`tablero`, `pieza`, `deshacer`, `layout`, `import`,
`studio/activity_log.py::CATEGORIES`) en vez de los 9 eventos con nombre
aspiracionales que boceta `ADR-003` — acotado explícitamente con el usuario
por no encajar con la granularidad real del código. Cada clase `Command`
declara su `.category` igual que ya declaraba `.name`; la pestaña Actividad
del Timeline gana un `QComboBox` para filtrar por categoría. Dado de alta
en el Backlog antes de construirse.

`IDE-0027` — sexto punto de la lista de gaps, el aplazado en la
priorización original: `AssemblySolution.solution_id`
(`src/boardcomposer/domain/solution.py`) es una propiedad calculada, hash
corto y determinista de las colocaciones — no un campo del constructor,
para no tocar los ~12 sitios de `solver` que construyen `AssemblySolution`
directamente. Acotado con el usuario entre tres alcances posibles
("etiqueta de sesión", "id persistente" o "ambas"): eligió ambas.
`studio/solution_labels.py::solution_label(index)` da la etiqueta A/B/C/D
para la UI; el Comparador y los mensajes de aplicar/marcar favorita
sustituyen el antiguo `Solución {índice + 1}` (que cambiaba de
significado en cada comparación nueva) por la etiqueta más el id corto
persistente entre paréntesis. Dado de alta en el Backlog antes de
construirse.

784 tests en verde.

Publicada `v0.3.3` (01/08/2026): `IDE-0020` + `IDE-0021` — claves de API
por cliente con cuota mensual y cobro del overage con Stripe, primer y
segundo paso técnico de la decisión de producto resuelta el 31/07/2026:
Studio gratis + API de pago (modelo híbrido). Planes cerrados con el
usuario: `free` (20 solves/mes, 0 €), `basico` (300/mes, 9 €/mes, overage
0,05 €/solve), `pro` (1500/mes, 29 €/mes, overage 0,03 €/solve).

`IDE-0020`: `src/boardcomposer/billing.py` (registro de claves en SQLite,
contador de cuota mensual pluggable — memoria en dev/test, Redis en
producción) más `scripts/manage_keys.py` (CLI admin) y
`_authenticate_and_meter()` en `api.py`, que sustituye a `_require_api_key()`
manteniendo la clave única legacy como acceso admin sin medir. Repite el
mismo incumplimiento de proceso que `IDE-0019`: construido y comiteado
(`043caf1`) antes de darlo de alta aquí — registrado también como
`DT-0022`.

`IDE-0021`: `src/boardcomposer/stripe_billing.py` — al superar la cuota en
un plan de pago, cada request reporta 1 unidad de overage a Stripe
(`SubscriptionItem.create_usage_record`, best-effort, nunca rompe la
petición del cliente si Stripe falla). `manage_keys.py create` da de alta
el Customer+Subscription en Stripe automáticamente cuando el plan es de
pago. Este sí se dio de alta en el Backlog *antes* de construirse, sin
generar una `DT` nueva. Inactivo por defecto (mismo patrón que
`REDIS_URL`): sin `STRIPE_SECRET_KEY`/`STRIPE_PRICE_BASICO`/
`STRIPE_PRICE_PRO`, nada cambia — el usuario tiene cuenta Stripe de
pruebas pendiente de pasar a producción, sin Price IDs creados todavía.

Billing verificado en producción el 31/07/2026 (sin Stripe activo aún):
rebuild de la VPS con `IDE-0020`, volumen persistente para `keys.db` (con
fallo de permisos real detectado y corregido — UID del contenedor vs.
propietario del volumen), clave admin generada y probada desde dos
dispositivos distintos (bloqueada primero por `auth_basic` de nginx,
delante de la API, sin relación con este cambio).

Primera build de macOS realmente firmada y notarizada (`DT-0011`,
`DEC-0017`): la infraestructura existía desde `v0.3.1` pero nunca se había
probado contra un certificado real hasta activar la cuenta de Apple
Developer el 01/08/2026. Tres bugs reales en `scripts/sign_and_notarize.sh`
solo visibles con un certificado de verdad — datos de Nuitka sueltos en
`Contents/MacOS/` (movidos a `Contents/Resources/` con symlink relativo),
`notarytool submit --wait` que no comprobaba el estado real de Apple
(ahora saca el log si rechaza), binarios de Qt sin extensión que se
saltaban la firma explícita (detectados ahora por contenido Mach-O, no por
`*.so`/`*.dylib`). Verificado con la propia release: el asset publicado no
lleva `docs/INSTALL-macos.md` acompañándolo, señal de que tomó la rama
firmada.

748 tests en verde.

Publicada `v0.3.2` (30/07/2026): incluye `IDE-0019` — el dock "Timeline"
mostraba desde su creación el texto literal "Timeline / Consola / Eventos";
pasa a tener Resumen (tableros con piezas y % de uso) y Actividad (log en
vivo, primer uso real del `EventBus` de ADR-003, hasta entonces construido
y sin conectar). Por el camino: 6 de 9 clases de comando no definían
`.name` pese a que el Protocol lo exige (`AttributeError` dormido, nunca
disparado hasta que el log lo necesitó). Registrado como `IDE-0019`
*después* de construirse, incumpliendo la norma 1 de este documento —
también como `DT-0021`.

Publicada `v0.3.1` (28/07/2026): republica el `.app` de macOS con el
bundle identifier corregido y el ancho de sierra aplicado por el solver
(`DT-0020`, `DEC-0016` — el kerf se traduce en Studio, el Core sigue sin
saber qué es), ninguno de los dos a tiempo para `v0.3.0`. Incluye también
la corrección de que marcar una pieza en el Explorer no cambiaba al
tablero donde estaba, y el arreglo de que el tema oscuro elegido a mano no
llegaba a los paneles de contenido (Inspector/Comparador/Asistente) — los
tres con estados vacíos reales en vez de texto plano sin tratamiento.

Sigue completa la revisión de documentación del 26/07/2026: índice del
masterplan (`INDEX.md`, hasta entonces vacío), referencia de usuario de la
línea de comandos (`docs/cli.md`, nueva).

## Próxima decisión

Dirección de producto resuelta el 31/07/2026: modelo híbrido — Studio
gratis (sin cambios, ya empaquetado), API de pago por request
(`IDE-0020`). Descartadas por ahora: instancia demo pública, marketplace de
plugins y SaaS completo con cuentas propias (`DOC-999-Ideas.md`) — quedan
como candidatas futuras si el modelo híbrido no basta.

Pendiente, de menor a mayor alcance:

1. Activar Stripe en producción (`IDE-0021` ya construido, inactivo;
   `DT-0038` corregido antes de tocar dinero real — dos Price por plan,
   no uno, ver `DOC-006-DeudaTecnica.md`): crear en la cuenta Stripe del
   usuario (ya en modo live) **dos** Price por plan — uno recurrente
   normal para la cuota fija (`básico` 9€/mes, `pro` 29€/mes) y uno
   medido sin tramos para el overage (`básico` 0,05€/unidad, `pro`
   0,03€/unidad) — y configurar `STRIPE_SECRET_KEY`/`STRIPE_PRICE_BASICO`/
   `STRIPE_PRICE_BASICO_OVERAGE`/`STRIPE_PRICE_PRO`/
   `STRIPE_PRICE_PRO_OVERAGE` en la VPS.
2. Alta de cliente self-service (hoy `scripts/manage_keys.py` es manual,
   sin landing ni registro automático).
3. Automatizar el rebuild/despliegue del VPS (hoy manual por SSH, ver
   `Estado actual`) si la cadencia de cambios en la API lo justifica.

Si el kerf tiene que importar también fuera de Studio (CLI y API hoy no lo
tienen), `DEC-0016` es la decisión a revisitar.

Formalmente sigue pendiente el andamiaje de proceso que declaran `DOC-003`,
`DOC-004` y `DOC-006` en su estado 🟡 "En revisión": descomponer las fases en
épicas (EP), enlazar Roadmap y Backlog, y definir el flujo
Idea → Épica → Sprint → Implementación → Liberación. Con el backlog vacío no
bloquea nada hoy.

## Normas de trabajo

1. No añadir funcionalidad sin bloque definido.
2. No lógica geométrica en MainWindow.
3. No reglas de colocación fuera de PlacementValidator.
4. No comandos dependientes de Qt.
5. Ruff limpio antes de cada commit.
6. Commit al cerrar cada bloque.
7. Antes de cada commit:
   - ejecutar `ruff check`;
   - ejecutar `ruff check --fix`;
   - volver a ejecutar `ruff check`;
   - ejecutar la aplicación;
   - comprobar manualmente la funcionalidad afectada;
   - revisar `git status`.
