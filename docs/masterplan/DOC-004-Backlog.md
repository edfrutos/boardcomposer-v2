# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 01/07/2026

---

## Objetivo

Mantener un registro único, priorizado y trazable de todas las funcionalidades, mejoras, ideas e iniciativas previstas para BoardComposer.

El Backlog constituye la fuente oficial de trabajo del proyecto y evoluciona de forma continua.

---

## Principios

- Ninguna idea se pierde.
- Ninguna funcionalidad se implementa sin pasar previamente por el Backlog.
- Toda entrada debe tener un identificador único.
- La prioridad puede cambiar; la trazabilidad nunca.

---

## Estados

- ⚪ Idea
- 🔵 Planificada
- 🟡 En desarrollo
- 🟢 Completada
- 🔴 Bloqueada
- ⚫ Descartada

---

## Prioridades

- **P0** — Crítica
- **P1** — Alta
- **P2** — Media
- **P3** — Baja

---

## Formato de una entrada

```text
ID: IDE-0001
Título:
Estado:
Prioridad:
Impacto:
Esfuerzo:
Dependencias:
Documentos relacionados:
Descripción:
Criterios de aceptación:
Observaciones:
```

---

## Backlog inicial

| ID | Título | Estado | Prioridad |
|----|--------|--------|-----------|
| IDE-0001 | Workspace interactivo | 🟢 | P0 |
| IDE-0002 | Comparador de algoritmos | 🟢 | P0 |
| IDE-0003 | Inspector de piezas | 🟢 | P0 |
| IDE-0004 | Gestión de proyectos | 🟢 | P1 |
| IDE-0005 | Exportación PDF/SVG | 🟢 | P1 |
| IDE-0006 | API pública | 🟢 | P2 |
| IDE-0007 | Asistente IA | 🟢 | P2 |
| IDE-0008 | Sistema de plugins | 🟡 | P3 |

---

## IDE-0007 — Asistente IA

**Estado:** 🟢 Completado (Fases A–F). Proveedor real todavía sin decidir — todas las capacidades funcionan con `MockAIProvider`; las que necesitan una respuesta JSON estructurada (`project_from_text()`, `suggest_strategy()`, y por tanto `/assist/project`/`/assist/strategy`) requieren un proveedor real para dar resultados útiles.

Alcance dividido en fases, cada una construida sobre la anterior:

- **Fase A** (🟢 completada) — puerto `AIProvider` en el Core (`src/boardcomposer/ai/`) con `MockAIProvider` y `provider_by_name()`, sin proveedor real conectado.
- **Fase B** (🟢 completada) — `project_from_text()` (`src/boardcomposer/ai/project_from_text.py`): genera un `Project` a partir de texto libre, pidiendo al `AIProvider` un JSON con la misma forma que ya valida `/solve` en la API.
- **Fase C** (🟢 completada) — `explain_solution()` (`src/boardcomposer/ai/explain_solution.py`): pide al `AIProvider` una explicación en lenguaje natural de un `AssemblySolution`, a partir de sus métricas (tablas colocadas, dimensiones, desperdicio, puntuación) y de `SolutionExplanation` (fortalezas/debilidades/notas).
- **Fase D** (🟢 completada) — `suggest_strategy()` (`src/boardcomposer/ai/suggest_strategy.py`): a partir de un objetivo en lenguaje natural, pide al `AIProvider` unos pesos de puntuación (`ScoringWeights`) y generadores de disposición, y construye una `OptimizationStrategy` que `GeometrySolver` ejecuta igual que `balanced`/`material`/`compact`. La IA solo ajusta parámetros del solver determinista existente — nunca genera geometría directamente, para no comprometer la validez de las disposiciones.
- **Fase E** (🟢 completada) — `AssistantService`/`render_chat()` (`studio/assistant_service.py`, `studio/panels/chat_panel.py`): chat de ayuda contextual, nuevo dock "Asistente" en Studio. Envía la pregunta del usuario más el contexto del proyecto abierto directamente a `AIProvider.complete()` (conversación libre, sin pasar por `project_from_text()`/`explain_solution()`/`suggest_strategy()`).
- **Fase F** (🟢 completada) — `POST /assist/project`, `POST /assist/strategy`, `POST /assist/explain` (`src/boardcomposer/api.py`): exponen las Fases B, D y C respectivamente vía HTTP, con la misma validación de `boards`/`constraints` que ya usa `/solve`. `create_app(ai_provider=None)` acepta ahora un `AIProvider` inyectable (por defecto `provider_by_name("mock")`).

---

## IDE-0008 — Sistema de plugins

**Estado:** 🟡 En desarrollo. A diferencia de `IDE-0007`, introduce ejecución de código de terceros dentro de la aplicación (paquetes Python instalables, registrados vía *entry points*).

Alcance dividido en fases, cada una construida sobre la anterior:

- **Fase A** (🟢 completada) — `discover_plugins(group)` (`src/boardcomposer/plugins/discovery.py`): resuelve los *entry points* instalados para un grupo dado (`importlib.metadata.entry_points()`) en un diccionario `nombre -> objeto`, junto a una lista de `PluginLoadError` para los que fallan al cargar sin bloquear al resto.
- **Fase B** (⚪) — generadores de disposición como plugins, junto a los 6 ya existentes en `solver.generators.GENERATOR_REGISTRY`.
- **Fase C** (⚪) — estrategias de optimización como plugins, junto a `balanced`/`material`/`compact` en `strategy_by_name()`.
- **Fase D** (⚪) — importadores/exportadores como plugins (hoy solo hay CSV de entrada y SVG de salida en el Core).
- **Fase E** (⚪) — paneles/acciones de menú de Studio como plugins.

---

## Reglas de mantenimiento

- Cada nueva idea comienza como **IDE**.
- Cuando una idea se aprueba para desarrollo, se vinculará a una Épica (EP) y posteriormente a uno o varios Sprints (SPR).
- Las funcionalidades completadas permanecerán en este documento como histórico.
- Ninguna entrada se elimina; únicamente cambia de estado.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- incorporar las primeras Épicas (EP);
- enlazar el Roadmap con el Backlog;
- definir el flujo completo Idea → Épica → Sprint → Implementación → Liberación.
