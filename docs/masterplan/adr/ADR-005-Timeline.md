
# ADR-005 — El Timeline como representación del sistema

| Campo | Valor |
|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Alto |
| Revisión | N/A |

---

## Contexto

BoardComposer no solo debe generar soluciones; también debe permitir comprender cómo se han obtenido. Para ello es necesario disponer de una representación cronológica y reproducible de los acontecimientos relevantes ocurridos durante la vida de un proyecto.

---

## Problema

Los algoritmos de optimización suelen comportarse como una "caja negra": el usuario únicamente ve el resultado final y desconoce el proceso seguido para alcanzarlo.

Alternativas consideradas:

1. Mostrar únicamente el resultado final.
2. Implementar un registro técnico orientado al desarrollador.
3. Construir un Timeline visual basado en los eventos del sistema.

---

## Decisión

Se adopta la tercera alternativa.

BoardComposer dispondrá de un **Timeline** construido a partir de los eventos publicados por el sistema. El Timeline será una representación visual del historial del proyecto y permitirá reproducir, analizar y comprender la evolución de cada operación sin introducir una lógica paralela.

El Timeline consumirá eventos; no generará reglas de negocio.

---

## Consecuencias

### Ventajas

- Explicabilidad de los algoritmos.
- Depuración simplificada.
- Historial cronológico unificado.
- Base para auditorías y formación.
- Reutilización del Event Bus existente.

### Inconvenientes

- Necesidad de mantener un catálogo de eventos estable.
- Posible incremento del volumen de información almacenada.

---

## Principios derivados

- El Timeline refleja hechos ocurridos, nunca estados hipotéticos.
- Toda entrada del Timeline procede de uno o varios eventos registrados.
- El Timeline podrá filtrarse por tipo de evento, algoritmo o intervalo temporal.
- La reproducción nunca modificará el estado del proyecto.

---

## Impacto

Esta decisión afecta a Studio, Event Bus, Inspector, Comparador, sistema de auditoría, IA explicativa y futuras herramientas de análisis.

---

## Relación con otros documentos

- ADR-003 — Arquitectura basada en eventos.
- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- FLW-003 — Generar Soluciones.

---

## Revisión futura

En versiones posteriores el Timeline permitirá reproducción paso a paso de algoritmos, marcadores, anotaciones del usuario, comparación sincronizada entre soluciones, métricas temporales y exportación del historial para análisis o soporte técnico.