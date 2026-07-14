# BoardComposer

[![wakatime](https://wakatime.com/badge/user/16c6559b-16d0-48b5-be12-d8e02abcd889/project/73e7ddb3-1eec-4acf-bf1b-8b955ac705cc.svg)](https://wakatime.com/badge/user/16c6559b-16d0-48b5-be12-d8e02abcd889/project/73e7ddb3-1eec-4acf-bf1b-8b955ac705cc)

Motor 2D para generar composiciones de tablas a partir de medidas dadas.

## Estado actual

- Python 3.13
- CLI funcional
- Entrada CSV
- Salida texto y JSON
- Solver geométrico inicial
- Layout free-space inicial
- Tests automatizados

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

## CSV de entrada

Columnas obligatorias:

    id,length_mm,width_mm,thickness_mm

Ejemplo:

    A,2000,300,20
    B,1000,300,20
    C,800,250,20
