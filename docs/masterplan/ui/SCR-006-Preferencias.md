# SCR-006 — Preferencias

**Módulo:** BoardComposer Studio

**Código:** SCR-006
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

La pantalla de Preferencias permite personalizar el comportamiento general de BoardComposer Studio sin modificar la configuración específica de ningún proyecto.

Las preferencias representan el entorno de trabajo habitual del usuario y se aplican automáticamente a todos los proyectos, salvo que estos definan explícitamente un comportamiento diferente.

---

## Filosofía

Las preferencias pertenecen al usuario.

Los proyectos pertenecen al trabajo.

Esta separación garantiza que un proyecto pueda compartirse entre distintos usuarios sin alterar sus configuraciones personales.

---

## Distribución conceptual

```text
┌────────────────────────────────────────────────────────────────────┐
│ Preferencias                                                      │
├────────────────────┬───────────────────────────────────────────────┤
│ General            │ Idioma                                       │
│                    │ Tema                                         │
│                    │ Unidades                                     │
├────────────────────┼───────────────────────────────────────────────┤
│ Workspace          │ Zoom                                         │
│                    │ Cuadrícula                                   │
│                    │ Guías                                        │
├────────────────────┼───────────────────────────────────────────────┤
│ Algoritmos         │ Valores por defecto                          │
│                    │ Beam Width                                   │
│                    │ Rotación                                     │
├────────────────────┼───────────────────────────────────────────────┤
│ Exportación        │ PDF                                          │
│                    │ SVG                                          │
│                    │ DXF                                          │
├────────────────────┼───────────────────────────────────────────────┤
│ Avanzado           │ Caché                                        │
│                    │ Logs                                         │
│                    │ Desarrollo                                   │
└────────────────────┴───────────────────────────────────────────────┘
```

---

## Componentes principales

### General

- Idioma.
- Tema claro / oscuro.
- Sistema de unidades.
- Formato de fechas.
- Formato numérico.

### Workspace

- Nivel de zoom inicial.
- Mostrar cuadrícula.
- Mostrar reglas.
- Mostrar cotas.
- Mostrar vetas.
- Mostrar desperdicio.
- Mostrar etiquetas.

### Algoritmos

- Algoritmo preferido.
- Beam Width por defecto.
- Rotación permitida.
- Estrategia de evaluación.
- Número máximo de soluciones.

### Exportación

- Formato preferido.
- Carpeta por defecto.
- Calidad de imágenes.
- Incluir métricas.
- Incluir explicación.
- Plantillas de exportación.

### Rendimiento

- Uso máximo de memoria.
- Número de hilos.
- Caché de soluciones.
- Precálculo.
- Optimización automática.

### Desarrollo

- Registro de eventos.
- Consola avanzada.
- Información de depuración.
- Estadísticas internas.
- Funciones experimentales.

---

## Flujo principal

1. Abrir Preferencias.
2. Modificar la configuración.
3. Aplicar cambios.
4. Guardar automáticamente.
5. Refrescar únicamente los elementos afectados.

---

## Principios de interacción

- Cambios inmediatos cuando sea posible.
- Vista previa antes de aplicar cambios visuales.
- Restaurar valores por defecto.
- Búsqueda global de preferencias.
- Organización por categorías.

---

## Criterios de aceptación

- Localizar cualquier preferencia en menos de diez segundos.
- No mezclar preferencias con configuración del proyecto.
- Sin necesidad de reiniciar Studio tras la mayoría de cambios.
- Preferencias sincronizables en futuras versiones.

---

## Relación con otras pantallas

- SCR-001 — Inicio.
- SCR-002 — Workspace.
- SCR-005 — Proyecto.
- SCR-007 — Exportación.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- perfiles de usuario;
- sincronización en la nube;
- importación y exportación de preferencias;
- preferencias por espacio de trabajo;
- personalización completa de paneles;
- temas desarrollados por la comunidad.

---

## Nota de diseño

Las preferencias deberán almacenarse de forma independiente a los proyectos y ser compatibles entre versiones de BoardComposer Studio.

En el futuro podrán asociarse a una cuenta de usuario para sincronizar automáticamente la configuración entre distintos equipos.
