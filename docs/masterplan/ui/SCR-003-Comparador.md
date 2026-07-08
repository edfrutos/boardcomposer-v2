
# SCR-003 — Comparador de Soluciones

**Módulo:** BoardComposer Studio

**Código:** SCR-003
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

El Comparador permite analizar simultáneamente varias soluciones generadas por distintos algoritmos o configuraciones, facilitando una decisión fundamentada basada en datos objetivos y visualización directa.

---

## Filosofía

BoardComposer no pretende ofrecer una única respuesta «correcta». Su propósito es mostrar alternativas, explicar sus diferencias y ayudar al profesional a elegir la solución más adecuada para cada proyecto.

---

## Distribución conceptual

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Comparador de Soluciones                                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Solución A │ Solución B │ Solución C │ Solución D                            │
├──────────────────────────────────────────────────────────────────────────────┤
│ Vista gráfica de cada tablero                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│ Aprovechamiento │ Desperdicio │ Cortes │ Tiempo │ Calidad │ Puntuación       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Explicación │ Diferencias │ Seleccionar │ Exportar                            │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Componentes principales

## Panel de soluciones

Muestra varias soluciones de forma simultánea con miniaturas sincronizadas.

## Métricas comparativas

Cada solución incluirá, como mínimo:

- porcentaje de aprovechamiento;
- superficie desperdiciada;
- número de cortes;
- tiempo de cálculo;
- puntuación global;
- algoritmo utilizado.
- fragmentación del material;
- número de tableros utilizados;
- tiempo estimado de mecanizado (cuando esté disponible).

## Panel de diferencias

Resalta únicamente aquello que cambia entre soluciones para facilitar el análisis.

## Acciones

- Seleccionar solución activa.
- Abrir en Workspace.
- Exportar.
- Fijar como favorita.

## Explicación de la solución

Cada solución dispondrá de un resumen que explique por qué ha obtenido su puntuación y cuáles son sus principales fortalezas y debilidades.

---

## Flujo principal

1. Generar varias soluciones.
2. Abrir el Comparador.
3. Analizar métricas y representación gráfica.
4. Revisar explicaciones.
5. Seleccionar la solución preferida.
6. Volver al Workspace o exportar.

---

## Principios de interacción

- Comparación visual inmediata.
- Misma escala para todos los tableros.
- Métricas sincronizadas.
- Navegación fluida entre soluciones.
- Posibilidad de fijar una solución como referencia.
- posibilidad de establecer una solución como referencia para comparar el resto.

---

## Criterios de aceptación

- Comparar hasta cuatro soluciones simultáneamente.
- Cambiar entre soluciones sin regenerarlas.
- Visualizar diferencias relevantes de un vistazo.
- Exportar directamente la solución seleccionada.

---

## Relación con otras pantallas

- SCR-002 — Workspace.
- SCR-004 — Inspector.
- SCR-007 — Exportación.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- comparación ilimitada mediante pestañas;
- gráficos históricos de rendimiento;
- recomendaciones automáticas mediante IA;
- comparación entre versiones de un mismo proyecto;
- reproducción sincronizada del proceso de colocación (Timeline).
