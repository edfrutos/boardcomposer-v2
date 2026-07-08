# ADR-003 — Arquitectura basada en eventos (Event Bus)

| Campo | Valor |

|--------|-------|

| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Muy alto |
| Revisión | N/A |

---

## Contexto

BoardComposer integra múltiples componentes: Core, Studio, CLI, API, exportadores, plugins y futuras automatizaciones. Estas capas necesitan reaccionar a cambios del sistema sin establecer dependencias directas entre ellas.

---

## Problema

Una comunicación basada en llamadas directas entre componentes incrementaría el acoplamiento y dificultaría la incorporación de nuevas funcionalidades.

Alternativas consideradas:

1. Comunicación directa entre módulos.
2. Observadores específicos para cada componente.
3. Bus de eventos común para todo el sistema.

---

## Decisión

Se adopta una arquitectura basada en un **Event Bus** interno.

El Core publicará eventos de dominio y el resto de componentes podrá suscribirse a ellos sin conocer la implementación de quien los genera.

El Event Bus será un mecanismo de comunicación, nunca un lugar donde resida lógica de negocio.

---

## Eventos iniciales

- ProjectCreated
- ProjectModified
- ProjectSaved
- CsvImported
- SolutionGenerationStarted
- SolutionGenerated
- SolutionSelected
- ExportCompleted
- WorkspaceUpdated

---

## Consecuencias

### Ventajas

- Bajo acoplamiento.
- Mayor extensibilidad.
- Facilita plugins y automatizaciones.
- Permite instrumentación, registro y telemetría.
- Simplifica la evolución de Studio.

### Inconvenientes

- Mayor complejidad para depurar flujos de eventos.
- Necesidad de documentar cuidadosamente cada evento.
- Riesgo de exceso de eventos si no existe disciplina.

---

## Principios derivados

- Los eventos describen hechos ya ocurridos.
- Un evento no solicita acciones; comunica cambios.
- El nombre de los eventos utilizará tiempo pasado (ProjectCreated, SolutionGenerated...).
- Los consumidores no dependerán entre sí.

---

## Impacto

Esta decisión afecta a Studio, Core, API, CLI, plugins, automatizaciones, registro de actividad y futuras integraciones.

---

## Relación con otros documentos

- ADR-001 — El Core es la única fuente de verdad.
- ADR-002 — Las soluciones son inmutables.
- DOC-002 — Arquitectura.
- DOC-008 — API y Extensibilidad.
- FLW-001 a FLW-006.

---

## Revisión futura

En versiones posteriores podrán diferenciarse eventos de dominio, de aplicación y de interfaz, manteniendo un catálogo oficial y versionado para preservar la compatibilidad entre componentes y extensiones.
