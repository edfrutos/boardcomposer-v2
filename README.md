# BoardComposer

[![wakatime](https://wakatime.com/badge/user/16c6559b-16d0-48b5-be12-d8e02abcd889/project/73e7ddb3-1eec-4acf-bf1b-8b955ac705cc.svg)](https://wakatime.com/badge/user/16c6559b-16d0-48b5-be12-d8e02abcd889/project/73e7ddb3-1eec-4acf-bf1b-8b955ac705cc)

Motor 2D para generar composiciones de tablas a partir de medidas dadas.

## Estado actual

- Python 3.13
- Core: varios algoritmos de layout (skyline, MaxRects, beam search, permutaciones), puntuación y explicación de soluciones, exportación SVG/DXF
- CLI: entrada CSV/Excel, salida texto/JSON, subcomando `plugins` — referencia completa en `docs/cli.md`
- API HTTP (`/solve`, `/strategies`, `/assist/*`, `/plugins`) con autenticación por clave y rate limiting opcionales, servidor WSGI de producción (`gunicorn`)
- BoardComposer Studio (GUI PySide6): workspace interactivo multi-tablero, alta y edición de tableros y piezas, importación de piezas desde CSV, comparador, inspector, exportación SVG/PDF/DXF, empaquetado como `.app` de macOS
- Asistente IA (proveedor real conectado: Anthropic Claude)
- Sistema de plugins: generadores, estrategias, importadores/exportadores y paneles de Studio de terceros — ver `docs/plugins.md`
- Tests automatizados (673)

Ver `docs/masterplan/DOC-004-Backlog.md` para el estado vivo, funcionalidad por funcionalidad, y `docs/masterplan/INDEX.md` como índice de toda la documentación.

## Instalación

    python3.13 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

## Comandos

    make test
    make check
    make demo
    make json

## Uso desde la terminal

    boardcomposer --csv piezas.csv --max-length 3000 --max-width 600
    boardcomposer --excel piezas.xlsx --strategy compact --allow-rotation
    boardcomposer --csv piezas.csv --json --top 3
    boardcomposer plugins

Referencia completa de opciones, formato de entrada, salida JSON, mensajes de
error y códigos de salida: **`docs/cli.md`**.

## API en producción

Por defecto (`make run`/`python -m boardcomposer.api`) la API usa el servidor de desarrollo de Flask — solo para uso local. Para producción:

    pip install -e ".[prod]"
    export BOARDCOMPOSER_API_KEY="una-clave-secreta"
    make serve

`make serve` arranca `gunicorn` sobre `boardcomposer.api:create_app()`. Con `BOARDCOMPOSER_API_KEY` configurada, todas las rutas salvo `/health` exigen esa clave en la cabecera `X-API-Key`; sin ella, no hay autenticación (igual que antes). Todas las rutas están además limitadas a 60 peticiones/minuto por IP (`/health` exenta).

### Despliegue en la nube

    docker build -t boardcomposer-api .
    docker run -d -p 5050:5050 -e BOARDCOMPOSER_API_KEY="..." boardcomposer-api

Ver `docs/deploy.md` para Fly.io o un VPS con Caddy.

## BoardComposer Studio

Interfaz gráfica (PySide6). En desarrollo:

    make studio

o directamente `boardcomposer-studio` una vez instalado el paquete.

### Empaquetado como aplicación de macOS

    pip install -e ".[package]"
    make package

Genera `studio/dist/BoardComposerStudio.app` (con `pyside6-deploy`). Al crear un tag `v*` en GitHub, `.github/workflows/package-studio.yml` compila el `.app` y lo publica automáticamente como asset de una release.

Las releases actuales **no van firmadas con un certificado de Apple**, así que macOS avisa la primera vez que se abre una descargada — no una compilada en local, que nunca pasa por la cuarentena del navegador. Instrucciones para quien la descargue: **`docs/INSTALL-macos.md`**, que acompaña al `.zip` en cada release.

El workflow ya sabe firmar y notarizar (`scripts/sign_and_notarize.sh`); solo espera a que existan los secrets de una cuenta de Apple Developer, y entonces lo hace sin cambiar nada más (`DEC-0017`, `DT-0011`). Un certificado autofirmado no sirve: Gatekeeper solo confía en los emitidos por Apple.

## CSV/Excel de entrada

Columnas obligatorias (mismas en `--csv` y `--excel`): `length_mm`,
`width_mm`, `thickness_mm`. La columna `id` es opcional — si falta, se genera
un identificador. El importador de piezas de Studio usa el mismo formato pero
sí exige `id`.

    id,length_mm,width_mm,thickness_mm
    A,2000,300,20
    B,1000,300,20
    C,800,250,20

Ficheros de ejemplo en `data/samples/`. Detalle en `docs/cli.md`.
