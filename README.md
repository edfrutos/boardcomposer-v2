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

## CSV de entrada

Columnas obligatorias:

    id,length_mm,width_mm,thickness_mm

Ejemplo:

    A,2000,300,20
    B,1000,300,20
    C,800,250,20
