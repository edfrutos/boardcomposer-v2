# AI Context

Nombre del proyecto: BoardComposer

Propósito:
Generar composiciones de tablas reutilizando material existente mediante algoritmos de optimización.

Estado actual (ver `docs/masterplan/DOC-004-Backlog.md` para el detalle vivo):
- Core implementado: modelos de dominio, varios algoritmos de layout (skyline, maxrects, beam search, permutaciones), sistema de puntuación y explicación de soluciones.
- CLI funcional (entrada CSV o Excel, salida texto/JSON).
- API HTTP (`/solve`, `/strategies`, `/assist/*`), con autenticación opcional por clave (`BOARDCOMPOSER_API_KEY`), rate limiting (Flask-Limiter) y `gunicorn` como servidor WSGI de producción (`IDE-0009`).
- BoardComposer Studio (GUI PySide6): workspace interactivo, comparador, inspector, gestión de proyectos, exportación SVG/PDF.
- Asistente IA (IDE-0007, 6 fases completas) sobre un proveedor pluggable, con `AnthropicProvider` (modelo `claude-haiku-4-5`) conectado como proveedor real. `default_provider()` usa Anthropic si hay `ANTHROPIC_API_KEY` en el entorno, si no cae a `MockAIProvider`.
- Sistema de plugins (IDE-0008, 5 fases completas): generadores, estrategias, importadores/exportadores y paneles de Studio registrables vía entry points de Python.
- Pendiente: exportación DXF, empaquetado y distribución de Studio.

Reglas:
- No romper compatibilidad del modelo de datos.
- Documentar cualquier decisión relevante en `docs/masterplan/DOC-005-Decisiones.md` (el `DECISIONS.md` de la raíz quedó congelado en el día 1 del proyecto).
- Actualizar `CHANGELOG.md` con cada hito.
- El backlog vivo y el estado real de cada funcionalidad están en `docs/masterplan/DOC-004-Backlog.md`, no en `ROADMAP.md`/`TODO.md` de la raíz (ambos son el andamiaje inicial del proyecto, sin mantener desde entonces).
