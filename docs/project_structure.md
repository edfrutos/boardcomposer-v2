# Estructura del proyecto

> **Superado.** Snapshot del primer día del proyecto (26/06/2026): no
> menciona `studio/`, `src/boardcomposer/api.py`, `ai/`, `plugins/`,
> `export/`, `presenters/` ni nada construido después. La estructura real y
> mantenida está en `docs/architecture.md`. Se conserva aquí como registro
> histórico.

## Raíz

- `pyproject.toml`: configuración Python.
- `Makefile`: comandos frecuentes.
- `README.md`: descripción general.
- `TODO.md`: tareas pendientes.
- `CHANGELOG.md`: historial de cambios.

## Código

- `src/boardcomposer/domain/`: modelos principales.
- `src/boardcomposer/layout/`: geometría y colocación.
- `src/boardcomposer/solver/`: generación, validación y evaluación.
- `src/boardcomposer/io/`: entrada/salida de datos.
- `src/boardcomposer/cli.py`: interfaz de línea de comandos.

## Pruebas

- `tests/`: tests unitarios.

## Datos

- `data/samples/`: CSV de ejemplo.

## Scripts

- `scripts/check_project.py`: validación básica del proyecto.
