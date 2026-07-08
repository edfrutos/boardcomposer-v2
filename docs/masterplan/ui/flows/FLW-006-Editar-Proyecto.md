# FLW-006 — Editar Proyecto

**Módulo:** BoardComposer Studio

**Código:** FLW-006
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

Describir el flujo mediante el cual el usuario modifica un proyecto existente, manteniendo la coherencia de la información, la trazabilidad de los cambios y la reproducibilidad de las soluciones generadas.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Existe un proyecto abierto.
- El usuario dispone de permisos para modificarlo.

---

## Flujo principal

1. El usuario abre un proyecto existente.
2. Accede a la pantalla SCR-005 — Proyecto o modifica elementos desde el Workspace.
3. Realiza los cambios necesarios (materiales, piezas, tableros, restricciones o parámetros).
4. Studio valida automáticamente las modificaciones.
5. Los cambios quedan registrados en el historial del proyecto.
6. Si las modificaciones afectan a las soluciones existentes, Studio las marca como "pendientes de regeneración".
7. El usuario guarda el proyecto o continúa trabajando.

---

## Flujo alternativo A — Cambios no válidos

1. Studio detecta inconsistencias.
2. Informa de los elementos afectados.
3. El usuario corrige los datos antes de continuar.

---

## Flujo alternativo B — Descartar cambios

1. El usuario cancela la edición.
2. Studio ofrece conservar o descartar las modificaciones no guardadas.
3. El proyecto recupera el último estado confirmado si así se solicita.

---

## Validaciones

- Coherencia de dimensiones.
- Restricciones compatibles.
- Materiales existentes.
- Integridad de referencias.
- Consistencia entre piezas y tableros.

---

## Eventos generados

- ProjectModified
- ProjectValidated
- ProjectSaved
- SolutionsMarkedOutdated
- ProjectHistoryUpdated

---

## Resultado esperado

El proyecto refleja los cambios realizados manteniendo su integridad y permitiendo regenerar las soluciones cuando sea necesario.

---

## Criterios de aceptación

- Validación inmediata de cambios.
- Historial completo de modificaciones.
- Posibilidad de deshacer cambios en futuras versiones.
- Detección automática de soluciones obsoletas.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-004 — Inspector.
- SCR-005 — Proyecto.

---

## Observaciones

En futuras versiones este flujo incorporará control de versiones del proyecto, diferencias visuales entre revisiones, edición colaborativa, bloqueo de recursos durante la edición, recuperación automática tras fallos y un sistema de deshacer/rehacer ilimitado basado en el historial de eventos.

Asimismo, cada modificación significativa podrá registrarse como una revisión identificable, facilitando auditorías, comparaciones entre estados del proyecto y reproducción exacta de cualquier versión anterior.
