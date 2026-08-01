# ADR-006 — Identidad permanente de los artefactos

| Campo | Valor |

|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Muy alto |
| Revisión | N/A |

---

> ⚠️ **Parcialmente implementado.** El UUID permanente solo existe en
> `StudioProject.project_id` (`uuid.uuid4()`, `main_window.py`). `Project`
> y `AssemblySolution` del Core no tienen ningún campo de identidad. La
> convención de ID legible (`SOL-000123`/`PRJ-000042` como capa separada
> del UUID) no está implementada — el UUID se usa en crudo, con
> `"PRJ-DEMO-001"` como único caso hardcodeado para el proyecto demo.
> Verificado 01/08/2026.

---

## Contexto

BoardComposer gestionará proyectos, soluciones, importaciones, exportaciones, revisiones, plugins y otros artefactos que deberán mantenerse identificables durante toda su vida útil, incluso cuando cambien de nombre, ubicación o formato.

---

## Problema

Basar la identidad de los elementos en nombres o rutas provoca ambigüedades, dificulta la trazabilidad y complica las integraciones externas.

Alternativas consideradas:

1. Identificar los artefactos mediante su nombre.
2. Utilizar identificadores secuenciales visibles únicamente.
3. Asignar una identidad permanente e independiente del contenido mediante UUID.

---

## Decisión

Se adopta la tercera alternativa.

Todo artefacto relevante dispondrá de un identificador UUID inmutable generado en el momento de su creación.

Además, aquellos elementos que interactúen con el usuario podrán disponer de un identificador legible (por ejemplo, `SOL-000123` o `PRJ-000042`), que actuará únicamente como referencia visual.

El UUID será siempre la identidad canónica del sistema.

---

## Artefactos identificados

- Proyecto.
- Solución.
- Importación.
- Exportación.
- Revisión.
- Plugin.
- Perfil de exportación.
- Plantilla.

---

## Consecuencias

### Ventajas

- Trazabilidad completa.
- Referencias estables entre componentes.
- Integración sencilla con API y plugins.
- Historial consistente.
- Compatibilidad con sincronización y colaboración futura.

### Inconvenientes

- Necesidad de mantener la correspondencia entre UUID e identificadores visibles.
- Mayor complejidad en tareas de depuración manual.

---

## Principios derivados

- El UUID nunca cambia.
- El nombre puede modificarse sin afectar a la identidad.
- Los enlaces internos utilizarán UUID.
- Las interfaces mostrarán identificadores legibles cuando resulte conveniente.
- Ningún componente dependerá del nombre como clave funcional.

---

## Impacto

Esta decisión afecta al Core, Studio, API, CLI, Event Bus, Timeline, exportaciones, importaciones, plugins y futuras integraciones.

---

## Relación con otros documentos

- ADR-001 — El Core es la única fuente de verdad.
- ADR-002 — Las soluciones son inmutables.
- ADR-003 — Arquitectura basada en eventos.
- ADR-005 — El Timeline como representación del sistema.
- DOC-002 — Arquitectura.
- DOC-008 — API y Extensibilidad.

---

## Revisión futura

En versiones posteriores podrán incorporarse identificadores distribuidos, sincronización entre dispositivos, resolución de conflictos y mecanismos de federación, manteniendo siempre el UUID como identidad primaria de cada artefacto.
