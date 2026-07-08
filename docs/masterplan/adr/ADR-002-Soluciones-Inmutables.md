# ADR-002 — Las soluciones son inmutables

| Campo | Valor |

|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Muy alto |
| Revisión | N/A |

---

## Contexto

BoardComposer puede generar múltiples soluciones para un mismo proyecto utilizando diferentes algoritmos, estrategias y parámetros. Es imprescindible que cada solución represente fielmente el resultado obtenido en el momento de su generación.

---

## Problema

Si una solución pudiera modificarse directamente tras ser generada, dejaría de representar el resultado real producido por el algoritmo, dificultando la comparación, la auditoría y la reproducción de los cálculos.

Las alternativas consideradas fueron:

1. Permitir modificar las soluciones directamente.
2. Mantener las soluciones inmutables y generar nuevas revisiones cuando sea necesario.

---

## Decisión

Se adopta la segunda alternativa.

Una vez generada, una solución será **inmutable**.

Cualquier cambio que afecte al resultado (piezas, tableros, restricciones, parámetros o edición manual) dará lugar a una nueva solución con una identidad propia, preservando siempre la anterior.

---

## Consecuencias

### Ventajas

- Comparaciones fiables entre soluciones.
- Reproducción exacta de resultados.
- Historial completo de la evolución del proyecto.
- Trazabilidad para informes y exportaciones.
- Base sólida para control de versiones y colaboración.

### Inconvenientes

- Mayor consumo de almacenamiento.
- Necesidad de gestionar múltiples revisiones.

---

## Principios derivados

- Una solución nunca se edita; se reemplaza por una nueva versión.
- Toda solución tendrá un identificador único.
- Las exportaciones harán referencia a la solución que las originó.
- Las comparaciones siempre se realizarán entre soluciones completas.

---

## Impacto

Esta decisión afecta a:

- Generación de soluciones.
- Comparador.
- Workspace.
- Exportación.
- Historial del proyecto.
- API.
- Plugins.

---

## Relación con otros documentos

- ADR-001 — El Core es la única fuente de verdad.
- DOC-002 — Arquitectura.
- DOC-008 — API y Extensibilidad.
- FLW-003 — Generar Soluciones.
- FLW-004 — Comparar Soluciones.

---

## Revisión futura

Si en el futuro se permite edición manual de una disposición, dicha edición deberá generar automáticamente una nueva solución derivada, manteniendo intacta la solución original y conservando la relación entre ambas mediante su historial de revisiones.
