# ADR-008 — Arquitectura basada en Commands (Command Pattern)

| Campo | Valor |

|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Muy alto |
| Revisión | N/A |

---

## Contexto

BoardComposer permite realizar numerosas operaciones: crear proyectos, importar piezas, generar soluciones, exportar resultados, modificar configuraciones y, en el futuro, ejecutar automatizaciones, macros y acciones asistidas por IA.

Estas operaciones deben ejecutarse de forma uniforme, registrable y reproducible.

---

## Problema

Si cada acción se implementa como una llamada directa entre componentes, será muy difícil añadir capacidades como deshacer, rehacer, macros, scripting, historial detallado o automatización.

Alternativas consideradas:

1. Acciones implementadas mediante llamadas directas.
2. Mezclar distintos mecanismos según cada módulo.
3. Representar cada operación mediante un Command bien definido.

---

## Decisión

Se adopta la tercera alternativa.

Toda operación relevante iniciada por el usuario, una automatización o un servicio externo se representará mediante un **Command**.

Un Command describe una intención de cambio. Tras su ejecución, el Core aplicará la lógica correspondiente y publicará los eventos de dominio necesarios mediante el Event Bus.

Los Commands no sustituyen al Event Bus; ambos mecanismos son complementarios.

---

## Ejemplos de Commands

- CreateProjectCommand
- ImportCsvCommand
- GenerateSolutionsCommand
- SelectSolutionCommand
- ExportSolutionCommand
- UpdateProjectCommand
- DeleteBoardCommand
- AddPieceCommand

---

## Consecuencias

### Ventajas

- Base para Deshacer y Rehacer.
- Automatizaciones reproducibles.
- Macros y scripting.
- Integración sencilla con API y CLI.
- Compatibilidad con asistentes basados en IA.
- Registro homogéneo de operaciones.

### Inconvenientes

- Mayor número de clases u objetos.
- Necesidad de definir contratos claros para cada Command.
- Mayor disciplina arquitectónica.

---

## Principios derivados

- Toda modificación del sistema comienza mediante un Command.
- Un Command expresa una intención; un Event describe un hecho ocurrido.
- Los Commands son validados antes de ejecutarse.
- El Core decide si un Command produce cambios.
- Un Command nunca modifica directamente el estado desde la interfaz.

---

## Relación entre Commands y Events

```text
Usuario
    │
    ▼
Command
    │
    ▼
Core
    │
    ▼
Eventos
    │
    ▼
Studio · API · CLI · Plugins · Timeline
```

---

## Impacto

Esta decisión afecta al Core, Studio, CLI, API, Event Bus, Timeline, automatizaciones, plugins, IA y futuras integraciones.

---

## Relación con otros documentos

- ADR-001 — El Core es la única fuente de verdad.
- ADR-003 — Arquitectura basada en eventos.
- ADR-005 — El Timeline como representación del sistema.
- DOC-002 — Arquitectura.
- DOC-008 — API y Extensibilidad.

---

## Revisión futura

En versiones posteriores podrá incorporarse un Command Bus, colas de ejecución, ejecución asíncrona, comandos compuestos (macros), políticas de autorización, registro completo para auditoría y reproducción automática de secuencias de trabajo.
