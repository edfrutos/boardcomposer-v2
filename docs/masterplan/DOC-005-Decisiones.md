# BoardComposer

## Documento 5 — Registro de Decisiones

**Código:** DOC-005
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 16/08/2026

---

## Objetivo

Registrar de forma permanente todas las decisiones estratégicas, funcionales y arquitectónicas que afecten al desarrollo de BoardComposer.

Este documento actúa como índice del conocimiento acumulado del proyecto y evita que decisiones importantes dependan de la memoria de sus desarrolladores.

---

## Principios

- Toda decisión relevante debe quedar documentada.
- Las decisiones nunca se eliminan; pueden quedar sustituidas o marcadas como obsoletas.
- Cada decisión debe poder justificarse en su contexto.
- Las decisiones importantes podrán ampliarse mediante un ADR (Architecture Decision Record).

---

## Formato de una decisión

```text
DEC-XXXX

Título

Fecha

Estado

Contexto

Alternativas consideradas

Decisión adoptada

Justificación

Consecuencias

Documentos relacionados
```

---

## Registro inicial

| ID | Título | Estado |

|----|--------|--------|
| DEC-0001 | El Core será independiente de cualquier interfaz | ✅ Vigente |
| DEC-0002 | BoardComposer será una plataforma multiplataforma | ✅ Vigente |
| DEC-0003 | El usuario explorará soluciones en lugar de ejecutar un único «Resolver» | ✅ Vigente |
| DEC-0004 | Toda funcionalidad comenzará en el Core antes de llegar a cualquier interfaz | ✅ Vigente |
| DEC-0005 | El proyecto utilizará un Master Plan versionado como referencia oficial | ✅ Vigente |
| DEC-0006 | El Asistente IA (`IDE-0007`) solo ajusta parámetros del solver determinista (pesos de puntuación, generadores a usar) — nunca genera geometría/colocaciones directamente | ✅ Vigente |
| DEC-0007 | Los plugins (`IDE-0008`) se registran vía *entry points* estándar de Python (`importlib.metadata`), no un cargador propio | ✅ Vigente |
| DEC-0008 | Ante una colisión de nombre, las capacidades integradas (generadores, estrategias, importadores, exportadores) siempre ganan sobre un plugin | ✅ Vigente |
| DEC-0009 | "Automatización" (Fase 3 del Roadmap) se considera cubierta por el sistema de plugins (`IDE-0008`) — no recibe una entrega propia | ✅ Vigente |
| DEC-0010 | "Integraciones" (Fase 3 del Roadmap) se considera cubierta por los importadores/exportadores de plugins (`IDE-0008` Fase D) — no recibe una entrega propia | ✅ Vigente |
| DEC-0011 | De las candidatas de Marketplace/Comunidad en `DOC-999-Ideas.md`, se empieza por la guía para desarrolladores de plugins (`IDE-0013`), la más acotada y sin decisión de producto pendiente | ✅ Vigente |
| DEC-0012 | De las candidatas de Cloud en `DOC-999-Ideas.md`, se empieza por la receta de despliegue — Dockerfile + guía (`IDE-0014`), la más acotada y sin decisión de producto pendiente | ✅ Vigente |
| DEC-0013 | De las candidatas restantes de Marketplace/Comunidad en `DOC-999-Ideas.md`, se sigue con la visibilidad de plugins instalados — CLI + API (`IDE-0015`), la única sin decisión de producto ni coste de infraestructura pendiente | ✅ Vigente |
| DEC-0014 | Para proteger la API de `IDE-0017` (despliegue privado de un único usuario), se descarta un sistema de login/registro con confirmación por email — implicaría la primera capa de persistencia de todo el proyecto (usuarios, tokens, envío de email transaccional) para un problema de un solo usuario. Se opta por un allowlist de IP en nginx (`allow`/`deny`) sobre `BOARDCOMPOSER_API_KEY` (`IDE-0009`) como defensa en profundidad | 🔄 Sustituida por `DEC-0015` |
| DEC-0015 | El allowlist de IP de `DEC-0014` ataba el acceso a una única red — se rompía al cambiar de IP/viajar. Se sustituye por autenticación HTTP Basic en nginx (`auth_basic`/`htpasswd`) en `bc.efjdefrutos.com` y `studio.efjdefrutos.com`: funciona desde cualquier red, sin infraestructura nueva ni persistencia (sigue sin ser el login/registro descartado en `DEC-0014`, que sigue igual de descartado). Se suma a `BOARDCOMPOSER_API_KEY` y a `VNC_PASSWORD`, no los sustituye — cada capa es una credencial independiente | ✅ Vigente |
| DEC-0016 | El ancho de sierra (kerf) se queda **fuera del dominio del Core** y se traduce en Studio (`DT-0020`). La alternativa era `ProjectConstraints.kerf_mm` como restricción de primera clase, que obligaba a tocar los 6 generadores, la puntuación, la CLI y la API: una capacidad nueva del producto para arreglar una incoherencia de Studio. En su lugar `LayoutService.to_core_project()` entrega cada pieza **y el tablero** ensanchados un corte — el Core solo ve tableros algo mayores — y `piece_fits_on_board()`/`find_free_position()` aplican la misma convención fuera del lienzo. Exacto para cortes en un eje, conservador en dos. Se revisará el día que el kerf tenga que importar también a quien usa la CLI o la API, que hoy no lo tienen | ✅ Vigente |
| DEC-0017 | Para distribuir el `.app` de forma privada (release de GitHub, no App Store) se descarta **firmar con un certificado autofirmado**: Gatekeeper solo confía en certificados emitidos por Apple, así que firmar por nuestra cuenta deja el mismo aviso al descargar y solo añade la falsa sensación de haberlo resuelto. Las dos únicas salidas reales son Developer ID Application + notarización (cuenta de Apple Developer, 99 USD/año) o quitar la cuarentena en destino. Se elige **preparar la primera sin contratarla todavía**: `scripts/sign_and_notarize.sh` y los pasos condicionales de `package-studio.yml` detectan si existen los secrets de firma — si están, firman, notarizan y grapan; si no, publican la build sin firmar junto a `docs/INSTALL-macos.md`. Contratar la cuenta pasa a ser añadir secrets, sin cambios de código. Ver `DT-0011`. Cuenta activada el 01/08/2026 — `v0.3.3` es la primera release realmente firmada y notarizada. | ✅ Vigente |
| DEC-0018 | Dirección de producto (31/07/2026): con el backlog técnico a cero (`v0.3.2`) y la única deuda abierta siendo de negocio, no de código (`DT-0011`), se decide monetizar la API sin esperar a un SaaS completo (cuentas propias, persistencia por usuario — sigue sin acotar, `DOC-999-Ideas.md`). Modelo híbrido: **BoardComposer Studio sigue gratis**, sin cambios; **la API se cobra por request**, sobre la autenticación por clave que ya existía (`IDE-0009`) — solo hacía falta ligarla a un plan con cuota. Planes cerrados con el usuario: `free` (20 solves/mes, 0€), `basico` (300/mes, 9€/mes, overage 0,05€/solve), `pro` (1500/mes, 29€/mes, overage 0,03€/solve). Se descartan por ahora, como candidatas de mayor alcance: instancia demo pública y marketplace de plugins. Construido como `IDE-0020` (claves por cliente + cuota, `src/boardcomposer/billing.py`) e `IDE-0021` (cobro de overage con Stripe, `src/boardcomposer/stripe_billing.py`), ambas en `v0.3.3`. | ✅ Vigente |
| DEC-0019 | De la Candidata 1 de aprovechamiento de retales (`DOC-999-Ideas.md`, 03/08/2026), acotada con el usuario al alcance más barato — alta manual del retal (sin inventario persistente entre proyectos) y elección manual en Studio (sin priorización automática del solver). Con ese alcance, la capacidad **ya existe** en el modelo actual: `Board` (`src/boardcomposer/domain/board.py`) no distingue procedencia — solo largo/ancho/grosor —, y `StudioBoard.material` (`studio/models/board.py`) ya es texto libre para anotar "es un retal". No recibe entrega de código propia ni número `IDE-XXXX`; se documenta como guía de uso, `docs/retales-como-tablero.md` | ✅ Vigente |
| DEC-0020 | De los tres frentes sin acotar de la Fase 5 (Marketplace público, Biblioteca de materiales, Comunidad), se empieza por la biblioteca de materiales — elegido con el usuario el 13/08/2026, sin decisión de producto pendiente a diferencia del marketplace público (¿ecosistema de terceros o uso interno?) o de comunidad (sin ninguna definición previa). Alcance acotado con el usuario en la misma sesión: catálogo **del taller** (persiste entre proyectos y reinicios, mismo patrón SQLite que el inventario de retales — `IDE-0039` — en vez de vivir dentro de cada `.bcstudio.json`), con campos básicos más proveedor y precio, exportable/importable como CSV para compartirlo entre instalaciones de Studio. Construido como `IDE-0041` | ✅ Vigente |
| DEC-0021 | El usuario esperaba que "Buscar actualizaciones" (`IDE-0032`) descargara el `.dmg` y lo autoinstalara con su autorización — nunca lo hizo (`DOC-999-Ideas.md`). Acotado el 16/08/2026 al alcance menor de las dos candidatas ya listadas: **descargar el `.dmg` y abrirlo** (Finder monta la imagen), no una instalación completa estilo Sparkle (la app sustituyéndose y reiniciándose sola) — esa queda descartada por ahora, mismo motivo original de `DOC-999-Ideas.md` (Gatekeeper tras un self-replace, sin caso de uso más allá de este). Al acotarlo salió un bloqueo real: los assets de una release de un repo privado exigen autenticación (`404` sin ella, igual que `DT-0025`), así que el Gist público (que resuelve *saber* la versión) no basta para *distribuir* el binario. Ni hacer público el repo entero (expondría `billing.py`/`stripe_billing.py`) ni embeber un token en el binario eran aceptables — mismo criterio que `DT-0025`. Se opta por un **segundo repo, público, sin código** (`edfrutos/boardcomposer-releases`) que solo aloja los `.dmg` de cada release; el CI (`package-studio.yml`) lo alimenta con un token de alcance mínimo (`RELEASES_REPO_TOKEN`, fine-grained, solo ese repo + Gists), que de paso automatiza la actualización del Gist y cierra `DT-0028`. Construido como `IDE-0043` | ✅ Vigente |

---

## Relación con ADR

Las decisiones que requieran un análisis técnico más profundo se desarrollarán en documentos independientes dentro de `docs/adr/`.

Este documento actúa como índice de dichas decisiones y como referencia histórica del proyecto.

---

## Normas de mantenimiento

- Toda decisión aprobada recibirá un identificador permanente.
- Las modificaciones deberán crear una nueva versión de la decisión o un ADR relacionado, nunca sobrescribir el contexto original.
- Ninguna decisión histórica será eliminada.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- crear los primeros ADR;
- enlazar decisiones con los documentos DOC-000 a DOC-004;
- incorporar referencias cruzadas con futuras Épicas y Sprints.