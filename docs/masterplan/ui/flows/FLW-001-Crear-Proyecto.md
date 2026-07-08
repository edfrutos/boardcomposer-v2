# FLW-001 — Crear Proyecto

**Módulo:** BoardComposer Studio

**Código:** FLW-001
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

Describir el flujo completo para crear un nuevo proyecto en BoardComposer Studio, desde el acceso inicial hasta la apertura automática del Workspace preparado para comenzar a trabajar.

---

## Actor principal

- Usuario.

---

## Precondiciones

- BoardComposer Studio está iniciado.
- No existe ningún asistente modal bloqueando la interfaz.

---

## Flujo principal

1. El usuario accede a la pantalla de Inicio (SCR-001).
2. Selecciona **Nuevo proyecto**.
3. Studio abre el asistente de creación.
4. El usuario introduce los datos básicos del proyecto.
5. Studio valida la información.
6. Se crea el proyecto con un identificador único.
7. Se aplican las preferencias predeterminadas del usuario.
8. Se abre automáticamente el Workspace (SCR-002).
9. El proyecto queda listo para importar tableros y piezas.

---

## Flujo alternativo A — Cancelación

1. El usuario cancela el asistente.
2. No se crea ningún proyecto.
3. Studio vuelve a la pantalla de Inicio.

---

## Flujo alternativo B — Datos incompletos

1. Studio detecta campos obligatorios sin completar.
2. Resalta únicamente los campos afectados.
3. El usuario corrige la información.
4. Continúa el flujo principal.

---

## Datos mínimos

- Nombre del proyecto.
- Unidad de medida.
- Material principal (opcional en la primera versión).

---

## Resultado esperado

Se crea un proyecto válido, reproducible y preparado para recibir información adicional sin requerir configuraciones posteriores obligatorias.

---

## Eventos generados

- ProjectCreated
- WorkspaceOpened

---

## Criterios de aceptación

- Crear un proyecto en menos de un minuto.
- No solicitar información innecesaria.
- Validación inmediata de errores.
- Apertura automática del Workspace.

---

## Pantallas implicadas

- SCR-001 — Inicio.
- SCR-002 — Workspace.
- SCR-005 — Proyecto.

---

## Observaciones

En versiones futuras este flujo podrá ampliarse con asistentes, plantillas de proyecto, importación inicial de datos y creación basada en proyectos existentes, manteniendo siempre un recorrido simple para los nuevos usuarios.
