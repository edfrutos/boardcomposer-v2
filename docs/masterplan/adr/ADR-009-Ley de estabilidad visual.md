# ADR-009 — Ley de estabilidad visual

| Campo | Valor |

|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Alto |
| Revisión | N/A |

---

## Contexto

BoardComposer Studio mostrará información muy diversa: proyectos, tableros, piezas, soluciones, comparativas, métricas y herramientas avanzadas. A medida que cambie el contexto, la interfaz deberá adaptarse sin desorientar al usuario.

---

## Problema

Las interfaces que modifican continuamente la posición de paneles, barras de herramientas o controles obligan al usuario a reaprender la disposición de la aplicación, reduciendo la productividad y aumentando la carga cognitiva.

Alternativas consideradas:

1. Reorganizar completamente la interfaz según cada contexto.
2. Mantener una estructura estable y modificar únicamente el contenido relevante.

---

## Decisión

Se adopta la segunda alternativa.

BoardComposer Studio mantendrá una estructura visual estable. Los paneles conservarán su posición y función general; únicamente cambiarán su contenido, las acciones disponibles o el nivel de detalle en función del contexto activo.

---

## Principios derivados

- La disposición general de Studio será constante.
- Los cambios de contexto modificarán el contenido, no la estructura.
- Las transiciones visuales serán suaves y predecibles.
- El usuario deberá conservar en todo momento la referencia espacial de la interfaz.
- La personalización del espacio de trabajo nunca romperá estos principios.

---

## Consecuencias

### Ventajas

- Menor carga cognitiva.
- Aprendizaje más rápido.
- Mayor productividad en sesiones largas.
- Interfaz coherente y profesional.
- Escalabilidad al añadir nuevas funcionalidades.

### Inconvenientes

- Requiere un diseño cuidadoso de los paneles contextuales.
- Algunas funciones deberán adaptarse al espacio disponible.

---

## Impacto

Esta decisión afecta a todas las pantallas de BoardComposer Studio, especialmente al Workspace, Inspector, Comparador, Exportación y futuros espacios de trabajo.

---

## Relación con otros documentos

- ADR-007 — La interfaz es contextual.
- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- DOC-003 — Diseño de interfaz.

---

## Revisión futura

En futuras versiones podrán incorporarse espacios de trabajo personalizados y paneles acoplables, siempre respetando la ley de estabilidad visual como principio de diseño fundamental.
