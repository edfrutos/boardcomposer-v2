# BoardComposer

## Documento 3 — Roadmap del Producto

**Código:** DOC-003
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 16/07/2026

---

## Objetivo

Definir la evolución prevista de BoardComposer mediante fases, hitos y prioridades, proporcionando una visión clara del desarrollo del producto a corto, medio y largo plazo.

---

## Principios

El Roadmap representa la dirección del proyecto, no una planificación cerrada. Podrá evolucionar conforme aparezcan nuevas necesidades, siempre respetando el Manifiesto y la Arquitectura.

---

## Fase 1 — Core (Completada)

**Estado:** 🟢

Objetivos alcanzados:

- Motor de optimización desacoplado.
- Algoritmos Skyline y MaxRects.
- Beam Search.
- Sistema de evaluación.
- Exportadores básicos.
- Cobertura amplia mediante pruebas automatizadas.

---

## Fase 2 — BoardComposer Studio (Completada)

**Estado:** 🟢

Objetivo:

Construir la aplicación visual profesional para explorar, comparar y comprender soluciones de corte.

Entregables principales:

- Workspace. 🟢 (IDE-0001)
- Comparador de algoritmos. 🟢 (IDE-0002)
- Inspector de piezas. 🟢 (IDE-0003)
- Panel de propiedades. 🟢 (cubierto por el Inspector, IDE-0003)
- Gestión de proyectos. 🟢 (IDE-0004)
- Exportación visual. 🟢 (SVG/PDF, IDE-0005)
- Alta/edición de tableros y piezas, y soporte multi-tablero. 🟢 (`DT-0013`, `docs/masterplan/DOC-006-DeudaTecnica.md`)

---

## Fase 3 — Plataforma

**Estado:** 🟢 Completada

Incluye:

- API pública. 🟢 (IDE-0006: `/health`, `/strategies`, `/solve`; ver `docs/architecture.md`)
- Automatización. 🟢 (DEC-0009: cubierta por el mecanismo de plugins de `IDE-0008` — generadores, estrategias, importadores/exportadores instalables vía entry points; sin entrega nueva propia)
- Integraciones. 🟢 (DEC-0010: cubierta por los importadores/exportadores registrables de `IDE-0008` Fase D; sin entrega nueva propia)
- Servicios remotos. 🟢 (IDE-0009: autenticación por clave de API vía `BOARDCOMPOSER_API_KEY`, rate limiting con Flask-Limiter, `gunicorn` como servidor WSGI de producción; ver `docs/architecture.md`)

---

## Fase 4 — Inteligencia

**Estado:** 🟢 Completada (Fases A–F de IDE-0007)

Objetivos:

- Asistencia mediante IA. 🟢 (`AssistantService`/chat en Studio, Fase E)
- Explicaciones inteligentes. 🟢 (`explain_solution()`, Fase C)
- Recomendación automática de estrategias. 🟢 (`suggest_strategy()`, Fase D)
- Análisis avanzado de soluciones. 🟢 (generación de proyecto desde texto, Fase B; expuesto vía API, Fase F)

Proveedor de IA real conectado: `AnthropicProvider` (Claude, modelo `claude-haiku-4-5`), vía `default_provider()` — se activa automáticamente si hay `ANTHROPIC_API_KEY` en el entorno, si no cae a `MockAIProvider` (`docs/masterplan/DOC-004-Backlog.md`).

---

## Fase 5 — Ecosistema

**Estado:** 🟡 En curso

Objetivos:

- Plugins. 🟢 (IDE-0008, Fases A–E completas: generadores, estrategias, importadores/exportadores y paneles de Studio registrables vía entry points de Python)
- Marketplace. 🔵 (DEC-0011: guía para desarrolladores de plugins planificada como `IDE-0013`)
- Biblioteca de materiales. ⚪ Sin empezar.
- Comunidad. ⚪ Sin empezar.

---

## Prioridades actuales

Studio, API, IA, Plugins y Plataforma (antes P0–P2) ya están completos — ver arriba. El endurecimiento para producción (`IDE-0009`) y el empaquetado de Studio (`IDE-0011`, `pyside6-deploy`, `.app` de macOS) también están completos (`docs/masterplan/DOC-004-Backlog.md`). No quedan prioridades P0/P1 pendientes; las prioridades reales hoy son:

### Prioridad P2

- Exportación DXF. 🟢 Completado (`IDE-0012`, `solution_to_dxf()`, SDK `ezdxf`).
- Guía para desarrolladores de plugins. 🔵 Planificada (`IDE-0013`, `DEC-0011`) — primer paso concreto de Marketplace/Comunidad (Fase 5); biblioteca de materiales y marketplace público siguen sin acotar (`DOC-999-Ideas.md`).
- Receta de despliegue Cloud. 🔵 Planificada (`IDE-0014`, `DEC-0012`) — Dockerfile + guía de despliegue; instancia demo pública y SaaS real siguen sin acotar (`DOC-999-Ideas.md`).

---

## Criterios para modificar el Roadmap

Toda modificación deberá:

- aportar valor al usuario;
- mantener la coherencia con el Manifiesto;
- respetar la arquitectura definida;
- quedar registrada en el historial de decisiones.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- descomponer las fases en épicas (EP);
- vincular los futuros sprints;
- incorporar estimaciones y dependencias;
- aprobar como hoja de ruta oficial del proyecto.
