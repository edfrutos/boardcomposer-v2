# Despliegue de la API (Cloud)

Receta de despliegue para la API HTTP de BoardComposer (`src/boardcomposer/api.py`), ya lista para producción desde `IDE-0009` (autenticación por clave, rate limiting, `gunicorn`). Cierra el punto "Cloud" de `DOC-003-Roadmap.md` (`IDE-0014`, `DEC-0012`, `docs/masterplan/DOC-005-Decisiones.md`).

**Fuera de alcance:** BoardComposer Studio (aplicación de escritorio PySide6, `IDE-0011` cubre su propio empaquetado como `.app` de macOS) no forma parte de este despliegue. Tampoco una instancia demo pública mantenida ni un SaaS real con cuentas de usuario — ver las candidatas sin acotar en `docs/masterplan/DOC-999-Ideas.md`.

---

## La imagen

`Dockerfile` en la raíz del repo: `python:3.13-slim`, instala `boardcomposer` con el extra `[prod]` (incluye `gunicorn`), copia `src/` y `studio/` (el paquete declara ambos en `[tool.setuptools.packages.find]`, aunque solo `src/boardcomposer` se ejecuta aquí), y arranca como usuario sin privilegios (`appuser`, no root). Expone el puerto `5050`.

Aviso de tamaño: `pyside6` es una dependencia obligatoria del paquete `boardcomposer` (no opcional, por el diseño actual de `pyproject.toml`), así que la imagen la instala igualmente aunque la API nunca la importe — la imagen resultante ronda 1-1.3 GB. Reducirlo requeriría separar `pyside6` a un extra propio de Studio en `pyproject.toml`, un cambio de empaquetado fuera del alcance de esta receta.

### Build y prueba local

    docker build -t boardcomposer-api .
    docker run -d --name boardcomposer-api -p 5050:5050 \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

    curl http://localhost:5050/health
    curl -H "X-API-Key: una-clave-secreta" http://localhost:5050/strategies

Verificado con una build y arranque reales (no solo revisión del `Dockerfile`): `/health` responde sin clave, `/strategies` rechaza sin clave o con clave incorrecta (`401`), acepta con la clave correcta, `/solve` devuelve una solución real, y los logs de `gunicorn` confirman que corre como `appuser` (no root).

Sin `BOARDCOMPOSER_API_KEY`, la API queda sin autenticación (mismo comportamiento que en local, `IDE-0009`) — no se recomienda para un despliegue expuesto a Internet. Sin `ANTHROPIC_API_KEY`, `/assist/*` sigue funcionando pero con `MockAIProvider` en vez de respuestas reales de Claude (`default_provider()`, `docs/masterplan/DOC-004-Backlog.md`).

---

## Opción A — Fly.io (PaaS, recomendada)

Fly.io construye directamente desde el `Dockerfile` del repo, sin registro de imágenes propio que mantener.

    curl -L https://fly.io/install.sh | sh   # instala flyctl
    fly auth login
    fly launch --dockerfile Dockerfile --no-deploy

`fly launch` detecta el `Dockerfile`, pregunta el nombre de la app y la región, y genera un `fly.toml`. Edítalo para que el puerto interno coincida con el `EXPOSE 5050` de la imagen:

```toml
[http_service]
  internal_port = 5050
  force_https = true
```

Configura los secretos (nunca en `fly.toml`, que se versiona):

    fly secrets set BOARDCOMPOSER_API_KEY="una-clave-secreta"
    fly secrets set ANTHROPIC_API_KEY="sk-ant-..."

Despliega:

    fly deploy

`fly.toml` puede añadir un healthcheck sobre `/health` (la única ruta que `IDE-0009` deja sin autenticación):

```toml
[[http_service.checks]]
  path = "/health"
  method = "GET"
  interval = "15s"
  timeout = "5s"
```

---

## Opción B — VPS + Caddy

Para un VPS propio (cualquier proveedor), con `docker` instalado y Caddy como proxy inverso — Caddy gestiona el certificado TLS automáticamente vía Let's Encrypt, sin configuración manual de certificados.

**1. Arrancar el contenedor en el VPS**, escuchando solo en loopback (Caddy es el único punto de entrada público):

    docker run -d --name boardcomposer-api --restart unless-stopped \
      -p 127.0.0.1:5050:5050 \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

**2. `Caddyfile`** (`/etc/caddy/Caddyfile`):

```
api.tu-dominio.com {
    reverse_proxy localhost:5050
}
```

Caddy obtiene y renueva el certificado TLS automáticamente al arrancar (`systemctl reload caddy` tras editar el `Caddyfile`) — no requiere ningún paso adicional para HTTPS.

**3. Actualizar tras un cambio de código:**

    git pull
    docker build -t boardcomposer-api .
    docker stop boardcomposer-api && docker rm boardcomposer-api
    docker run -d --name boardcomposer-api --restart unless-stopped \
      -p 127.0.0.1:5050:5050 \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

---

## Troubleshooting

- **`401` en todas las rutas salvo `/health`:** falta la cabecera `X-API-Key` o no coincide con `BOARDCOMPOSER_API_KEY`. Verificar con `curl -H "X-API-Key: ..." .../health` — `/health` siempre responde `200` independientemente de la clave.
- **`429`:** límite de 60 peticiones/minuto por IP superado (`IDE-0009`). El almacenamiento del rate limiting es en memoria y no se comparte entre workers de `gunicorn` (`DT-0010`, `docs/masterplan/DOC-006-DeudaTecnica.md`) — con varios workers el límite real es mayor que 60/min.
- **`/assist/*` responde pero con explicaciones genéricas:** `ANTHROPIC_API_KEY` no está definida y la API cayó a `MockAIProvider`. Confirmar con `docker exec boardcomposer-api env | grep ANTHROPIC`.
