# BoardComposer Studio

## SCR-001 — Pantalla de Inicio

**Código:** SCR-001
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

La pantalla de inicio constituye el punto de entrada a BoardComposer Studio. Debe permitir al usuario comenzar a trabajar en pocos segundos, recuperar proyectos recientes y acceder rápidamente a las funciones principales.

---

## Principios de diseño

- La pantalla debe transmitir claridad y profesionalidad.
- El usuario nunca debe sentirse perdido.
- Las acciones principales deben estar visibles sin desplazamiento.
- El acceso a un proyecto reciente debe requerir un solo clic.

---

## Distribución conceptual

```text
┌──────────────────────────────────────────────────────────────┐
│ BoardComposer Studio                                         │
├──────────────────────────────────────────────────────────────┤
│ Nuevo Proyecto                                               │
│ Abrir Proyecto                                               │
│ Importar CSV                                                 │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ Proyectos recientes                                          │
│                                                              │
│ • Proyecto Cocina.pdf                                        │
│ • Armario Dormitorio                                         │
│ • Oficina Cliente A                                          │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ Documentación │ Ejemplos │ Preferencias │ Novedades │ Ayuda  │
└──────────────────────────────────────────────────────────────┘
```

---

## Componentes

## Barra superior

- Nombre y versión del producto.
- Acceso al menú principal.
- Selector de tema (futuro).

## Acciones principales

- Nuevo proyecto.
- Abrir proyecto.
- Importar piezas desde CSV.

## Proyectos recientes

Lista cronológica con miniatura, nombre, fecha de modificación y acceso directo.

## Accesos secundarios

- Documentación.
- Ejemplos.
- Preferencias.
- Registro de novedades.
- Ayuda.

---

## Flujo principal

1. Abrir BoardComposer Studio.
2. Elegir un proyecto reciente o crear uno nuevo.
3. Acceder al Workspace (SCR-002).

---

## Criterios de aceptación

- Inicio en menos de cinco segundos.
- Navegación intuitiva.
- Todas las acciones principales visibles.
- Acceso a proyectos recientes con un clic.

---

## Relación con otras pantallas

- SCR-002 — Workspace.
- SCR-005 — Proyecto.
- SCR-006 — Preferencias.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- proyectos anclados;
- sincronización en la nube;
- plantillas de proyectos;
- panel de actividad reciente;
- búsqueda global.
