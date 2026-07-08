
# DECISIONS - BoardComposer

## 2026-06-26 - Ensamblaje 2D

Se decide comenzar con ensamblaje plano 2D de tablas rectangulares.

Motivo: reduce la complejidad y permite validar el motor antes de añadir interfaz gráfica o algoritmos avanzados.

## 2026-06-26 - Núcleo independiente

El núcleo no dependerá de PySide6, ficherosos ni IA.

Motivo: debe poder probarse desde consola y con tests unitarios.

## 2026-06-26 - Soluciones explicables

Cada solución deberá incluir puntuación y explicación.

Motivo: el usuario debe entender por qué una composición es mejor que otra.

