
# ADR-004 — Arquitectura de Plugins

| Campo | Valor |
|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Muy alto |
| Revisión | N/A |

---

## Contexto

BoardComposer debe evolucionar sin convertir el Core en un sistema monolítico. Nuevos algoritmos, importadores, exportadores, analizadores e integraciones deberán poder incorporarse sin modificar el núcleo de la aplicación.

---

## Problema

Si toda nueva funcionalidad exige modificar el Core, cada ampliación incrementará el acoplamiento, dificultará las pruebas y aumentará el riesgo de regresiones.

Alternativas consideradas:

1. Incorporar todas las funcionalidades al Core.
2. Permitir extensiones mediante puntos de integración controlados.
3. Cargar código arbitrario sin restricciones.

---

## Decisión

Se adopta la segunda alternativa.

BoardComposer dispondrá de un sistema oficial de plugins basado en puntos de extensión documentados.

Los plugins ampliarán capacidades, pero nunca sustituirán las reglas fundamentales del Core ni modificarán directamente su estado interno.

---

## Tipos iniciales de plugins

- Algoritmos de optimización.
- Importadores.
- Exportadores.
- Presentadores.
- Analizadores y métricas.
- Integraciones externas.
- Automatizaciones.

---

## Consecuencias

### Ventajas

- Arquitectura extensible.
- Menor acoplamiento.
- Ecosistema abierto para terceros.
- Evolución independiente de módulos.
- Facilita pruebas aisladas.

### Inconvenientes

- Mayor complejidad en la gestión del ciclo de vida.
- Necesidad de versionar la API de plugins.
- Requisitos de compatibilidad y seguridad.

---

## Principios derivados

- Todo plugin utilizará únicamente APIs públicas.
- El Core nunca dependerá de un plugin concreto.
- Los plugins podrán añadirse o retirarse sin recompilar el Core.
- Los puntos de extensión estarán documentados y versionados.
- Los fallos de un plugin no deberán comprometer la estabilidad del sistema.

---

## Impacto

Esta decisión afecta a Studio, CLI, API, importadores, exportadores, algoritmos, integraciones, automatizaciones y futuras extensiones desarrolladas por terceros.

---

## Relación con otros documentos

- ADR-001 — El Core es la única fuente de verdad.
- ADR-003 — Arquitectura basada en eventos.
- DOC-008 — API y Extensibilidad.
- SCR-007 — Exportación.

---

## Revisión futura

En versiones posteriores se definirá un SDK oficial para plugins, un manifiesto de capacidades, control de compatibilidad por versiones, firma digital opcional y un catálogo de extensiones instalables desde BoardComposer Studio.