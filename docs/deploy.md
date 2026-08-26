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

### Claves de cliente y cuota mensual (planes de pago)

`BOARDCOMPOSER_API_KEY` sigue siendo una única clave compartida, sin cuota — pensada para uso interno/admin. Para vender acceso a la API por plan (`src/boardcomposer/billing.py`), añade además:

    docker run -d --name boardcomposer-api -p 5050:5050 \
      -e BOARDCOMPOSER_DB_PATH="/data/keys.db" \
      -e REDIS_URL="redis://redis:6379/0" \
      -v boardcomposer-data:/data \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

`BOARDCOMPOSER_DB_PATH` apunta a un SQLite (registro de claves por cliente, plan `free`/`basico`/`pro`, ver `PLAN_LIMITS` en `billing.py`) — necesita un volumen persistente, no vive dentro del contenedor. `REDIS_URL` es opcional pero recomendado en producción: sin él, el contador de cuota (y el rate limiter existente) es en memoria por proceso, no compartido entre workers de `gunicorn`.

Gestión de claves con `scripts/manage_keys.py` (dentro del contenedor o con el mismo `BOARDCOMPOSER_DB_PATH` montado):

    python scripts/manage_keys.py create taller-perez --plan pro
    python scripts/manage_keys.py list
    python scripts/manage_keys.py revoke bc_...

Los planes `free` se bloquean con `402` al agotar la cuota mensual; `basico`/`pro` siguen respondiendo por encima de su cuota.

### Cobro del overage con Stripe (`src/boardcomposer/stripe_billing.py`)

Opcional — sin configurar, el overage se acumula igual que antes pero no se cobra. Requiere **dos** Price por plan de pago en Stripe, no uno (`DT-0038`): un Price normal recurrente para la cuota fija mensual (`básico` 9€/mes, `pro` 29€/mes — sin metering, Stripe lo cobra solo cada periodo) y un Price **medido, sin tramos**, para el overage (`básico` 0,05€/unidad, `pro` 0,03€/unidad). Un único Price "graduado" con el corte en la cuota incluida (300/1500) no sirve: `report_overage()` solo reporta a Stripe las unidades que ya son overage, nunca las que están dentro de la cuota — así que el uso acumulado que ve Stripe en un mes nunca llega a cruzar un corte de tramo puesto en 300/1500, y el overage real quedaría sin cobrarse nunca.

    docker run -d --name boardcomposer-api -p 5050:5050 \
      -e BOARDCOMPOSER_DB_PATH="/data/keys.db" \
      -v boardcomposer-data:/data \
      -e STRIPE_SECRET_KEY="sk_live_..." \
      -e STRIPE_PRICE_BASICO="price_..." \
      -e STRIPE_PRICE_BASICO_OVERAGE="price_..." \
      -e STRIPE_PRICE_PRO="price_..." \
      -e STRIPE_PRICE_PRO_OVERAGE="price_..." \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Con estas variables presentes, `scripts/manage_keys.py create <cliente> --plan pro` crea también el Customer + una Subscription de **dos** ítems en Stripe (el de cuota fija se factura solo; guarda en `keys.db` el id del ítem de overage, aunque ya no se usa para facturar — ver abajo). El plan `free` nunca toca Stripe. Si falta cualquiera de las dos variables de un plan (base u overage), `stripe_billing.is_configured()` lo trata como no configurado del todo — nunca crea una suscripción a medias.

**Facturada por email, no con tarjeta automática** (`DT-0040`): un `Customer` recién creado no tiene ningún método de pago asociado, y `manage_keys.py` es una herramienta de admin para altas manuales, no un checkout — no hay ningún paso previo donde el cliente introduzca una tarjeta. `Subscription.create()` usa `collection_method="send_invoice"` (`days_until_due=15`): Stripe envía una factura por email cada periodo en vez de intentar cobrar automáticamente, algo que habría fallado sin una tarjeta ya asociada.

**El Price de overage necesita un *Meter* de Stripe** (`DT-0039`, cuentas nuevas de Stripe usan el sistema de "Billing Meters" — la API antigua de `SubscriptionItem.create_usage_record` ya no aplica a un Price basado en medidor). Antes de crear el Price de overage, crea el medidor en el Dashboard de Stripe (*Product catalog → Meters → Create meter*):

| | Básico | Pro |
|---|---|---|
| Event name (obligatorio, literal) | `boardcomposer_basico_overage` | `boardcomposer_pro_overage` |
| Método de agregación | Sum | Sum |

