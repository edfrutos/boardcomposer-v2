# ADR-013 — Geometry Engine

## Estado

Aceptada.

## Contexto

BoardComposer Studio ya permite mover, rotar y eliminar piezas, pero la lógica geométrica aún depende parcialmente de elementos gráficos de Qt.

Esto no es suficiente para la evolución del proyecto, porque el futuro motor de optimización no trabajará con una escena gráfica, sino con modelos, tableros y rectángulos lógicos.

## Decisión

Toda la geometría de BoardComposer se centralizará en `PlacementValidator`.

`PlacementValidator` será la fuente única de verdad para:

- límites del tablero;
- rectángulos lógicos de piezas;
- colisiones;
- rotaciones;
- validación de colocaciones;
- futuras reglas de snap;
- futuras reglas de nesting.

## Regla principal

Ninguna clase fuera de `PlacementValidator` debe decidir si una pieza cabe, colisiona, puede moverse o puede rotarse.

## Responsabilidades

`PlacementValidator` deberá evolucionar hacia una API estable:

```python
piece_rect(...)
rotated_rect(...)
overlaps(...)
collides(...)
can_place(...)
can_rotate(...)
constrain_position(...)
