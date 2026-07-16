# BoardComposer

[![wakatime](https://wakatime.com/badge/user/16c6559b-16d0-48b5-be12-d8e02abcd889/project/73e7ddb3-1eec-4acf-bf1b-8b955ac705cc.svg)](https://wakatime.com/badge/user/16c6559b-16d0-48b5-be12-d8e02abcd889/project/73e7ddb3-1eec-4acf-bf1b-8b955ac705cc)

Motor 2D para generar composiciones de tablas a partir de medidas dadas.

## Estado actual

- Python 3.13
- Core: varios algoritmos de layout (skyline, MaxRects, beam search, permutaciones), puntuación y explicación de soluciones, exportación SVG/DXF
- CLI: entrada CSV/Excel, salida texto/JSON
- API HTTP (`/solve`, `/strategies`, `/assist/*`) con autenticación por clave y rate limiting opcionales, servidor WSGI de producción (`gunicorn`)
- BoardComposer Studio (GUI PySide6): workspace interactivo, comparador, inspector, gestión de proyectos, exportación SVG/PDF, empaquetado como `.app` de macOS
- Asistente IA (proveedor real conectado: Anthropic Claude)
- Sistema de plugins: generadores, estrategias, importadores/exportadores y paneles de Studio de terceros — ver `docs/plugins.md`
- Tests automatizados (300+)

Ver `docs/masterplan/DOC-004-Backlog.md` para el estado vivo, funcionalidad por funcionalidad.

## Instalación

    python3.13 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

## Comandos

    make test
    make check
    make demo
    make json

## API en producción

Por defecto (`make run`/`python -m boardcomposer.api`) la API usa el servidor de desarrollo de Flask — solo para uso local. Para producción:

    pip install -e ".[prod]"
    export BOARDCOMPOSER_API_KEY="una-clave-secreta"
    make serve

`make serve` arranca `gunicorn` sobre `boardcomposer.api:create_app()`. Con `BOARDCOMPOSER_API_KEY` configurada, todas las rutas salvo `/health` exigen esa clave en la cabecera `X-API-Key`; sin ella, no hay autenticación (igual que antes). Todas las rutas están además limitadas a 60 peticiones/minuto por IP (`/health` exenta).

## BoardComposer Studio

Interfaz gráfica (PySide6). En desarrollo:

    make studio

o directamente `boardcomposer-studio` una vez instalado el paquete.

### Empaquetado como aplicación de macOS

    pip install -e ".[package]"
    make package

Genera `studio/dist/BoardComposerStudio.app` (con `pyside6-deploy`, sin firmar ni notarizar por Apple — Gatekeeper avisará de "desarrollador no identificado" al primer arranque). Al crear un tag `v*` en GitHub, `.github/workflows/package-studio.yml` compila el `.app` y lo publica automáticamente como asset de una release.

## CSV/Excel de entrada

Columnas obligatorias (mismas en `--csv` y `--excel`):

    id,length_mm,width_mm,thickness_mm

Ejemplo:

    A,2000,300,20
    B,1000,300,20
    C,800,250,20
