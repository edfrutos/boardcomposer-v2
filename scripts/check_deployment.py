#!/usr/bin/env python3
"""Guardrail against a stale production deployment (DT-0034 / DT-0035).

The VPS runs two independent containers — the API (`boardcomposer-api`) and
the browser Studio (`boardcomposer-studio-remote`) — each rebuilt by hand over
SSH, with no CI/CD. Twice in the project's life both drifted months behind
`main` (the API sat on `v0.3.9` for 27 releases) and it was only noticed by
explicitly checking. This script makes that check one command.

What it does:

  * Reads the expected version from `pyproject.toml` (override with --expect).
  * GETs `<api-url>/health` and compares its `version` field (added to the API
    for exactly this purpose) against the expected one.
  * Prints an explicit reminder about the Studio container, which has no
    HTTP-readable version — it must be rebuilt from the same tag, but this
    script cannot verify it.

Exit codes: 0 in sync, 1 drift detected, 2 could not check (network / usage).

Usage:

    python scripts/check_deployment.py
    python scripts/check_deployment.py --api-url https://bc.efjdefrutos.com \\
        --auth "$BC_DEPLOY_AUTH" --expect 0.3.42

`--auth` (or env BC_DEPLOY_AUTH) is `user:password` for the nginx HTTP Basic
in front of the API on the real VPS (`docs/deploy.md`, Opción C, paso 5).
`--api-url` also reads env BC_DEPLOY_API_URL. `/health` itself needs no API
key — it is exempt from `X-API-Key` (only the Basic auth sits in front of it).
"""

import argparse
import base64
import json
import os
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_API_URL = "https://bc.efjdefrutos.com"
STUDIO_CONTAINER = "boardcomposer-studio-remote"

EXIT_OK = 0
EXIT_DRIFT = 1
EXIT_CANNOT_CHECK = 2


def _fail(code: int, message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def _project_version() -> str:
    with Path("pyproject.toml").open("rb") as file:
        return tomllib.load(file)["project"]["version"]


def _fetch_health(api_url: str, auth: str | None, timeout: float) -> dict:
    request = urllib.request.Request(f"{api_url.rstrip('/')}/health")
    if auth:
        token = base64.b64encode(auth.encode()).decode()
        request.add_header("Authorization", f"Basic {token}")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode()
    except urllib.error.HTTPError as error:
        hint = " — revisa --auth / BC_DEPLOY_AUTH" if error.code in (401, 403) else ""
        _fail(EXIT_CANNOT_CHECK, f"{api_url}/health devolvió HTTP {error.code}{hint}")
    except (urllib.error.URLError, TimeoutError) as error:
        _fail(EXIT_CANNOT_CHECK, f"No se pudo alcanzar {api_url}/health: {error}")

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        _fail(
            EXIT_CANNOT_CHECK,
            f"/health no devolvió JSON (¿nginx/Plesk delante pidiendo "
            f"credenciales?): {body[:200]!r}",
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Comprueba que la API desplegada sirve la versión actual."
    )
    parser.add_argument(
        "--api-url",
        default=os.environ.get("BC_DEPLOY_API_URL", DEFAULT_API_URL),
        help=f"Base URL de la API desplegada (env BC_DEPLOY_API_URL; "
        f"por defecto {DEFAULT_API_URL}).",
    )
    parser.add_argument(
        "--auth",
        default=os.environ.get("BC_DEPLOY_AUTH"),
        help="usuario:contraseña del HTTP Basic de nginx (env BC_DEPLOY_AUTH).",
    )
    parser.add_argument(
        "--expect",
        default=None,
        help="Versión esperada (por defecto la de pyproject.toml).",
    )
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    expected = args.expect or _project_version()
    health = _fetch_health(args.api_url, args.auth, args.timeout)
    deployed = health.get("version")

    print(f"API  {args.api_url}")
    print(f"  esperada:   {expected}")
    print(f"  desplegada: {deployed or '(sin campo version)'}")

    if deployed is None:
        _fail(
            EXIT_DRIFT,
            "\nLa API desplegada no expone `version` en /health — es anterior a "
            "este guardarraíl, así que lleva sin reconstruirse desde antes de "
            "añadirlo. Reconstruye el contenedor (docs/deploy.md, Opción C, "
            "paso 8).",
        )

    if deployed != expected:
        _fail(
            EXIT_DRIFT,
            f"\nDESFASE: la API sirve {deployed}, la release actual es "
            f"{expected}. Reconstruye `boardcomposer-api` (docs/deploy.md, "
            f"Opción C, paso 8) — sin olvidar el `chown` del volumen (DT-0034).",
        )

    print(f"\nAPI en sync ({deployed}).")
    print(
        f"\nRecordatorio: el contenedor {STUDIO_CONTAINER} (Studio por "
        f"navegador, noVNC) no expone su versión por HTTP y este script NO "
        f"puede comprobarlo. Reconstrúyelo desde el mismo tag "
        f"(docs/deploy-studio-remote.md) y confírmalo a mano con "
        f'"Ayuda → Acerca de" — es justo el que se quedó atrás en DT-0035.'
    )


if __name__ == "__main__":
    main()
