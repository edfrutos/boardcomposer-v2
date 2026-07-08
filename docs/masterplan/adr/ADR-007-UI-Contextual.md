# ADR-007 — La interfaz es contextual

| Campo | Valor |

|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Muy alto |
| Revisión | N/A |

---

## Contexto

BoardComposer Studio debe gestionar proyectos complejos sin sobrecargar al usuario con paneles, botones o información innecesaria. La aplicación trabajará con distintos tipos de elementos (proyectos, tableros, piezas, soluciones, algoritmos y exportaciones), cada uno con necesidades de información diferentes.

---

## Problema

Una interfaz estática obliga a mostrar simultáneamente controles que solo son útiles en determinados momentos, aumentando la complejidad y la carga cognitiva.

Alternativas consideradas:

1. Interfaz fija con todos los paneles visibles.
2. Múltiples pantallas independientes para cada tipo de objeto.
3. Interfaz contextual que adapte dinámicamente su contenido según la selección y el flujo de trabajo.

---

## Decisión

Se adopta la tercera alternativa.

BoardComposer Studio utilizará una interfaz contextual. El contenido de paneles como el Inspector, la barra de herramientas, los menús contextuales y determinadas acciones cambiará automáticamente en función del contexto activo.

La lógica de negocio permanecerá en el Core; la interfaz únicamente adaptará la presentación y las acciones disponibles.

---

## Contextos iniciales

- Proyecto.
- Tablero.
- Pieza.
- Solución.
- Algoritmo.
- Comparación.
- Exportación.

---

## Consecuencias

### Ventajas

- Menor carga cognitiva.
- Interfaz más limpia.
- Aprendizaje progresivo.
- Mayor productividad.
- Escalabilidad al incorporar nuevas funciones.

### Inconvenientes

- Mayor complejidad en la gestión de estados de la interfaz.
- Necesidad de definir claramente cada contexto y sus transiciones.

---

## Principios derivados

- Solo se mostrará información relevante para el contexto activo.
- Las acciones disponibles dependerán de la selección actual.
- Los cambios de contexto deberán ser inmediatos y predecibles.
- La disposición general de Studio permanecerá estable para favorecer la memoria espacial del usuario.
- Ningún cambio visual alterará el estado funcional del Core.

---

## Impacto

Esta decisión afecta al Workspace, Inspector, Comparador, Exportación, futuros paneles, sistema de comandos, accesos rápidos y extensiones de interfaz.

---

## Relación con otros documentos

- ADR-001 — El Core es la única fuente de verdad.
- ADR-003 — Arquitectura basada en eventos.
- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- SCR-007 — Exportación.

---

## Revisión futura

En versiones posteriores la interfaz contextual podrá incorporar espacios de trabajo especializados, personalización por perfiles, adaptación inteligente mediante IA y recomendaciones contextuales basadas en el comportamiento del usuario, manteniendo siempre una experiencia coherente y predecible.
