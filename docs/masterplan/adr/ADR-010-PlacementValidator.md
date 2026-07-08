# ADR-010 — PlacementValidator como fuente única de validación

## Estado

Aceptada.

## Contexto

El Workspace de BoardComposer ha evolucionado desde una prueba visual hacia un editor CAD básico. Actualmente existen validaciones repartidas entre:

- BoardWorkspace
- collision.py
- constraints.py
- MainWindow
- comandos de movimiento/rotación

Esto provoca riesgo de incoherencias: una pieza puede moverse con unas reglas y rotarse con otras.

## Decisión

Se crea `PlacementValidator` como única fuente de verdad para validar colocaciones.

Será responsable de:

- comprobar límites del tablero;
- detectar colisiones entre piezas;
- validar movimientos;
- validar rotaciones;
- centralizar futuras reglas de nesting, separación, márgenes y kerf.

## Consecuencias

BoardWorkspace dejará de decidir reglas de validez.

MainWindow no contendrá lógica geométrica.

Los comandos consultarán reglas coherentes.

Las futuras operaciones piar, pegar, importar y optimizar— usarán el mismo criterio.

## Plan de migración

1. Crear `studio/workspace/placement_validator.py`.
2. Mover allí lógica de colisiones y límites.
3. Hacer que BoardWorkspace use PlacementValidator.
4. Hacer que la rotación use PlacementValidator.
5. Eliminar lógica duplicada o dispersa.
6. Validar con Ruff y prueba manual.
