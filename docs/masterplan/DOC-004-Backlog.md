# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 01/07/2026

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
| IDE-0007 | Asistente IA | 🟡 | P2 |
| IDE-0008 | Sistema de plugins | ⚪ | P3 |

---

## IDE-0007 — Asistente IA

**Estado:** 🟡 En desarrollo. Proveedor real todavía sin decidir.

Alcance dividido en fases, cada una construida sobre la anterior:

- **Fase A** (🟢 completada) — puerto `AIProvider` en el Core (`src/boardcomposer/ai/`) con `MockAIProvider` y `provider_by_name()`, sin proveedor real conectado.
- **Fase B** (🟢 completada) — `project_from_text()` (`src/boardcomposer/ai/project_from_text.py`): genera un `Project` a partir de texto libre, pidiendo al `AIProvider` un JSON con la misma forma que ya valida `/solve` en la API.
- **Fase C** (⚪) — explicación en lenguaje natural de un `AssemblySolution`, apoyada en `SolutionExplanation`.
- **Fase D** (⚪) — sugerencia/optimización de disposiciones más allá de las estrategias `balanced`/`material`/`compact`.
- **Fase E** (⚪) — chat de ayuda contextual, panel nuevo en Studio.
- **Fase F** (⚪) — exposición de las capacidades anteriores vía API (`/assist/...`).

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