El `event_name` tiene que coincidir exactamente con `_METER_EVENT_NAMES` en `stripe_billing.py` — es una convención fija en el código, no una variable de entorno. Con el medidor creado, el formulario de precio deja elegirlo al marcar el Price como medido ("usage is metered"). Cada solve por encima de la cuota reporta un `Meter Event` (`stripe.billing.MeterEvent.create()`, keyed por el `stripe_customer_id`, no por el ítem de la suscripción — Stripe correlaciona solo con el `event_name`) — best-effort, un fallo de Stripe no rompe la petición del cliente, solo esa unidad de overage no se factura ese ciclo.

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
      -v boardcomposer-data:/data \
      -e BOARDCOMPOSER_DB_PATH="/data/keys.db" \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Si no vas a vender acceso por plan, omite `-v .../data` y `BOARDCOMPOSER_DB_PATH` — sin esas dos líneas la API funciona igual que antes de `IDE-0020`, solo con la clave única. **Si ya los usas** (planes `free`/`basico`/`pro`), no los omitas al reconstruir: sin `BOARDCOMPOSER_DB_PATH` el proceso arranca sin base de claves y toda clave de cliente que no sea la admin empieza a devolver `401` en vez de aplicar su cuota — la app arranca igual, sin avisar de que el billing quedó desactivado.

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
      -v boardcomposer-data:/data \
      -e BOARDCOMPOSER_DB_PATH="/data/keys.db" \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Si no vas a vender acceso por plan, omite `-v .../data` y `BOARDCOMPOSER_DB_PATH` — sin esas dos líneas la API funciona igual que antes de `IDE-0020`, solo con la clave única. **Si ya los usas** (planes `free`/`basico`/`pro`), no los omitas al reconstruir: sin `BOARDCOMPOSER_DB_PATH` el proceso arranca sin base de claves y toda clave de cliente que no sea la admin empieza a devolver `401` en vez de aplicar su cuota — la app arranca igual, sin avisar de que el billing quedó desactivado.

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
      -v boardcomposer-data:/data \
      -e BOARDCOMPOSER_DB_PATH="/data/keys.db" \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Si no vas a vender acceso por plan, omite `-v .../data` y `BOARDCOMPOSER_DB_PATH` — sin esas dos líneas la API funciona igual que antes de `IDE-0020`, solo con la clave única. **Si ya los usas** (planes `free`/`basico`/`pro`), no los omitas al reconstruir: sin `BOARDCOMPOSER_DB_PATH` el proceso arranca sin base de claves y toda clave de cliente que no sea la admin empieza a devolver `401` en vez de aplicar su cuota — la app arranca igual, sin avisar de que el billing quedó desactivado.

Puede arrancarse igualmente desde la propia extensión Docker de Plesk (*Docker* → *Ejecutar un contenedor* → imagen local `boardcomposer-api`) en vez de por SSH, configurando ahí el mismo mapeo de puerto y las mismas variables de entorno.

**4. Credenciales para el proxy** (`htpasswd`, por SSH — viene con el paquete `apache2-utils`/`httpd-tools` según la distro):

    htpasswd -c /etc/nginx/.htpasswd-bc tu-usuario

Pide la contraseña dos veces y la guarda ya hasheada (nunca en claro) en `/etc/nginx/.htpasswd-bc`. Con `-c` se crea el fichero desde cero — omite `-c` si ya existe y solo añades otro usuario.

**5. Proxy inverso hacia el contenedor, con autenticación HTTP Basic delante:** en el subdominio, *Configuración de Apache y nginx* → *Directivas adicionales de nginx*:

