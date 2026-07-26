# BoardComposer — Índice del Masterplan

**Última revisión:** 26/07/2026

Punto de entrada a la documentación de proyecto. El resumen de estado y las
normas de trabajo están en [`MASTERPLAN.md`](MASTERPLAN.md); si algo de ahí
contradice a `DOC-003`, `DOC-004` o `DOC-006`, mandan estos últimos.

## Documentos maestros

| Documento | Contenido | Cuándo consultarlo |
|---|---|---|
| [`MASTERPLAN.md`](MASTERPLAN.md) | Estado actual, trabajo en curso, próxima decisión, normas de trabajo. | Primer fichero a leer al retomar el proyecto. |
| [`DOC-000-Manifiesto.md`](DOC-000-Manifiesto.md) | Principios y propósito del producto. | Antes de aceptar o rechazar una idea nueva. |
| [`DOC-001-Producto.md`](DOC-001-Producto.md) | Qué es BoardComposer, para quién y qué no es. | Al acotar alcance. |
| [`DOC-002-Arquitectura.md`](DOC-002-Arquitectura.md) | Principios arquitectónicos (nivel producto). | Antes de introducir una capa o dependencia nueva. |
| [`DOC-003-Roadmap.md`](DOC-003-Roadmap.md) | Fases 1–5 y prioridades P0/P1/P2. | Para saber la dirección, no el detalle. |
| [`DOC-004-Backlog.md`](DOC-004-Backlog.md) | Estado vivo funcionalidad por funcionalidad (`IDE-xxxx`). | **Fuente de verdad** de qué está hecho. |
| [`DOC-005-Decisiones.md`](DOC-005-Decisiones.md) | Registro de decisiones (`DEC-xxxx`). | Antes de revisitar algo ya decidido. |
| [`DOC-006-DeudaTecnica.md`](DOC-006-DeudaTecnica.md) | Deuda técnica (`DT-xxxx`), abierta y resuelta. | Al cerrar un bloque y antes de publicar versión. |
| [`DOC-007-UX-Studio.md`](DOC-007-UX-Studio.md) | Criterios de experiencia de usuario de Studio. | Al tocar la interfaz. |
| [`DOC-008-API.md`](DOC-008-API.md) | Contrato y criterios de la API HTTP. | Al modificar endpoints. |
| [`DOC-999-Ideas.md`](DOC-999-Ideas.md) | Ideas sin acotar (marketplace, demo pública, SaaS). | Solo como cantera; nada de aquí está comprometido. |

## Decisiones de arquitectura (ADR)

| ADR | Tema |
|---|---|
| [ADR-001](adr/ADR-001-Core-Inmutable.md) | Core inmutable e independiente de la interfaz. |
| [ADR-002](adr/ADR-002-Soluciones-Inmutables.md) | Soluciones inmutables. |
| [ADR-003](adr/ADR-003-Event-Bus.md) | Event Bus síncrono en Studio. |
| [ADR-004](adr/ADR-004-Plugin-System.md) | Sistema de plugins por *entry points*. |
| [ADR-005](adr/ADR-005-Timeline.md) | Timeline. |
| [ADR-006](adr/ADR-006-Project-UUID.md) | Identidad de proyecto por UUID. |
| [ADR-007](adr/ADR-007-UI-Contextual.md) | Interfaz contextual. |
| [ADR-008](<adr/ADR-008-Arquitectura basada en Commands (Command Pattern).md>) | Command Pattern para undo/redo. |
| [ADR-009](<adr/ADR-009-Ley de estabilidad visual.md>) | Ley de estabilidad visual. |
| [ADR-010](adr/ADR-010-PlacementValidator.md) | `PlacementValidator` como única fuente de verdad de colocación. |
| [ADR-011](adr/ADR-011-Workspace-Blueprint.md) | Blueprint del workspace. |
| [ADR-012](adr/ADR-012-SelectionController.md) | `SelectionController`. |
| [ADR-013](adr/ADR-013-Geometry-Engine.md) | Motor de geometría. |

## Especificaciones de interfaz

Pantallas (`ui/`): [SCR-001 Inicio](<ui/SCR-001-Pantalla de Inicio.md>) ·
[SCR-002 Workspace](ui/SCR-002-Workspace.md) ·
[SCR-003 Comparador](ui/SCR-003-Comparador.md) ·
[SCR-004 Inspector](ui/SCR-004-Inspector.md) ·
[SCR-005 Proyecto](ui/SCR-005-Proyecto.md) ·
[SCR-006 Preferencias](ui/SCR-006-Preferencias.md) ·
[SCR-007 Exportación](<ui/SCR-007-Exportación.md>)

Flujos (`ui/flows/`): [FLW-001 Crear proyecto](ui/flows/FLW-001-Crear-Proyecto.md) ·
[FLW-002 Importar CSV](ui/flows/FLW-002-Importar-CSV.md) ·
[FLW-003 Generar soluciones](ui/flows/FLW-003-Generar-Soluciones.md) ·
[FLW-004 Comparar](ui/flows/FLW-004-Comparar.md) ·
[FLW-005 Exportar](ui/flows/FLW-005-Exportar.md) ·
[FLW-006 Editar proyecto](ui/flows/FLW-006-Editar-Proyecto.md)

Las especificaciones describen el diseño previsto, no necesariamente lo
implementado: cuando el código se aparta de una SCR (campos que el modelo de
datos no soporta, métricas que el dominio no calcula), la desviación queda
anotada en `docs/studio.md`, no en la propia SCR.

## Documentación técnica y de usuario (fuera del masterplan)

| Fichero | Contenido |
|---|---|
| [`../../README.md`](../../README.md) | Instalación, uso desde terminal, API y Studio. |
| [`../cli.md`](../cli.md) | Referencia completa de la línea de comandos. |
| [`../architecture.md`](../architecture.md) | Estructura real del código, capa por capa. |
| [`../studio.md`](../studio.md) | Documentación funcional de Studio. |
| [`../algorithms.md`](../algorithms.md), [`../scoring.md`](../scoring.md), [`../solver_architecture.md`](../solver_architecture.md) | Generadores, puntuación y solvers. |
| [`../data_model.md`](../data_model.md) | Modelo de datos del Core. |
| [`../plugins.md`](../plugins.md) | Guía para desarrolladores de plugins. |
| [`../deploy.md`](../deploy.md), [`../deploy-studio-remote.md`](../deploy-studio-remote.md) | Despliegue de la API y de Studio remoto. |
| [`../../CHANGELOG.md`](../../CHANGELOG.md) | Historial de versiones. |

Ficheros de la raíz marcados **Superado** (`ROADMAP.md`, `TODO.md`,
`DECISIONS.md`, `docs/estructura.md`, `docs/project_structure.md`) son el
andamiaje del primer día del proyecto; se conservan como registro histórico y
no se mantienen.
