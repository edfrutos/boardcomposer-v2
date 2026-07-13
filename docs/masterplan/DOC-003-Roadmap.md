# BoardComposer

## Documento 3 — Roadmap del Producto

**Código:** DOC-003
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 13/07/2026

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

---

## Fase 3 — Plataforma

**Estado:** 🟡 En curso

Incluye:

- API pública. 🟢 (IDE-0006: `/health`, `/strategies`, `/solve`; ver `docs/architecture.md`)
- Automatización. ⚪ Sin empezar.
- Integraciones. ⚪ Sin empezar.
- Servicios remotos. ⚪ Sin empezar — la API sigue siendo el servidor de desarrollo de Flask, sin auth, sin WSGI de producción.

---

## Fase 4 — Inteligencia

**Estado:** 🟢 Completada (Fases A–F de IDE-0007)

Objetivos:

- Asistencia mediante IA. 🟢 (`AssistantService`/chat en Studio, Fase E)
- Explicaciones inteligentes. 🟢 (`explain_solution()`, Fase C)
- Recomendación automática de estrategias. 🟢 (`suggest_strategy()`, Fase D)
- Análisis avanzado de soluciones. 🟢 (generación de proyecto desde texto, Fase B; expuesto vía API, Fase F)

Con una salvedad importante: todo corre sobre `MockAIProvider` — no hay ningún proveedor de IA real conectado todavía (`docs/masterplan/DOC-004-Backlog.md`). `/assist/project` y `/assist/strategy` no dan resultados útiles sin uno.

---

## Fase 5 — Ecosistema

**Estado:** 🟡 En curso

Objetivos:

- Plugins. 🟢 (IDE-0008, Fases A–E completas: generadores, estrategias, importadores/exportadores y paneles de Studio registrables vía entry points de Python)
- Marketplace. ⚪ Sin empezar.
- Biblioteca de materiales. ⚪ Sin empezar.
- Comunidad. ⚪ Sin empezar.

---

## Prioridades actuales

Studio, API, IA y Plugins (antes P0–P2) ya están completos — ver arriba. Las prioridades reales hoy son:

### Prioridad P0

- Conectar un proveedor de IA real (hoy todo corre sobre `MockAIProvider`).
- Endurecimiento para producción: autenticación, rate limiting, servidor WSGI de producción (hoy es el servidor de desarrollo de Flask).

### Prioridad P1

- Importación desde Excel (RF-002, pendiente desde el inicio).
- Empaquetado y distribución de Studio (hoy se ejecuta desde código fuente).

### Prioridad P2

- Exportación DXF.
- Marketplace, biblioteca de materiales, comunidad (Fase 5).
- Cloud.

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