```nginx
location / {
    auth_basic "BoardComposer";
    auth_basic_user_file /etc/nginx/.htpasswd-bc;

    proxy_pass http://127.0.0.1:5050;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

`auth_basic` pide usuario/contraseña por HTTP (diálogo nativo del navegador o `curl -u`) antes de que la petición llegue siquiera a la API — funciona desde cualquier IP/red, a diferencia de un allowlist de IP (`DEC-0015`, `docs/masterplan/DOC-005-Decisiones.md`), que ataba el acceso a una única IP y se rompía en cuanto cambiabas de red o tu IP dinámica rotaba. No es un sistema de login/cuentas (eso se descartó en `DEC-0014` por desproporcionado) — es una credencial fija a nivel de servidor web, sin infraestructura nueva ni persistencia. Se suma a `BOARDCOMPOSER_API_KEY`, no la sustituye: quien pase el `auth_basic` sigue necesitando la clave de la API para cualquier ruta salvo `/health`.

Si quieres que un monitor de disponibilidad externo (UptimeRobot o similar) siga pudiendo comprobar `/health` sin credenciales, añade una excepción antes del bloque `location /` general:

```nginx
location = /health {
    proxy_pass http://127.0.0.1:5050;
}
```

**6. TLS:** *Certificados SSL/TLS* del subdominio → *Obtener gratis* (Let's Encrypt) — Plesk lo renueva solo, sin pasos manuales adicionales.

**7. Verificar:**

    curl -u tu-usuario:tu-contraseña https://bc.tu-dominio.com/health
    curl -u tu-usuario:tu-contraseña -H "X-API-Key: una-clave-secreta" https://bc.tu-dominio.com/strategies

**8. Actualizar tras un cambio de código:**

    cd boardcomposer && git pull
    docker build -t boardcomposer-api .
    docker stop boardcomposer-api && docker rm boardcomposer-api
    docker run --rm -v boardcomposer-data:/data alpine chown -R 1000:1000 /data
    docker run -d --name boardcomposer-api --restart unless-stopped \
      -p 127.0.0.1:5050:5050 \
      -v boardcomposer-data:/data \
      -e BOARDCOMPOSER_DB_PATH="/data/keys.db" \
      -e BOARDCOMPOSER_API_KEY="una-clave-secreta" \
      -e ANTHROPIC_API_KEY="sk-ant-..." \
      boardcomposer-api

Si no vas a vender acceso por plan, omite `-v .../data`, `BOARDCOMPOSER_DB_PATH` y el `chown` — sin esas líneas la API funciona igual que antes de `IDE-0020`, solo con la clave única. **Si ya los usas** (planes `free`/`basico`/`pro`), no los omitas al reconstruir: sin `BOARDCOMPOSER_DB_PATH` el proceso arranca sin base de claves y toda clave de cliente que no sea la admin empieza a devolver `401` en vez de aplicar su cuota — la app arranca igual, sin avisar de que el billing quedó desactivado.

**El paso `chown` es obligatorio si `boardcomposer-data` es un volumen nuevo o recién recreado** (`DT-0034`): la imagen corre como `appuser` (UID 1000, sin privilegios) y el `Dockerfile` solo hace `chown` de `/app`, nunca del punto de montaje de un volumen — Docker lo crea con propietario `root:root` por defecto. Sin este paso, `boardcomposer.billing.init_db()` falla con `sqlite3.OperationalError: unable to open database file` y el contenedor entra en bucle de reinicio (`docker logs boardcomposer-api` lo confirma). Si el volumen ya existía de una ejecución anterior con los permisos ya corregidos, el `chown` es idempotente — no hace daño repetirlo en cada actualización.

Uso personal/de un único usuario: con el `auth_basic` del paso 5 ya nadie sin la contraseña llega ni a `/health`, así que es la protección principal, y funciona desde cualquier red; mantener `BOARDCOMPOSER_API_KEY` definida además es defensa en profundidad barata (una segunda credencial independiente, a otro nivel — HTTP vs. aplicación). Con `ANTHROPIC_API_KEY` real (sin `MockAIProvider`), fijar un límite de gasto mensual en la propia consola de Anthropic — BoardComposer no impone ninguno.

**Verificado con un despliegue real (`IDE-0017`)**, no solo con `docker build`/`run` local: subdominio propio con SSL Let's Encrypt, contenedor corriendo en el VPS, proxy nginx conectado tras desactivar "Modo proxy" en Plesk, `/health` (`200`) y `/strategies` con clave (`200`, lista de estrategias) desde la IP permitida, `403` de nginx desde una IP fuera del `allow` (probado con datos móviles). Dos falsos positivos descartados durante el diagnóstico: Fail2Ban y el Web Application Firewall (mod_security) de Plesk, ambos desactivados para este dominio — el `403` inicial que parecía venir de uno de los dos resultó ser, una vez añadido `-v` a `curl`, simplemente la clave de ejemplo sin sustituir por la real. Protección migrada después de `allow`/`deny` por IP a `auth_basic` (`DEC-0015`) para no depender de una IP fija.

---

## Troubleshooting

- **El navegador/`curl` pide usuario y contraseña (`401` con cabecera `WWW-Authenticate`):** es el `auth_basic` del paso 5, no un fallo — introduce las credenciales de `.htpasswd-bc`. Con `curl`, añade `-u tu-usuario:tu-contraseña`.
- **`401` de nginx sin pedir credenciales / rechaza las que introduces:** revisa que `auth_basic_user_file` apunte al fichero correcto y que lo regeneraste con `htpasswd` (no editado a mano — el hash tiene que coincidir).
- **`401` en todas las rutas salvo `/health`, ya autenticado por `auth_basic`:** falta la cabecera `X-API-Key` o no coincide con `BOARDCOMPOSER_API_KEY`. Verificar con `curl -u usuario:contraseña -H "X-API-Key: ..." .../health` — `/health` siempre responde `200` independientemente de la clave (pero sigue pidiendo `auth_basic` salvo que hayas añadido la excepción del paso 5).
- **`429`:** límite de 60 peticiones/minuto por IP superado (`IDE-0009`). El almacenamiento del rate limiting es en memoria y no se comparte entre workers de `gunicorn` (`DT-0010`, `docs/masterplan/DOC-006-DeudaTecnica.md`) — con varios workers el límite real es mayor que 60/min.
- **`/assist/*` responde pero con explicaciones genéricas:** `ANTHROPIC_API_KEY` no está definida y la API cayó a `MockAIProvider`. Confirmar con `docker exec boardcomposer-api env | grep ANTHROPIC`.
