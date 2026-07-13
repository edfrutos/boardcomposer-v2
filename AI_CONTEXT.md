# AI Context

Nombre del proyecto: BoardComposer

Propósito:
Generar composiciones de tablas reutilizando material existente mediante algoritmos de optimización.

Estado actual (ver `docs/masterplan/DOC-004-Backlog.md` para el detalle vivo):
- Core implementado: modelos de dominio, varios algoritmos de layout (skyline, maxrects, beam search, permutaciones), sistema de puntuación y explicación de soluciones.
- CLI funcional (entrada CSV, salida texto/JSON).
- API HTTP (`/solve`, `/strategies`, `/assist/*`).
- BoardComposer Studio (GUI PySide6): workspace interactivo, comparador, inspector, gestión de proyectos, exportación SVG/PDF.
- Asistente IA (IDE-0007, 6 fases completas) sobre un proveedor pluggable — todavía sin proveedor real conectado (usa `MockAIProvider`).
- Sistema de plugins (IDE-0008, 5 fases completas): generadores, estrategias, importadores/exportadores y paneles de Studio registrables vía entry points de Python.
- Pendiente: importación desde Excel (RF-002), exportación DXF, conectar un proveedor de IA real, endurecimiento para producción (auth, servidor WSGI, rate limiting, empaquetado de Studio).

Reglas:
- No romper compatibilidad del modelo de datos.
- Documentar cualquier decisión relevante en `docs/masterplan/DOC-005-Decisiones.md` (el `DECISIONS.md` de la raíz quedó congelado en el día 1 del proyecto).
- Actualizar `CHANGELOG.md` con cada hito.
- El backlog vivo y el estado real de cada funcionalidad están en `docs/masterplan/DOC-004-Backlog.md`, no en `ROADMAP.md`/`TODO.md` de la raíz (ambos son el andamiaje inicial del proyecto, sin mantener desde entonces).
