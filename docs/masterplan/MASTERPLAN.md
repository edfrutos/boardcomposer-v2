# BoardComposer — MASTERPLAN

## Estado actual

Rama: `feat/skyline-multinode`

Último bloque consolidado:
- Workspace modular
- CommandManager
- MovePieceCommand
- RotatePieceCommand
- PlacementValidator
- ADR-010
- ADR-011
- ADR-012

## Bloque en curso

### Bloque 2 — SelectionController

Objetivo:
Centralizar toda la selección del Workspace.

Estado:
- ADR-012 creado
- Pendiente implementación

## Próxima tarea única

Crear:

`studio/workspace/selection_controller.py`

## Criterio de finalización del bloque

- Selección centralizada
- BoardWorkspace sin lógica directa de selección
- Inspector sincronizado
- Ruff limpio
- App ejecuta sin errores
- Commit realizado

## Normas de trabajo

1. No añadir funcionalidad sin bloque definido.
2. No lógica geométrica en MainWindow.
3. No reglas de colocación fuera de PlacementValidator.
4. No comandos dependientes de Qt.
5. Ruff limpio antes de cada commit.
6. Commit al cerrar cada bloque.
7. Antes de cada commit:
   - ejecutar `ruff check`;
   - ejecutar `ruff check --fix`;
   - volver a ejecutar `ruff check`;
   - ejecutar la aplicación;
   - comprobar manualmente la funcionalidad afectada;
   - revisar `git status`..