# BoardComposer

## Documento 999 — Ideas sin acotar

**Código:** DOC-999
**Estado:** En revisión
**Última revisión:** 15/07/2026

---

## Objetivo

Capturar ideas mencionadas en `docs/masterplan/DOC-003-Roadmap.md` que todavía no tienen alcance definido — para que existan candidatas concretas sobre las que decidir, sin comprometerlas al Backlog (`DOC-004`) hasta que se elija una y se acote de verdad.

---

## Marketplace / Biblioteca de materiales / Comunidad (Fase 5)

El sistema de plugins (`IDE-0008`) ya deja instalar generadores, estrategias, importadores/exportadores y paneles de Studio de terceros vía *entry points* de Python. Eso es la base técnica; "comunidad"/"marketplace" describe qué se construye encima, y hoy no hay nada decidido. Candidatas, de menor a mayor alcance:

- **Guía para desarrolladores de plugins** (`docs/plugins.md`): cómo crear y publicar un plugin (grupo de entry point, forma de la función, ejemplo mínimo end-to-end para cada uno de los 4 tipos). Sin esto, nadie fuera de este repo sabe que el mecanismo existe.
- **Visibilidad de los plugins instalados**: `generator_plugin_errors()`/`strategy_plugin_errors()`/`importer_plugin_errors()`/`exporter_plugin_errors()` ya existen en el Core, pero hoy no los consume nada salvo el equivalente de paneles en Studio (aviso en la barra de estado). No hay forma de ver, desde la CLI o la API, qué plugins están instalados o cuáles fallaron al cargar. Un comando `boardcomposer plugins` o una ruta `GET /plugins` sería el primer paso concreto y programable — sin visibilidad no hay ecosistema que gestionar.
- **Marketplace real** (sitio o índice público listando plugins de terceros): esto sí requiere infraestructura externa (hosting, moderación, proceso de publicación) y una decisión de producto previa — ¿quiere BoardComposer un ecosistema público de plugins de terceros, o el mecanismo de plugins es solo para uso interno/empresarial? Sin esa decisión no hay nada que programar todavía.

## Cloud (Fase 5 / Manifiesto)

`docs/masterplan/DOC-000-Manifiesto.md` menciona "Servicios Cloud" como una de las interfaces que el Core debería poder soportar — no describe un producto cloud concreto. Con `IDE-0009` (auth por clave, rate limiting, `gunicorn`) la API ya es desplegable; falta decidir qué significa "Cloud" aquí:

- **Guía/receta de despliegue** (Dockerfile + instrucciones para Fly.io/Railway/Render o un VPS con Caddy): lo más acotado y programable ya mismo, no requiere ninguna decisión de producto adicional.
- **Instancia demo pública**: la API (o Studio) desplegada en algún sitio con una clave de solo lectura, para que cualquiera la pruebe sin instalar nada. Acotado, pero implica mantener infraestructura corriendo y pagar por ella.
- **SaaS real** (proyectos persistentes por usuario, gestión de cuentas, autenticación real más allá de una clave compartida): salto arquitectónico grande — base de datos, modelo de usuarios, facturación. No es una tarea, es una fase nueva del producto; requiere decisión de producto antes de diseñar nada técnico.

---

## Cómo usar este documento

Ninguna de estas ideas pasa a `DOC-004-Backlog.md` como `IDE-XXXX` hasta que se elija una candidata concreta y se confirme su alcance (como se hizo con `IDE-0007` a `IDE-0012`). Mientras tanto, viven aquí.
