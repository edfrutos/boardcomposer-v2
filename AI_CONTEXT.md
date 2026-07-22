# AI Context

Nombre del proyecto: BoardComposer

Propósito:
Generar composiciones de tablas reutilizando material existente mediante algoritmos de optimización.

Versión actual: 0.2.0 (publicada 2026-07-22). Ver `docs/masterplan/DOC-004-Backlog.md` para el detalle vivo de cada funcionalidad (todos los IDEs planificados, IDE-0001–IDE-0018, están en 🟢 completado).

Estado actual:
- Core implementado: modelos de dominio, varios algoritmos de layout (skyline, maxrects, beam search, permutaciones), sistema de puntuación y explicación de soluciones.
- CLI funcional (entrada CSV o Excel, salida texto/JSON). Subcomando `boardcomposer plugins` para inspeccionar plugins instalados.
- API HTTP (`/solve`, `/strategies`, `/assist/*`, `/plugins`), con autenticación opcional por clave (`BOARDCOMPOSER_API_KEY`), rate limiting (Flask-Limiter) y `gunicorn` como servidor WSGI de producción (`IDE-0009`).
- BoardComposer Studio (GUI PySide6): workspace interactivo, comparador, inspector, gestión de proyectos, exportación SVG/PDF/DXF, alta/edición de tableros y piezas con soporte multi-tablero, importación de piezas desde CSV (`IDE-0018`), tema visual claro/oscuro con detección automática del sistema, iconos de línea y toolbar (`IDE-0016`). Empaquetado como `.app` de macOS con `pyside6-deploy` (`make package`; publicado como release de GitHub al crear un tag `v*`, `IDE-0011`); lanzable también en desarrollo vía `boardcomposer-studio`.
- Asistente IA (IDE-0007, 6 fases completas) sobre un proveedor pluggable, con `AnthropicProvider` (modelo `claude-haiku-4-5`) conectado como proveedor real. `default_provider()` usa Anthropic si hay `ANTHROPIC_API_KEY` en el entorno, si no cae a `MockAIProvider`.
- Sistema de plugins (IDE-0008, 5 fases completas): generadores, estrategias, importadores/exportadores y paneles de Studio registrables vía entry points de Python.
- Exportación DXF (`IDE-0012`, SDK `ezdxf`), junto a SVG/PDF ya existentes.
- Despliegue privado verificado en VPS propio con Plesk (`IDE-0017`): API en `bc.efjdefrutos.com` y Studio accesible por navegador vía noVNC en `studio.efjdefrutos.com`. Autenticación por HTTP Basic (nginx) + `BOARDCOMPOSER_API_KEY` + `VNC_PASSWORD` como capas independientes.
- Sin IDEs pendientes. Ideas sin acotar (marketplace real, instancia demo pública, SaaS) en `docs/masterplan/DOC-999-Ideas.md`.

Reglas:
- No romper compatibilidad del modelo de datos.
- Documentar cualquier decisión relevante en `docs/masterplan/DOC-005-Decisiones.md` (el `DECISIONS.md` de la raíz quedó congelado en el día 1 del proyecto).
- Actualizar `CHANGELOG.md` con cada hito.
- El backlog vivo y el estado real de cada funcionalidad están en `docs/masterplan/DOC-004-Backlog.md`, no en `ROADMAP.md`/`TODO.md` de la raíz (ambos son el andamiaje inicial del proyecto, sin mantener desde entonces).
