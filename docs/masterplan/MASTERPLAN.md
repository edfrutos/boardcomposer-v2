# BoardComposer — MASTERPLAN

**Última revisión:** 26/07/2026

> Este documento resume el estado del proyecto y las normas de trabajo.
> El detalle vivo de cada funcionalidad está en `DOC-004-Backlog.md`, la
> dirección del producto en `DOC-003-Roadmap.md` y la deuda técnica en
> `DOC-006-DeudaTecnica.md`. Si algo aquí contradice a esos tres, mandan ellos.

## Estado actual

Rama: `main`
Versión publicada: `0.3.0` (26/07/2026, tag `v0.3.0`)
Tests: 673, en verde.

Fases del Roadmap (`DOC-003-Roadmap.md`):

| Fase | Estado |
|------|--------|
| 1 — Core | 🟢 Completada |
| 2 — BoardComposer Studio | 🟢 Completada |
| 3 — Plataforma (API, servicios remotos, Cloud) | 🟢 Completada |
| 4 — Inteligencia (IA) | 🟢 Completada |
| 5 — Ecosistema | 🟡 En curso |

Backlog (`DOC-004-Backlog.md`): `IDE-0001`–`IDE-0018`, todos 🟢 completados.
No hay ningún IDE en desarrollo ni planificado.

Deuda técnica (`DOC-006-DeudaTecnica.md`): 20 registros, 18 resueltos. Abiertas:

- `DT-0011` — el `.app` de macOS no está firmado ni notarizado, y solo se
  genera para macOS/arm64. A abordar solo si se necesita distribución pública
  o fuera de macOS Apple Silicon.
- `DT-0020` — el ancho de sierra (kerf) se configura y persiste, pero solo lo
  aplica el arrastre interactivo: ni el solver, ni el encaje fuera del lienzo,
  ni la exportación lo tienen en cuenta. Requiere decidir antes si el kerf
  pertenece al dominio del Core o se queda como ayuda visual de Studio.

Despliegue privado en marcha (`IDE-0017`): API en `bc.efjdefrutos.com` y
Studio por navegador (noVNC) en `studio.efjdefrutos.com`.

## Trabajo en curso

Ninguno acotado. `v0.3.0` recoge todo lo acumulado desde `v0.2.0`: corrección
y endurecimiento sobre funcionalidad ya entregada, no capacidades nuevas —
validación de números finitos en todas las entradas externas, recuperación de
proyectos con colocaciones colgantes, errores de fichero con número de línea en
vez de traceback, y siete correcciones de Studio (validación al editar/mover
piezas, sincronía de rotación, no vaciar otros tableros al aplicar una
disposición). Registrado como `DT-0017`–`DT-0019` en `DOC-006-DeudaTecnica.md`.

Incluye además la revisión completa de la documentación (26/07/2026): índice
del masterplan (`INDEX.md`, hasta entonces vacío), referencia de usuario de la
línea de comandos (`docs/cli.md`, nueva), y `README.md`, `docs/studio.md` y
`docs/architecture.md` alineados con el código actual.

La sección "Sin publicar" de `CHANGELOG.md` vuelve a estar vacía.

## Próxima decisión

Con el backlog a cero, la siguiente es una decisión de producto, no técnica.
Candidatas, de menor a mayor alcance (`DOC-999-Ideas.md`):

1. Cerrar `DT-0020` (ancho de sierra): decidir si el kerf pertenece al dominio
   del Core — y entonces afecta a `ProjectConstraints` y a todos los
   generadores — o se queda como ayuda visual del arrastre en Studio. Es la
   única deuda abierta que puede dar un resultado incorrecto al usuario: hoy
   una disposición generada o un plano exportado asumen corte de anchura cero.
2. Cerrar `DT-0011` (firma y notarización de Apple) si se quiere distribuir
   el `.app` fuera del entorno propio.
3. Instancia demo pública — acotada, pero implica infraestructura de pago.
4. Marketplace público de plugins — requiere decidir antes si el mecanismo de
   plugins es para un ecosistema abierto o solo para uso interno.
5. SaaS real (cuentas, persistencia por usuario, facturación) — no es una
   tarea, es una fase nueva del producto.

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
