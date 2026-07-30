# BoardComposer — MASTERPLAN

**Última revisión:** 30/07/2026

> Este documento resume el estado del proyecto y las normas de trabajo.
> El detalle vivo de cada funcionalidad está en `DOC-004-Backlog.md`, la
> dirección del producto en `DOC-003-Roadmap.md` y la deuda técnica en
> `DOC-006-DeudaTecnica.md`. Si algo aquí contradice a esos tres, mandan ellos.

## Estado actual

Rama: `main`
Versión publicada: `0.3.1` (28/07/2026, tag `v0.3.1`) — `IDE-0019` (PR #58,
mergeado 30/07/2026) queda por delante del tag, sin publicar todavía.
Tests: 712, en verde.

Fases del Roadmap (`DOC-003-Roadmap.md`):

| Fase | Estado |
|------|--------|
| 1 — Core | 🟢 Completada |
| 2 — BoardComposer Studio | 🟢 Completada |
| 3 — Plataforma (API, servicios remotos, Cloud) | 🟢 Completada |
| 4 — Inteligencia (IA) | 🟢 Completada |
| 5 — Ecosistema | 🟡 En curso |

Backlog (`DOC-004-Backlog.md`): `IDE-0001`–`IDE-0019`, todos 🟢 completados y
en `main`. No hay ningún IDE en desarrollo ni planificado.

Deuda técnica (`DOC-006-DeudaTecnica.md`): 21 registros, 20 resueltos.
Abierta: `DT-0011` (el `.app` de macOS no está firmado ni notarizado, y solo
se genera para macOS/arm64). Mitigada el 27/07/2026 con todo lo que no exige
cuenta de pago — bundle identifier propio, `docs/INSTALL-macos.md` en cada
release, y firma+notarización ya automatizadas a la espera de credenciales
(`DEC-0017`). Cerrarla del todo cuesta 99 USD/año.

Despliegue privado en marcha (`IDE-0017`): API en `bc.efjdefrutos.com` y
Studio por navegador (noVNC) en `studio.efjdefrutos.com`.

## Trabajo en curso

Ninguno acotado — `IDE-0019` (PR #58) se mergeó el 30/07/2026. El dock
"Timeline" mostraba desde su creación el texto literal "Timeline / Consola /
Eventos"; pasa a tener Resumen (tableros con piezas y % de uso) y Actividad
(log en vivo, primer uso real del `EventBus` de ADR-003, hasta entonces
construido y sin conectar). Por el camino: 6 de 9 clases de comando no
definían `.name` pese a que el Protocol lo exige (`AttributeError` dormido,
nunca disparado hasta que el log lo necesitó), y una revisión `/code-review`
sobre el propio diff encontró y corrigió tres cosas más antes de comitear —
arrastre de pieza sin registrar, `Feature Envy` en deshacer/rehacer, cálculo
de utilización duplicado. 712 tests en verde. El bloque se registró como
`IDE-0019` *después* de construirse, incumpliendo la norma 1 de este
documento — registrado también como `DT-0021`. Aún sin etiquetar: sería
`v0.3.2`.

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

Con el backlog a cero y sin más deuda que dé resultados incorrectos, la
siguiente es una decisión de producto, no técnica. Candidatas, de menor a
mayor alcance (`DOC-999-Ideas.md`):

1. Contratar la cuenta de Apple Developer (99 USD/año) para cerrar `DT-0011`.
   Ya no queda trabajo técnico: cargar los seis secrets en GitHub basta para
   que la siguiente release salga firmada y notarizada (`DEC-0017`).
2. Instancia demo pública — acotada, pero implica infraestructura de pago.
3. Marketplace público de plugins — requiere decidir antes si el mecanismo de
   plugins es para un ecosistema abierto o solo para uso interno.
4. SaaS real (cuentas, persistencia por usuario, facturación) — no es una
   tarea, es una fase nueva del producto.

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
