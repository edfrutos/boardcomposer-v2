# BoardComposer Studio por navegador (escritorio remoto)

Receta para acceder a la interfaz visual de BoardComposer Studio (`studio/`, aplicación de escritorio PySide6) desde el navegador, a través de un subdominio propio — sin reescribir la aplicación. `docs/deploy.md` cubre la API HTTP; este documento es su complemento para la interfaz visual, y ambos son despliegues independientes.

**Cómo funciona:** Studio corre exactamente igual que en local, pero dentro de una pantalla X11 virtual (`Xvfb`, sin monitor/GPU real) en el VPS. Un servidor VNC (`x11vnc`) captura esa pantalla, y `noVNC`/`websockify` la sirve como página web (HTML5 canvas sobre websockets) — el navegador se conecta a esa página y ve/controla la ventana de Studio como si fuera un escritorio remoto. No hay ningún puerto ni reescritura de la interfaz: es el mismo código de `studio/app.py`.

**Limitación importante:** esto es una sesión de escritorio remoto, no una aplicación web nativa — se siente como tal (la ventana entera viaja como imagen, sin diseño responsive) y solo admite un usuario a la vez sobre el mismo proyecto abierto. Para varios usuarios simultáneos con proyectos independientes haría falta un contenedor por sesión, fuera de alcance aquí.

---

## La imagen

`Dockerfile.studio` (raíz del repo): `python:3.13-slim` + `Xvfb`/`fluxbox`/`x11vnc`/`novnc`/`websockify` + las librerías de runtime que Qt necesita para pintar por software (sin GPU). Instala `boardcomposer` sin el extra `[prod]` (no hace falta `gunicorn` aquí), y arranca como usuario sin privilegios (`appuser`). Expone el puerto `6080` (noVNC).

`docker/studio-entrypoint.sh`: genera la contraseña de VNC a partir de `VNC_PASSWORD` (obligatoria, sin valor por defecto), arranca `Xvfb` + `fluxbox` + `boardcomposer-studio` + `x11vnc` + `websockify`, y sale si cualquiera de los tres procesos principales muere (para que `--restart unless-stopped` reinicie el contenedor entero en vez de dejarlo a medias).

### Build y prueba local

    docker build -f Dockerfile.studio -t boardcomposer-studio-remote .
    docker run -d --name boardcomposer-studio-remote -p 6080:6080 \
      -e VNC_PASSWORD="una-contraseña-de-vnc" \
      boardcomposer-studio-remote

Abre `http://localhost:6080/vnc.html` en el navegador, introduce la contraseña de VNC, y deberías ver la ventana de Studio arrancando.

**Verificado con una build y un arranque reales** (no solo revisión del `Dockerfile`): imagen construida, contenedor levantado, y la interfaz completa de Studio (Explorer, lienzo con piezas, toolbar, Asistente) confirmada por captura real a través de `noVNC` en el navegador. Un fallo real detectado y corregido en el proceso: Qt necesita `libxcb-xkb1` además de `libxcb-cursor0` para cargar el plugin `xcb` — el mensaje de error de Qt apunta genéricamente a `libxcb-cursor0` aunque la causa real sea otra librería `xcb-*` ausente; si el contenedor no arranca, revisa los logs (`docker logs`) para la línea `cannot open shared object file`, no solo el mensaje genérico de Qt.

---

## Despliegue — VPS con Plesk (extensión Docker)

Mismo patrón que la Opción C de `docs/deploy.md`, con un subdominio propio (p. ej. `studio.tu-dominio.com`) y su propio contenedor.

**1. Crear el subdominio en Plesk:** *Dominios* → *Añadir subdominio* → `studio.tu-dominio.com`.

**2. Construir la imagen en el servidor** (por SSH, fuera del docroot de Plesk — ver `docs/deploy.md` Opción C sobre por qué):

    cd /root/boardcomposer   # el mismo checkout usado para la API
    git pull
    docker build -f Dockerfile.studio -t boardcomposer-studio-remote .

**3. Arrancar el contenedor**, escuchando solo en loopback:

    docker run -d --name boardcomposer-studio-remote --restart unless-stopped \
      -p 127.0.0.1:6080:6080 \
      -e VNC_PASSWORD="una-contraseña-de-vnc" \
      boardcomposer-studio-remote

**4. Proxy inverso en Plesk**, con el mismo allowlist de IP que la API (`docs/deploy.md`, `DEC-0014`) — noVNC usa websockets, así que hacen falta las cabeceras de actualización de protocolo además del `proxy_pass` habitual:

```nginx
location / {
    allow TU.IP.PUBLICA.AQUI;
    deny all;

    proxy_pass http://127.0.0.1:6080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 3600s;
}
```

(`proxy_read_timeout` alto porque una sesión VNC es una conexión larga y persistente, no una petición HTTP puntual — el valor por defecto de nginx la cortaría a los pocos segundos de inactividad.)

**5. TLS:** *Certificados SSL/TLS* del subdominio → *Obtener gratis* (Let's Encrypt), igual que en la Opción C de `docs/deploy.md`.

**6. Verificar:** abre `https://studio.tu-dominio.com/vnc.html`, introduce la contraseña de VNC, y confirma que ves la ventana de Studio.

**7. Actualizar tras un cambio de código:**

    cd /root/boardcomposer && git pull
    docker build -f Dockerfile.studio -t boardcomposer-studio-remote .
    docker stop boardcomposer-studio-remote && docker rm boardcomposer-studio-remote
    docker run -d --name boardcomposer-studio-remote --restart unless-stopped \
      -p 127.0.0.1:6080:6080 \
      -e VNC_PASSWORD="una-contraseña-de-vnc" \
      boardcomposer-studio-remote

---

## Troubleshooting

- **La página de noVNC carga pero no conecta / se queda "Connecting…":** casi siempre faltan las cabeceras `Upgrade`/`Connection` del paso 4 — sin ellas nginx no deja pasar el handshake de websocket. Revisa las directivas adicionales de nginx.
- **Se desconecta tras un rato de inactividad:** `proxy_read_timeout` demasiado bajo (por defecto de nginx, unos 60s). Confirma que está el valor alto del paso 4.
- **`403` de nginx:** tu IP no está en el `allow` o ha cambiado — mismo troubleshooting que en `docs/deploy.md` (Opción C).
- **Contraseña de VNC rechazada:** `VNC_PASSWORD` se fija al arrancar el contenedor (`docker run -e VNC_PASSWORD=...`) — si la cambias, hay que recrear el contenedor (parar, quitar, volver a arrancar con el nuevo valor), no basta con reiniciarlo.
- **Rendimiento lento/tirones:** esperable en escritorio remoto sobre una conexión doméstica — noVNC no está pensado para animaciones fluidas, solo para uso puntual de la interfaz.
