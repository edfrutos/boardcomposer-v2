# BoardComposer Studio

## SCR-002 — Workspace

**Código:** SCR-002
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

El Workspace es el núcleo operativo de BoardComposer Studio. Desde esta pantalla el usuario visualiza los tableros, genera soluciones, compara algoritmos e inspecciona cada colocación sin abandonar el contexto de trabajo.

---

## Filosofía

El Workspace no es un simple visor de planos. Es un entorno interactivo donde el usuario explora alternativas, comprende el comportamiento de los algoritmos y toma decisiones fundamentadas.

---

## Distribución conceptual

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Barra superior: Proyecto | Algoritmo | Resolver | Comparar | Exportar | Buscar | Usuario   │
├───────────────┬───────────────────────────────────────────────────────────────┬─────────────┤
│ Explorador    │                                                               │ Inspector   │
│ Proyecto      │                                                               │             │
│               │                                                               │ Propiedades │
│ • Tableros    │               Workspace gráfico                               │ Métricas    │
│ • Piezas      │                                                               │ Explicación │
│ • Soluciones  │                                                               │             │
├───────────────┴───────────────────────────────────────────────────────────────┴─────────────┤
│ Comparador | Consola | Eventos | Calidad | Rendimiento | Aprovechamiento                      │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Componentes principales

## Barra superior

- Gestión del proyecto.
- Selección de algoritmo.
- Generación de soluciones.
- Comparación.
- Exportación.
- Búsqueda global.

## Explorador del proyecto

Árbol jerárquico con tableros, piezas, soluciones, materiales y recursos asociados.

## Workspace gráfico

Zona principal donde se representan los tableros y las piezas colocadas. Deberá admitir zoom, desplazamiento, selección, resaltado y futuras animaciones del proceso de colocación.

## Inspector

Panel contextual que muestra únicamente la información del elemento seleccionado: proyecto, tablero, pieza, solución o algoritmo.

## Panel inferior

Área con pestañas para:

- Comparador.
- Consola.
- Registro de eventos.
- Métricas.
- Diagnóstico.

---

## Flujo principal

1. Abrir un proyecto.
2. Configurar algoritmo y restricciones.
3. Generar una o varias soluciones.
4. Explorar visualmente cada alternativa.
5. Inspeccionar métricas y explicaciones.
6. Comparar resultados.
7. Exportar la solución elegida.

---

## Principios de interacción

- Selección directa sobre el tablero.
- Actualización inmediata del Inspector.
- Comparación sin cambiar de pantalla.
- Información contextual y no intrusiva.
- Atajos de teclado para operaciones frecuentes.

---

## Criterios de aceptación

- El usuario identifica el estado del proyecto de un vistazo.
- Todas las operaciones principales son accesibles sin abandonar el Workspace.
- El Inspector refleja siempre el contexto seleccionado.
- La navegación entre soluciones es inmediata.
- La interfaz mantiene un rendimiento fluido con proyectos complejos.

---

## Relación con otras pantallas

- SCR-001 — Inicio.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- SCR-005 — Proyecto.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- vista múltiple de tableros;
- animación paso a paso de los algoritmos;
- edición manual asistida;
- colaboración en tiempo real;
- integración con asistentes de IA;
- panel de salud del proyecto.
