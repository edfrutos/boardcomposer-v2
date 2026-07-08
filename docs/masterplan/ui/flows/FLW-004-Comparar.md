# FLW-004 — Comparar Soluciones

**Módulo:** BoardComposer Studio

**Código:** FLW-004
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

Describir el flujo que permite al usuario comparar distintas soluciones de optimización para seleccionar la más adecuada según criterios técnicos, económicos y productivos.

---

## Actor principal

- Usuario.

---

## Precondiciones

- El proyecto dispone de dos o más soluciones generadas.
- Las soluciones han sido evaluadas y clasificadas.

---

## Flujo principal

1. El usuario abre el Comparador (SCR-003).
2. Studio carga las soluciones disponibles.
3. El usuario selecciona las soluciones que desea comparar.
4. Se muestran simultáneamente las vistas gráficas y las métricas.
5. El usuario explora diferencias y explicaciones.
6. Puede fijar una solución como referencia.
7. Selecciona la solución preferida.
8. Studio actualiza el Workspace con la solución elegida.

---

## Flujo alternativo A — Una única solución

1. Solo existe una solución disponible.
2. Studio informa de ello y ofrece volver al Workspace o generar nuevas soluciones.

---

## Flujo alternativo B — Regenerar soluciones

1. El usuario considera que ninguna alternativa es satisfactoria.
2. Solicita una nueva generación modificando algoritmos o restricciones.
3. El flujo continúa en FLW-003 — Generar Soluciones.

---

## Información comparada

- Aprovechamiento.
- Desperdicio.
- Número de tableros.
- Número de cortes.
- Fragmentación.
- Tiempo de cálculo.
- Algoritmo.
- Estrategia utilizada.
- Puntuación global.
- Explicación resumida.

---

## Eventos generados

- ComparisonOpened
- SolutionSelected
- ReferenceSolutionChanged
- WorkspaceUpdated

---

## Resultado esperado

El usuario identifica con claridad las ventajas e inconvenientes de cada alternativa y selecciona conscientemente la solución que mejor se adapta a su objetivo.

---

## Criterios de aceptación

- Comparación visual inmediata.
- Métricas sincronizadas entre soluciones.
- Posibilidad de cambiar de referencia sin recalcular.
- Apertura instantánea de la solución elegida en el Workspace.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.

---

## Observaciones

En futuras versiones el Comparador incorporará reproducción sincronizada mediante Timeline, análisis asistido por IA, comparación histórica entre versiones del proyecto, gráficos avanzados y recomendaciones automáticas basadas en los objetivos definidos por el usuario.
