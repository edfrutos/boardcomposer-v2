# BoardComposer desde la terminal

Referencia de uso de `boardcomposer`, la línea de comandos del Core
(`src/boardcomposer/cli.py`). Para la interfaz gráfica ver `docs/studio.md`;
para el servicio HTTP, `docs/deploy.md` y `docs/masterplan/DOC-008-API.md`.

## Instalación

    python3.13 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

Eso deja disponibles dos ejecutables: `boardcomposer` (esta referencia) y
`boardcomposer-studio` (la aplicación de escritorio).

## Uso

    boardcomposer [--csv RUTA | --excel RUTA]
                  [--max-length MM] [--max-width MM]
                  [--allow-rotation] [--strategy NOMBRE]
                  [--top N] [--json]

    boardcomposer plugins [--json]

Sin ningún argumento se resuelve un proyecto de demostración incorporado (dos
tablas, `A` de 2000×300×20 mm y `B` de 1000×300×20 mm), útil para comprobar que
la instalación funciona:

    boardcomposer

## Opciones

| Opción | Valor | Por defecto | Qué hace |
|---|---|---|---|
| `--csv` | ruta | — | Lee las tablas de un CSV. Excluyente con `--excel`. |
| `--excel` | ruta a `.xlsx` | — | Lee las tablas de la primera hoja de un Excel. Excluyente con `--csv`. |
| `--max-length` | mm | sin límite | Largo máximo de la composición resultante. |
| `--max-width` | mm | sin límite | Ancho máximo de la composición resultante. |
| `--allow-rotation` | — | desactivado | Permite girar las tablas 90° al colocarlas. |
| `--strategy` | `balanced`, `material`, `compact` | `balanced` | Conjunto de generadores y pesos de puntuación (`docs/scoring.md`). |
| `--top` | entero | `5` | Número máximo de soluciones a incluir. **Solo afecta a `--json`**: la salida de texto muestra siempre la mejor. |
| `--json` | — | desactivado | Salida JSON en vez de texto. |

Las restricciones (`--max-length`, `--max-width`, `--allow-rotation`) se aplican
igual venga el proyecto de un fichero o de la demo. Todo valor numérico debe ser
finito: `NaN` e `Infinity` se rechazan con un error, no se cuelan hasta el
solver.

## Formato del fichero de entrada

Mismas columnas obligatorias en CSV y en Excel. La primera fila es la cabecera.

| Columna | Obligatoria | Contenido |
|---|---|---|
| `length_mm` | sí | Largo en mm (número positivo y finito). |
| `width_mm` | sí | Ancho en mm. |
| `thickness_mm` | sí | Grosor en mm. |
| `id` | no | Identificador de la tabla. Si falta o va vacío, se genera uno. |
| `quantity` | no | Solo CSV (`IDE-0038`). Entero ≥ 1; una fila con `quantity` > 1 se expande a esa cantidad de tablas idénticas. Con `id`, los ids derivados llevan sufijo (`A`, `A-2`, `A-3`...); sin `id`, todas las tablas resultantes quedan sin id. Ausente o vacía, equivale a `quantity=1`. |
| `material` | no | Solo CSV (`IDE-0038`). Etiqueta libre, sin efecto en el solver — el Core empaqueta las tablas sobre una única lámina, así que no hay varias tablas entre las que elegir por material. Se guarda y se puede leer luego desde `Board.material`. |

Cualquier otra columna se ignora. `quantity` y `material` no están soportadas en Excel, solo en CSV.

    id,length_mm,width_mm,thickness_mm
    A,2000,300,20
    B,1000,300,20
    C,800,250,20

Hay un fichero de ejemplo de cada tipo en `data/samples/`
(`basic_boards.csv`, `basic_boards.xlsx`).

> El importador de piezas de Studio (menú Archivo → "Importar piezas (CSV)…")
> usa las mismas columnas pero **sí exige `id`**, porque necesita un
> identificador estable para referenciar cada pieza en el proyecto.

## Salida

### Texto (por defecto)

Resumen de la mejor solución encontrada:

    $ boardcomposer --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600
    BoardComposer
    Tablas entrada: 3
    Soluciones válidas: 1
    Tablas colocadas: 3
    Largo total: 3000.0 mm
    Ancho total: 550.0 mm
    Puntuación: 70.33333333333333
    Layout: free_space

Si ninguna candidata cumple las restricciones, imprime `No hay soluciones
válidas.` y termina con código 0 — no es un error, es que no cabe.

### JSON (`--json`)

Mismo contenido que devuelve el endpoint `/solve` de la API: parámetros de
entrada, pesos de puntuación, mejor solución y hasta `--top` soluciones con la
posición de cada tabla (`board_id`, `x_mm`, `y_mm`, `length_mm`, `width_mm`,
`rotated`).

    $ boardcomposer --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600 --json --top 2
    {
      "input_boards": 3,
      "strategy": "balanced",
      "generators": ["horizontal", "vertical", "free_space"],
      "top": 2,
      "weights": { "material_utilization": 40.0, ... },
      "best_solution": { "score": 70.33, "placed_boards": 3, ... },
      "solutions": [ { "placements": [ ... ] } ]
    }

Es la forma prevista de encadenar BoardComposer con otras herramientas:

    boardcomposer --csv piezas.csv --json | jq '.best_solution.score'

## Subcomando `plugins`

Lista los plugins de terceros instalados por *entry point*, agrupados por tipo,
y los que fallan al cargarse (prefijados con `!`). Misma fuente que `GET
/plugins` en la API. Ver `docs/plugins.md` para escribir uno.

    $ boardcomposer plugins
    generators:
      (ninguno instalado)
    strategies:
      (ninguno instalado)
    importers:
      (ninguno instalado)
    exporters:
      (ninguno instalado)

Con `--json` devuelve la misma información en JSON. Los paneles de Studio no
aparecen aquí: solo tienen sentido dentro de la aplicación de escritorio.

## Errores y código de salida

| Situación | Salida | Código |
|---|---|---|
| Todo correcto | resultado en stdout | 0 |
| Sin soluciones válidas | `No hay soluciones válidas.` | 0 |
| Fichero con una fila inválida | `Error al leer el fichero de entrada: Fila 3: could not convert string to float: 'abc'` | 1 |
| Falta una columna obligatoria | `Error al leer el fichero de entrada: Faltan columnas obligatorias en el CSV: width_mm` | 1 |
| Fichero inexistente o ilegible | `No se pudo abrir el fichero de entrada: [Errno 2] ...` | 1 |
| `--csv` y `--excel` a la vez | error de `argparse` | 2 |

Los mensajes de fila cuentan la cabecera como fila 1, así que el número
coincide con el que muestra el editor o la hoja de cálculo.

## Atajos del Makefile

    make demo     # boardcomposer sobre data/samples/basic_boards.csv, salida de texto
    make json     # lo mismo con --json
    make run      # boardcomposer sin argumentos (proyecto de demostración)
    make studio   # boardcomposer-studio (interfaz gráfica)
    make test     # pytest
    make check    # scripts/check_project.py + ruff check + pytest
