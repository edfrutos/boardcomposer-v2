# ADR-011 — Blueprint del Workspace

## Estado

Aceptada.

## Objetivo

Definir la arquitectura estable del Workspace de BoardComposer Studio para evitar lógica dispersa y crecimiento desordenado.

## Principio rector

El Workspace debe comportarse como un editor CAD: cada responsabilidad debe vivir en un componente claro, sin duplicidades.

## Componentes

### MainWindow

Responsabilidad:

- construir menús;
- coordinar paneles;
- mostrar estado;
- invocar acciones de usuario.

No debe contener:

- geometría;
- colisiones;
- límites de tablero;
- reglas de colocación.

### BoardWorkspace

Responsabilidad:

- contener la escena Qt;
- recibir eventos de usuario;
- coordinar piezas, tablero, cámara, comandos y validación.

No debe contener:

- reglas geométricas complejas;
- lógica de negocio duplicada;
- validaciones que pertenezcan al dominio.

### BoardPieceItem

Responsabilidad:

- representar gráficamente una pieza;
- cambiar color visual;
- informar al Workspace de cambios de posición.

No debe conocer:

- proyecto;
- tablero;
- comandos;
- MainWindow.

### WorkspaceCamera

Responsabilidad:

- zoom;
- límites de zoom;
- centro de cámara.

### DragController

Responsabilidad:

- recordar inicio de arrastre;
- limpiar estado de arrastre;
- preparar futuras operaciones de drag.

### PlacementValidator

Responsabilidad:

- límites del tablero;
- colisiones;
- movimiento válido;
- rotación válida;
- futuras reglas de nesting.

Debe ser la única fuente de verdad para validar colocaciones.

### Factories

Responsabilidad:

- crear elementos gráficos a partir del modelo.

Archivos:

- board_item.py
- piece_factory.py

## Dependencias permitidas

MainWindow
→ BoardWorkspace
→ BoardPieceItem
→ PlacementValidator
→ WorkspaceCamera
→ DragController
→ Factories

## Dependencias prohibidas

BoardPieceItem no puede depender de MainWindow.

BoardPieceItem no puede depender del modelo de proyecto.

MainWindow no puede validar geometría.

Los comandos no deben depender de Qt.

Las reglas de colocación no deben duplicarse en varias clases.

## Regla de oro

Toda decisión sobre si una pieza cabe, colisiona, puede moverse o puede rotarse debe pasar por PlacementValidator.

## Plan de aplicación

1. Consolidar PlacementValidator.
2. Eliminar `collision.py` una vez absorbido por `PlacementValidator`.
3. Eliminar `constraints.py` una vez absorbido por `PlacementValidator`.
4. Hacer que rotación consulte PlacementValidator.
5. Hacer que movimiento consulte PlacementValidator.
6. Mantener MainWindow libre de geometría.
7. Añadir tests unitarios para PlacementValidator.

## Resultado esperado

Un Workspace modular, mantenible y preparado para:

- rotación;
- snap;
- multiselección;
- copiar/pegar;
- nesting;
- exportación.
