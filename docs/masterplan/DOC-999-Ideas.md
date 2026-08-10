# BoardComposer

## Documento 999 — Ideas sin acotar

**Código:** DOC-999
**Estado:** En revisión
**Última revisión:** 03/08/2026

---

## Objetivo

Capturar ideas mencionadas en `docs/masterplan/DOC-003-Roadmap.md` que todavía no tienen alcance definido — para que existan candidatas concretas sobre las que decidir, sin comprometerlas al Backlog (`DOC-004`) hasta que se elija una y se acote de verdad.

---

## Marketplace / Biblioteca de materiales / Comunidad (Fase 5)

El sistema de plugins (`IDE-0008`) ya deja instalar generadores, estrategias, importadores/exportadores y paneles de Studio de terceros vía *entry points* de Python. Eso es la base técnica; "comunidad"/"marketplace" describe qué se construye encima, y hoy no hay nada decidido. Candidatas, de menor a mayor alcance:

- **Guía para desarrolladores de plugins** (`docs/plugins.md`): cómo crear y publicar un plugin (grupo de entry point, forma de la función, ejemplo mínimo end-to-end para cada uno de los 4 tipos). Sin esto, nadie fuera de este repo sabe que el mecanismo existe. **Promovida a `IDE-0013`** (`DEC-0011`, `docs/masterplan/DOC-004-Backlog.md`).
- **Visibilidad de los plugins instalados**: `generator_plugin_errors()`/`strategy_plugin_errors()`/`importer_plugin_errors()`/`exporter_plugin_errors()` ya existen en el Core, pero hoy no los consume nada salvo el equivalente de paneles en Studio (aviso en la barra de estado). No hay forma de ver, desde la CLI o la API, qué plugins están instalados o cuáles fallaron al cargar. Un comando `boardcomposer plugins` o una ruta `GET /plugins` sería el primer paso concreto y programable — sin visibilidad no hay ecosistema que gestionar. **Promovida a `IDE-0015`** (`DEC-0013`, `docs/masterplan/DOC-004-Backlog.md`).
- **Marketplace real** (sitio o índice público listando plugins de terceros): esto sí requiere infraestructura externa (hosting, moderación, proceso de publicación) y una decisión de producto previa — ¿quiere BoardComposer un ecosistema público de plugins de terceros, o el mecanismo de plugins es solo para uso interno/empresarial? Sin esa decisión no hay nada que programar todavía.

## Cloud (Fase 5 / Manifiesto)

`docs/masterplan/DOC-000-Manifiesto.md` menciona "Servicios Cloud" como una de las interfaces que el Core debería poder soportar — no describe un producto cloud concreto. Con `IDE-0009` (auth por clave, rate limiting, `gunicorn`) la API ya es desplegable; falta decidir qué significa "Cloud" aquí:

- **Guía/receta de despliegue** (Dockerfile + instrucciones para Fly.io/Railway/Render o un VPS con Caddy): lo más acotado y programable ya mismo, no requiere ninguna decisión de producto adicional. **Promovida a `IDE-0014`** (`DEC-0012`, `docs/masterplan/DOC-004-Backlog.md`); ampliada con una tercera opción (VPS con Plesk) en **`IDE-0017`** (`DEC-0014`).
- **Instancia demo pública**: la API (o Studio) desplegada en algún sitio con una clave de solo lectura, para que cualquiera la pruebe sin instalar nada. Acotado, pero implica mantener infraestructura corriendo y pagar por ella. Sigue sin acotar — no confundir con `IDE-0017`, que es una instancia **privada** de un único usuario (protegida por allowlist de IP, sin acceso abierto al público).
- **SaaS real** (proyectos persistentes por usuario, gestión de cuentas, autenticación real más allá de una clave compartida): salto arquitectónico grande — base de datos, modelo de usuarios, facturación. Sigue sin acotar como fase completa.
- **Modelo híbrido — Studio gratis + API de pago**: decisión de producto tomada el 31/07/2026 (`DEC-0018`, `docs/masterplan/DOC-005-Decisiones.md`) sin esperar al SaaS completo — autenticación por clave ya existía (`IDE-0009`), solo faltaba ligarla a un plan con cuota. **Promovida a `IDE-0020`** (claves de API por cliente con cuota mensual, `src/boardcomposer/billing.py`) e **`IDE-0021`** (cobro de overage con Stripe, `src/boardcomposer/stripe_billing.py`), ambas en `main` desde `v0.3.3`, `docs/masterplan/DOC-004-Backlog.md`.

---

## Aprovechamiento de retales de tablero (Fase 5 / Sostenibilidad)

