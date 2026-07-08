# ADR-012 — SelectionController

## Estado

Aceptada.

## Contexto

La selección de piezas está mezclada entre BoardWorkspace, MainWindow y SelectionManager. Esto dificulta evolucionar hacia multiselección, selección por ventana, Ctrl+Click, Shift+Click e Inspector sincronizado.

## Decisión

Se crea `SelectionController` como coordinador único de la selección en el Workspace.

## Responsabilidades

SelectionController será responsable de:

- seleccionar una pieza;
- seleccionar varias piezas;
- limpiar selección;
- sincronizar selección visual;
- sincronizar SelectionManager;
- preparar el Inspector para selección única o múltiple.

## No responsabilidades

BoardWorkspace no decidirá reglas de selección.

BoardPieceItem no conocerá SelectionManager.

MainWindow no manipulará directamente piezas gráficas.

## API prevista

```python
select(piece_id)
select_many(piece_ids)
clear()
current()
selected()
```

## Plan

1. Crear `studio/workspace/selection_controller.py`.
2. Migrar selección visual desde `BoardWorkspace`.
3. Mantener compatibilidad inicial con selección única.
4. Preparar API para multiselección.
5. Añadir tests posteriores.

## Resultado esperado

La selección queda centralizada y preparada para multiselección profesional.
