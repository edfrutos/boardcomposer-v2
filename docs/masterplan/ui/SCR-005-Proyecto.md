# SCR-005 — Gestión del Proyecto

**Módulo:** BoardComposer Studio

**Código:** SCR-005
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

La pantalla de Proyecto centraliza toda la información general del trabajo en curso. Desde ella el usuario define los datos básicos, materiales, restricciones y configuración antes de generar o revisar soluciones.

---

## Filosofía

Un proyecto debe ser una unidad de trabajo completa y reproducible. Cualquier usuario deberá poder abrir un proyecto meses después y obtener exactamente el mismo contexto, configuración y resultados.

---

## Distribución conceptual

```text
┌──────────────────────────────────────────────────────────────┐
│ Proyecto                                                     │
├───────────────────────┬──────────────────────────────────────┤
│ Información general   │ Nombre                               │
│                       │ Cliente                              │
│                       │ Descripción                          │
├───────────────────────┼──────────────────────────────────────┤
│ Materiales            │ Tableros │ Espesores │ Vetas         │
├───────────────────────┼──────────────────────────────────────┤
│ Restricciones         │ Giro │ Márgenes │ Cortes │ Kerf      │
├───────────────────────┼──────────────────────────────────────┤
│ Algoritmos            │ Skyline │ MaxRects │ Beam            │
├───────────────────────┴──────────────────────────────────────┤
│ Resumen del proyecto                                     │
└──────────────────────────────────────────────────────────────┘
```

---

## Componentes principales

### Información general

- Nombre del proyecto.
- Cliente.
- Referencia.
- Descripción.
- Fecha de creación y modificación.

### Materiales

- Catálogo de tableros.
- Espesores.
- Dirección de veta.
- Material principal y alternativos.

### Restricciones

- Permitir rotación.
- Ancho del corte (kerf).
- Márgenes de seguridad.
- Restricciones de orientación.
- Restricciones definidas por el usuario.

### Algoritmos disponibles

- Selección de algoritmos.
- Parámetros específicos.
- Estrategia de evaluación.
- Número máximo de soluciones.

### Resumen

Vista consolidada con las características principales del proyecto y un diagnóstico rápido antes de iniciar la optimización.

---

## Flujo principal

1. Crear un nuevo proyecto.
2. Definir materiales y tableros.
3. Importar piezas.
4. Configurar restricciones.
5. Seleccionar algoritmos.
6. Guardar.
7. Abrir el Workspace para generar soluciones.

---

## Principios de interacción

- Validación inmediata de datos.
- Guardado automático configurable.
- Cambios siempre reversibles.
- Configuración organizada por bloques temáticos.
- Resumen permanente del estado del proyecto.

---

## Criterios de aceptación

- Crear un proyecto completo sin abandonar la pantalla.
- Detectar configuraciones incompletas o inconsistentes.
- Acceder al Workspace con un solo clic.
- Mantener la trazabilidad de todos los cambios.

---

## Relación con otras pantallas

- SCR-001 — Inicio.
- SCR-002 — Workspace.
- SCR-006 — Preferencias.
- SCR-007 — Exportación.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- plantillas de proyecto;
- historial completo de cambios;
- versiones y revisiones del proyecto;
- sincronización en la nube;
- colaboración multiusuario;
- firma digital y auditoría de proyectos.
