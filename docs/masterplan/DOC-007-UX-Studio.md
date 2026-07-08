


# BoardComposer

## Documento 7 — UX / BoardComposer Studio

**Código:** DOC-007
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 01/07/2026

---

## Objetivo

Definir la experiencia de usuario de BoardComposer Studio, estableciendo los principios de interacción, las pantallas principales y el flujo de trabajo que permitirá explorar, comparar y comprender soluciones de corte.

---

## Principios de diseño

- La interfaz debe ser visual antes que textual.
- Toda acción importante debe tener una representación gráfica.
- El usuario explora soluciones; no ejecuta un proceso opaco.
- La información debe organizarse por contexto, evitando la sobrecarga visual.
- La experiencia debe ser consistente en futuras versiones de escritorio, web y otras plataformas.

---

## Flujo principal del usuario

1. Crear o abrir un proyecto.
2. Importar piezas y tableros.
3. Configurar restricciones y algoritmos.
4. Explorar soluciones generadas.
5. Comparar alternativas.
6. Inspeccionar cada solución.
7. Exportar el resultado.

---

## Pantallas previstas

### SCR-001 — Inicio
Acceso a proyectos recientes, creación de proyectos y documentación.

### SCR-002 — Workspace
Área principal con la representación gráfica de los tableros y las piezas.

### SCR-003 — Comparador
Vista simultánea de varias soluciones con métricas comparables.

### SCR-004 — Inspector
Información detallada del proyecto, tablero, pieza o solución seleccionada.

### SCR-005 — Configuración
Preferencias, estrategias, algoritmos y opciones avanzadas.

---

## Distribución conceptual

```text
┌───────────────────────────────────────────────────────┐
│ Barra superior                                        │
├───────────────┬─────────────────────────────┬─────────┤
│ Explorador    │ Workspace                   │Inspector│
│ de proyecto   │                             │         │
├───────────────┴─────────────────────────────┴─────────┤
│ Comparador · Consola · Métricas · Eventos             │
└───────────────────────────────────────────────────────┘
```

---

## Principios de interacción

- Selección directa sobre el tablero.
- Arrastrar y soltar cuando tenga sentido.
- Comparación visual inmediata.
- Explicaciones accesibles sin abandonar el Workspace.
- Navegación fluida entre soluciones.

---

## Objetivos de la experiencia

El usuario debe ser capaz de:

- comprender una solución en pocos segundos;
- detectar diferencias entre algoritmos;
- localizar rápidamente cualquier pieza;
- confiar en el resultado gracias a explicaciones claras;
- trabajar durante horas sin fatiga visual.

---

## Evolución prevista

Versiones futuras incorporarán:

- animación del proceso de colocación;
- colaboración en tiempo real;
- asistencia mediante IA;
- panel de salud del proyecto;
- personalización avanzada del espacio de trabajo.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- diseñar wireframes de cada pantalla;
- definir el sistema de diseño visual;
- establecer componentes reutilizables;
- convertir esta especificación en la guía oficial de UX de BoardComposer Studio.