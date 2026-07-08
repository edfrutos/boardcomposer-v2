# FLW-002 — Importar CSV

**Módulo:** BoardComposer Studio

**Código:** FLW-002
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

Describir el flujo completo para importar piezas desde un archivo CSV, validando su contenido antes de incorporarlo al proyecto y garantizando la trazabilidad del proceso.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Existe un proyecto abierto.
- El usuario dispone de un archivo CSV compatible.

---

## Flujo principal

1. El usuario selecciona **Importar CSV**.
2. Studio abre el selector de archivos.
3. Se elige el archivo CSV.
4. Studio analiza automáticamente su estructura.
5. Se muestra una vista previa de los datos.
6. El usuario confirma la importación.
7. Las piezas se incorporan al proyecto.
8. El Workspace se actualiza automáticamente.

---

## Flujo alternativo A — Archivo inválido

1. El formato no puede interpretarse.
2. Studio informa del problema indicando la causa.
3. El usuario puede seleccionar otro archivo.

---

## Flujo alternativo B — Errores en los datos

1. Se detectan filas con errores.
2. Studio resalta únicamente las filas afectadas.
3. El usuario decide continuar, corregir o cancelar.

---

## Validaciones

- Cabeceras reconocidas.
- Campos obligatorios presentes.
- Valores numéricos válidos.
- Dimensiones positivas.
- Referencias duplicadas.
- Compatibilidad con la unidad del proyecto.

---

## Resultado esperado

Las piezas válidas quedan incorporadas al proyecto sin alterar la información existente y con un registro completo de la operación.

---

## Eventos generados

- CsvImported
- PiecesValidated
- PiecesAdded
- WorkspaceUpdated

---

## Criterios de aceptación

- Vista previa antes de importar.
- Mensajes de error claros y accionables.
- Posibilidad de cancelar en cualquier momento.
- Importación reproducible y registrada.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-005 — Proyecto.

---

## Observaciones

En futuras versiones se admitirán asistentes de mapeo de columnas, plantillas de importación, compatibilidad con Excel y formatos de terceros, así como reglas de validación configurables por el usuario.