Idea planteada por el usuario el 03/08/2026, todavía sin acotar: aprovechar restos de tablero de construcciones anteriores (recortes de corte, no tablero nuevo) en vez de descartarlos. Dos candidatas distintas dentro del mismo tema, de menor a mayor alcance — no se promueven a `IDE-XXXX` hasta elegir alcance concreto con el usuario, mismo criterio que el resto de este documento.

### Candidata 1 — Ajustar piezas contra un inventario de retales, antes de tablero nuevo

**Inicio.** Hoy `Project.boards` (`src/boardcomposer/domain/project.py`) es una lista de `Board` (`src/boardcomposer/domain/board.py`) sin distinguir procedencia — un tablero nuevo estándar y un resto de otra obra son, para el dominio, exactamente lo mismo: largo/ancho/grosor/material. El solver (`GeometrySolver`/generadores) ya coloca piezas dentro de cualquier `Board` que se le pase, sea cual sea su origen — no hace falta tocar el solver para que una pieza encaje en un retal si el retal se da de alta como un `Board` más.

**Proceso.** Lo que falta de verdad, no lo que ya existe:

1. **Inventario persistente de retales** — hoy `Project.boards` vive solo dentro de un proyecto, sin ningún almacén de "restos disponibles" que sobreviva entre proyectos distintos. Haría falta un registro nuevo (mismo patrón SQLite que ya usa `billing.py`, `IDE-0020`) con id/dimensiones/material/grosor/procedencia por retal, marcado como consumido al usarse en un proyecto.
2. **Retales no rectangulares** — un recorte real puede no ser un rectángulo perfecto (una L, una esquina cortada). El dominio actual (`Board`, `BoardPlacement`) asume rectángulos; soportar formas irregulares es un cambio de modelo geométrico grande, fuera de alcance salvo que se acote explícitamente a "solo retales rectangulares" como primer corte.
3. **Prioridad de asignación** — decidir con el usuario si el solver debe preferir agotar el inventario de retales antes de proponer tablero nuevo, o si es una elección manual en Studio ("usar retal X en vez de tablero nuevo").

**Consecución.** Acotada con el usuario el 03/08/2026 al alcance más barato: solo alta manual (sin inventario persistente) y elección manual en Studio (sin priorización automática del solver). Con ese alcance **ya está cubierta por el modelo actual** — sin código nuevo que construir (`DEC-0019`, `docs/masterplan/DOC-005-Decisiones.md`). Documentada como guía de uso, `docs/retales-como-tablero.md`. El inventario persistente (punto 1) **promovido a `IDE-0039`** el 09/08/2026 (`docs/masterplan/DOC-004-Backlog.md`). La priorización automática (punto 3) queda como posible ampliación futura, sin acotar, si el uso real lo pide.

### Candidata 2 — Diseño paramétrico de contenedores (caja/cajón/cajonera/estantería) a partir de un retal

**Inicio.** Distinto del punto anterior: no se trata de encajar piezas que el usuario ya definió, sino de generar automáticamente el despiece de un mueble de almacenaje (caja, cajón, cajonera de N cajones, estantería de N baldas) que quepa dentro de las dimensiones de un retal disponible, para darle utilidad de guardado de útiles.

**Proceso.** No encaja en el dominio actual en absoluto — BoardComposer coloca piezas ya definidas (a mano, CSV, Excel), no genera piezas nuevas a partir de un diseño de mueble. Haría falta:

1. Un catálogo de "tipos de contenedor" paramétrico: cada tipo, una función que a partir de las dimensiones exteriores disponibles (las del retal), el grosor de tablero y unas reglas de ensamblaje (solape en uniones, tolerancia de guías, nº de divisores) genera una lista de piezas (paredes, base, tapa, frentes, baldas) lista para pasar como un `Project` normal al solver existente.
2. Reglas de ensamblaje mínimas por tipo (una unión a tope vs. rebajada cambia las medidas de las piezas que se tocan) — conocimiento de carpintería nuevo en el proyecto, no solo geometría de corte.
3. Encaja de forma natural con el sistema de plugins ya existente (`IDE-0008`) como grupo de entry point nuevo (p. ej. `boardcomposer.container_templates`) en vez de vivir en el Core — mantiene el Core sin conocimiento de "qué es un cajón", igual que ya hace con generadores/estrategias.

**Consecución.** Acotada con el usuario el 03/08/2026: caja simple, unión a tope, sin divisores, como diálogo en Studio (no plugin, sin casos de uso externos todavía) — dejando el registro de tipos abierto para ampliar después sin rediseñar el patrón. **Promovida a `IDE-0028`** (`docs/masterplan/DOC-004-Backlog.md`).

---

## Cómo usar este documento

Ninguna de estas ideas pasa a `DOC-004-Backlog.md` como `IDE-XXXX` hasta que se elija una candidata concreta y se confirme su alcance (como se hizo con `IDE-0007` a `IDE-0012`). Mientras tanto, viven aquí.
