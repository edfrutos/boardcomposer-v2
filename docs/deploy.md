# Despliegue de la API (Cloud)

Receta de despliegue para la API HTTP de BoardComposer (`src/boardcomposer/api.py`), ya lista para producción desde `IDE-0009` (autenticación por clave, rate limiting, `gunicorn`). Cierra el punto "Cloud" de `DOC-003-Roadmap.md` (`IDE-0014`, `DEC-0012`, `docs/masterplan/DOC-005-Decisiones.md`). La Opción C, a diferencia de A y B, está verificada contra un despliegue real y en marcha (`IDE-0017`, `DEC-0014`), no solo documentada.

**Fuera de alcance:** BoardComposer Studio (aplicación de escritorio PySide6, `IDE-0011` cubre su propio empaquetado como `.app` de macOS) no forma parte de este despliegue. La Opción C cubre una instancia personal/de un único usuario en un VPS propio; un SaaS real con cuentas de usuario o una instancia demo abierta al público en general siguen sin acotar — ver las candidatas restantes en `docs/masterplan/DOC-999-Ideas.md`.

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

## Opción C — VPS con Plesk (extensión Docker)

Para un VPS con panel Plesk (con la extensión Docker habilitada) en vez de Caddy manual — Plesk gestiona el dominio, el proxy inverso y el certificado TLS (Let's Encrypt) desde su propia interfaz.

**1. Crear el subdominio en Plesk:** *Dominios* → *Añadir subdominio* → `bc.tu-dominio.com`. No hace falta contenido web propio; solo sirve como punto de entrada hacia el contenedor.

**2. Construir la imagen en el servidor** (por SSH — la extensión Docker de Plesk corre imágenes ya construidas, pero no compila un `Dockerfile` desde la UI):

    git clone <url-del-repo> boardcomposer
    cd boardcomposer
    docker build -t boardcomposer-api .

**3. Arrancar el contenedor**, escuchando solo en loopback (Plesk es el único punto de entrada público, igual que Caddy en la Opción B):

    docker run -d --name boardcomposer-api --restart unless-stopped \
      -p 127.0.0.1:5050:5050 \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Puede arrancarse igualmente desde la propia extensión Docker de Plesk (*Docker* → *Ejecutar un contenedor* → imagen local `boardcomposer-api`) en vez de por SSH, configurando ahí el mismo mapeo de puerto y las mismas variables de entorno.

**4. Proxy inverso hacia el contenedor:** en el subdominio, *Configuración de Apache y nginx* → *Directivas adicionales de nginx*:

```nginx
location / {
    allow 203.0.113.10;   # tu IP pública — averíguala con curl ifconfig.me
    deny all;

    proxy_pass http://127.0.0.1:5050;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Restringe el subdominio por IP en vez de (o además de) confiar solo en `BOARDCOMPOSER_API_KEY`: cualquiera fuera de la lista `allow` recibe un `403` de nginx antes de que la petición llegue siquiera a la API — la clave nunca es alcanzable desde otra IP, aunque se filtre. Añade una línea `allow` por cada IP/red que necesite acceso (formato CIDR, p. ej. `allow 203.0.113.0/24;`). Limitación a tener en cuenta: si tu IP pública es dinámica (típico en una conexión doméstica), cambiará tarde o temprano y te dejará fuera hasta que actualices la regla — para una IP estable sin depender de tu operador, una VPN propia (p. ej. WireGuard en el mismo VPS) es la alternativa más robusta, permitiendo el `allow` solo sobre la IP interna de la VPN.

**5. TLS:** *Certificados SSL/TLS* del subdominio → *Obtener gratis* (Let's Encrypt) — Plesk lo renueva solo, sin pasos manuales adicionales.

**6. Verificar:**

    curl https://bc.tu-dominio.com/health
    curl -H "X-API-Key: una-clave-secreta" https://bc.tu-dominio.com/strategies

**7. Actualizar tras un cambio de código:**

    cd boardcomposer && git pull
    docker build -t boardcomposer-api .
    docker stop boardcomposer-api && docker rm boardcomposer-api
    docker run -d --name boardcomposer-api --restart unless-stopped \
      -p 127.0.0.1:5050:5050 \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Uso personal/de un único usuario: con el `allow`/`deny` del paso 4 ya nadie fuera de tu IP llega ni a `/health`, así que es la protección principal; mantener `BOARDCOMPOSER_API_KEY` definida además es defensa en profundidad barata (si algún día compartes acceso con más IPs en la allowlist). Con `ANTHROPIC_API_KEY` real (sin `MockAIProvider`), fijar un límite de gasto mensual en la propia consola de Anthropic — BoardComposer no impone ninguno.

**Verificado con un despliegue real (`IDE-0017`)**, no solo con `docker build`/`run` local: subdominio propio con SSL Let's Encrypt, contenedor corriendo en el VPS, proxy nginx conectado tras desactivar "Modo proxy" en Plesk, `/health` (`200`) y `/strategies` con clave (`200`, lista de estrategias) desde la IP permitida, `403` de nginx desde una IP fuera del `allow` (probado con datos móviles). Dos falsos positivos descartados durante el diagnóstico: Fail2Ban y el Web Application Firewall (mod_security) de Plesk, ambos desactivados para este dominio — el `403` inicial que parecía venir de uno de los dos resultó ser, una vez añadido `-v` a `curl`, simplemente la clave de ejemplo sin sustituir por la real.

---

## Troubleshooting

- **`403` de nginx en cualquier ruta, incluida `/health` (solo Opción C con IP allowlist):** tu IP pública no está en la regla `allow` del subdominio (o ha cambiado, si es dinámica). Comprueba tu IP actual con `curl ifconfig.me` y actualiza la directiva nginx en Plesk.
- **`401` en todas las rutas salvo `/health`:** falta la cabecera `X-API-Key` o no coincide con `BOARDCOMPOSER_API_KEY`. Verificar con `curl -H "X-API-Key: ..." .../health` — `/health` siempre responde `200` independientemente de la clave.
- **`429`:** límite de 60 peticiones/minuto por IP superado (`IDE-0009`). El almacenamiento del rate limiting es en memoria y no se comparte entre workers de `gunicorn` (`DT-0010`, `docs/masterplan/DOC-006-DeudaTecnica.md`) — con varios workers el límite real es mayor que 60/min.
- **`/assist/*` responde pero con explicaciones genéricas:** `ANTHROPIC_API_KEY` no está definida y la API cayó a `MockAIProvider`. Confirmar con `docker exec boardcomposer-api env | grep ANTHROPIC`.
