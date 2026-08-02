# BoardComposer — MASTERPLAN

**Última revisión:** 01/08/2026

> Este documento resume el estado del proyecto y las normas de trabajo.
> El detalle vivo de cada funcionalidad está en `DOC-004-Backlog.md`, la
> dirección del producto en `DOC-003-Roadmap.md` y la deuda técnica en
> `DOC-006-DeudaTecnica.md`. Si algo aquí contradice a esos tres, mandan ellos.

## Estado actual

Rama: `main`
Versión publicada: `0.3.3` (01/08/2026, tag `v0.3.3`) — incluye `IDE-0020`
(billing/cuota de API) e `IDE-0021` (cobro de overage con Stripe). Primera
release firmada y notarizada de verdad (`DT-0011`). `IDE-0022` (exportar
DXF/JSON desde Studio), `IDE-0023` (Comparador: miniaturas, favorita,
fragmentación, nº de cortes) e `IDE-0024` (vista previa antes de
confirmar import CSV) quedan por delante del tag, sin publicar todavía.
Tests: 770, en verde.

Fases del Roadmap (`DOC-003-Roadmap.md`):

| Fase | Estado |
|------|--------|
| 1 — Core | 🟢 Completada |
| 2 — BoardComposer Studio | 🟢 Completada |
| 3 — Plataforma (API, servicios remotos, Cloud) | 🟢 Completada |
| 4 — Inteligencia (IA) | 🟢 Completada |
| 5 — Ecosistema | 🟡 En curso |

Backlog (`DOC-004-Backlog.md`): `IDE-0001`–`IDE-0024`, todos 🟢 completados y
en `main`. No hay ningún IDE en desarrollo ni planificado.

Deuda técnica (`DOC-006-DeudaTecnica.md`): 22 registros, los 22 resueltos.
`DT-0011` (el `.app` de macOS sin firmar/notarizar) cerrada del todo el
01/08/2026: cuenta de Apple Developer activada, secrets cargados, `v0.3.3`
es la primera release firmada y notarizada de verdad — tres bugs reales en
`scripts/sign_and_notarize.sh` aparecieron y se corrigieron en el proceso,
solo visibles al firmar contra un certificado real por primera vez. Sigue
sin cubrir Windows/Linux/Intel, fuera de alcance de este ítem.

Despliegue privado en marcha (`IDE-0017`): API en `bc.efjdefrutos.com` y
Studio por navegador (noVNC) en `studio.efjdefrutos.com`. Contenedores
reconstruidos y verificados el 31/07/2026 tras el commit `043caf1`
(rebuild manual por SSH, no automatizado — sin CI/CD de despliegue todavía).

## Trabajo en curso

Ninguno acotado. `IDE-0022` — exportar DXF y JSON desde Studio
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

770 tests en verde.

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

1. Activar Stripe en producción (`IDE-0021` ya construido, inactivo): crear
   los Price de `básico`/`pro` en la cuenta Stripe del usuario (hoy solo
   probada en modo test) y configurar `STRIPE_SECRET_KEY`/
   `STRIPE_PRICE_BASICO`/`STRIPE_PRICE_PRO` en la VPS.
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
