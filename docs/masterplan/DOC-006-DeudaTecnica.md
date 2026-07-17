

# BoardComposer

## Documento 6 — Gestión de la Deuda Técnica

**Código:** DOC-006
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 17/07/2026

---

## Objetivo

Registrar, clasificar y gestionar toda la deuda técnica del proyecto BoardComposer para asegurar que el crecimiento del producto no comprometa su calidad, mantenibilidad ni capacidad de evolución.

La deuda técnica es un elemento normal del desarrollo. El objetivo no es eliminarla por completo, sino hacerla visible, controlarla y decidir conscientemente cuándo asumirla o resolverla.

---

## Principios

- Toda deuda técnica conocida debe registrarse.
- La deuda nunca debe depender de la memoria del equipo.
- Cada elemento tendrá una prioridad y un impacto estimado.
- La deuda técnica forma parte de la planificación del producto.
- Ninguna deuda crítica podrá permanecer indefinidamente sin revisión.

---

## Clasificación

### DT-A — Arquitectura
Problemas de diseño estructural.

### DT-C — Código
Duplicación, complejidad o refactorizaciones pendientes.

### DT-T — Tests
Cobertura insuficiente o pruebas mejorables.

### DT-D — Documentación
Documentación incompleta o desactualizada.

### DT-P — Rendimiento
Aspectos relacionados con optimización y escalabilidad.

### DT-UX — Experiencia de usuario
Limitaciones conocidas en la interfaz o flujo de trabajo.

---

## Formato de un registro

```text
DT-0001

Título

Categoría

Prioridad

Descripción

Impacto

Riesgo

Propuesta de resolución

Documentos relacionados

Estado
```

---

## Registro inicial

| ID | Categoría | Descripción | Estado |

|----|-----------|-------------|--------|
| DT-0001 | DT-D | Completar la documentación funcional de BoardComposer Studio. Resuelto en `docs/studio.md`: servicios compartidos (`StudioServices`), ciclo de vida del proyecto, undo/redo, las dos capas de selección, validación de colocación, arrastre, flujo de resolución de layout y el `EventBus` (construido pero aún sin ningún publisher/subscriber real). | 🟢 Resuelto |
| DT-0002 | DT-A | Revisar y documentar la arquitectura interna del Solver tras la incorporación de nuevos algoritmos. Resuelto en `docs/solver_architecture.md`: aclara las dos jerarquías de `BaseSolver` (`GeometrySolver` en producción, `SequentialSolver` sin usar fuera de sus propios tests), y documenta que la variante beam search de MaxRects (`maxrects_engine.py`/`maxrects_beam_runner.py`) funciona pero no está dada de alta en `GENERATOR_REGISTRY` — solo la usan `workbench/` y `tools/visualize_demo.py`. | 🟢 Resuelto |
| DT-0003 | DT-T | Mantener la cobertura de pruebas por encima del objetivo definido. | 🟢 Controlado |
| DT-0004 | DT-C | `solver/packing_runner.py` (experimento de runner+selector genérico, commit `8feea6b`) y `solver/generator_utils.py` (adaptador `single_solution_generator`, commit `ab7b963`) quedaron sin uso tras adoptarse `CandidatePipeline`/`evaluate()` y el envoltorio manual de `generators.py`. Eliminados: sin importaciones, sin tests, sin mención en documentación. | 🟢 Resuelto |
| DT-0005 | DT-A | `pyproject.toml` no declaraba `[build-system]` ni `[tool.setuptools.packages.find]`: el paquete `studio/` (fuera de `src/`) solo era importable "por accidente" cuando el directorio de trabajo actual estaba en `sys.path` (p. ej. `python -m pytest`), pero no con la invocación real de CI (`pytest -q`, sin `python -m`). Detectado al añadir el primer test de Studio (`test_studio_project_io.py`). Resuelto añadiendo `where = ["src", "."]` a `packages.find`; verificado con `pip install -e .` + `pytest -q` puro. | 🟢 Resuelto |
| DT-0006 | DT-P | `GeometrySolver` no tenía ningún límite de tamaño de proyecto en la API: medido empíricamente, 100 tableros resuelven en ~1s, 200 en ~7s, 300+ no termina en un tiempo razonable (no relacionado con `generate_horizontal_permutations()`/`generate_vertical_permutations()`, que ya se autolimitan a 6 tableros). Resuelto añadiendo `MAX_BOARDS = 100` en `/solve`, `/assist/strategy` y `/assist/explain` (`api.py`). | 🟢 Resuelto |
| DT-0007 | DT-D | `AI_CONTEXT.md`, `ROADMAP.md`, `TODO.md` y `CHANGELOG.md` de la raíz quedaron congelados en el primer día del proyecto (26/06/2026) — `AI_CONTEXT.md` llegó a afirmar "sin implementación" con el proyecto ya completo en Core/Studio/API/IA/Plugins, lo que podía desorientar a cualquier sesión de IA que lo tomara como referencia. Resuelto: `AI_CONTEXT.md` actualizado con el estado real y redirigiendo a `docs/masterplan/DOC-004-Backlog.md`; `ROADMAP.md`/`TODO.md` marcados como superados con puntero al masterplan; `CHANGELOG.md` con una entrada `0.1.0` cubriendo los hitos pendientes de registrar; `DOC-003-Roadmap.md` corregido (Fases 2, 4 y 5 daban por no hechas capacidades ya completas). | 🟢 Resuelto |
| DT-0008 | DT-UX | Empaquetado y distribución de Studio pendiente: hoy se ejecuta desde código fuente, sin instalador ni binario distribuible. Resuelto en `IDE-0011` (`pyside6-deploy`, `.app` de macOS). | 🟢 Resuelto |
| DT-0009 | DT-A | Conectar un proveedor de IA real para `IDE-0007` (todas sus capacidades corrían sobre `MockAIProvider`). Resuelto añadiendo `AnthropicProvider` (`src/boardcomposer/ai/anthropic_provider.py`, SDK `anthropic`, modelo `claude-haiku-4-5`) y `default_provider()`, que lo activa automáticamente si hay `ANTHROPIC_API_KEY` en el entorno y si no cae a `MockAIProvider`; usado como valor por defecto en `create_app()` (API) y `AssistantService` (Studio). | 🟢 Resuelto |
| DT-0010 | DT-A | Endurecimiento para producción de la API (`IDE-0009`): sin autenticación ni rate limiting, servidor de desarrollo de Flask (no WSGI de producción). Resuelto con `create_app(api_key=None, rate_limit=None)`: clave de API por cabecera `X-API-Key` (variable `BOARDCOMPOSER_API_KEY`, opcional), `Flask-Limiter` a 60 peticiones/minuto por IP, y `gunicorn` como servidor WSGI (dependencia opcional `[prod]`, `make serve`). Limitación conocida: el almacenamiento del rate limiting es en memoria (`storage_uri="memory://"`) y no se comparte entre workers de `gunicorn` — cada worker cuenta sus propias peticiones, así que el límite real con varios workers es aproximadamente `60 × nº de workers` por minuto, no 60 exactas. Migrar a un backend compartido (Redis) solo si esto se convierte en un problema real. | 🟢 Resuelto |
| DT-0011 | DT-UX | El `.app` de `IDE-0011` no está firmado ni notarizado por Apple (Gatekeeper mostrará el aviso de "desarrollador no identificado" al primer arranque) y solo se genera para macOS/arm64 (sin Windows/Linux ni Intel). Ninguno bloquea el uso previsto (distribución interna/personal); firma+notarización requerirían una cuenta de Apple Developer, y Windows/Linux/Intel un runner de CI adicional por plataforma. Abordar solo si se necesita distribución pública o pública fuera de macOS Apple Silicon. | 🔴 Abierto |
| DT-0012 | DT-UX | `MainWindow._new_project()` (`studio/main_window.py`) llamaba a `_load_demo_project()`, el mismo método que se ejecuta al arrancar Studio — "Nuevo proyecto" nunca creaba un proyecto vacío, siempre recargaba la demo. Detectado probando datos reales tras el empaquetado (`IDE-0011`). Resuelto: `_new_project()` construye ahora un `StudioProject` vacío (`project_id` generado con `uuid.uuid4()`, sin tableros/piezas/colocaciones). | 🟢 Resuelto |
| DT-0013 | DT-UX | Studio no permitía crear ni editar tablas o piezas desde la interfaz: el menú "Editar" solo tenía deshacer/rehacer/rotar/eliminar (todas sobre piezas ya existentes), el Inspector (`inspector_panel.py`) era de solo lectura, y `BoardWorkspace._add_board()`/`_add_pieces()` únicamente dibujaban datos que ya estaban en el `StudioProject` cargado — no creaban nada nuevo. `docs/masterplan/ui/flows/FLW-006-Editar-Proyecto.md` ya documentaba el flujo previsto (validación, historial, deshacer/rehacer). Resuelto en 5 fases (PR #31–#35): Fase A — `board_id` en `StudioPlacement`, persistencia y migración retrocompatible; Fase B — `AddBoardCommand`/`EditBoardCommand`/`AddPieceCommand`/`EditPieceCommand` deshacibles vía `CommandManager`; Fase C — tablero activo rastreado y renderizado en `BoardWorkspace`, seleccionable desde el Explorer; Fase D — `BoardDialog`/`PieceDialog` (`studio/dialogs/`) y menús "Proyecto"/"Editar" para alta/edición con validación; Fase E — `LayoutService` (`solve_current_project()`, `compare_solutions()`, `apply_last_solution_to_current_project()`, `apply_comparison_solution()`) resuelve el tablero objetivo a partir del tablero activo del workspace en vez de asumir siempre `boards[0]`. | 🟢 Resuelto |
| DT-0014 | DT-UX | `BoardDialog`/`PieceDialog` (`studio/dialogs/`) no pedían grosor (`thickness_mm`) ni cantidad al crear un tablero o pieza — solo Id/Largo/Ancho/Material. Detectado probando datos reales tras `DT-0013`. Resuelto: `thickness_mm: float = 19.0` añadido a `StudioBoard`/`StudioPiece` (persistido en `.bcstudio.json`, con el mismo valor por defecto para migrar ficheros antiguos sin esa clave) y expuesto como campo "Grosor" en ambos diálogos; `LayoutService.to_core_project()` usa ahora `piece.thickness_mm` en vez del `19` fijo que tenía antes. "Cantidad" resuelto como una comodidad del propio diálogo, no un campo del modelo: un `QSpinBox` "Cantidad" (solo visible al añadir, no al editar) crea N tableros/piezas idénticos de una vez, con ids derivados (`p1`, `p1-2`, `p1-3`…) vía el helper `_generate_ids()`. | 🟢 Resuelto |
| DT-0015 | DT-UX | El nodo "Soluciones" del Explorer (`studio/main_window.py`, `_reload_explorer()`) se creaba y se añadía al árbol pero nunca se rellenaba — permanecía vacío siempre. Detectado probando datos reales tras `DT-0013`. Resuelto quitando el nodo del Explorer (decisión explícita: no prometer una funcionalidad sin implementar); se podrá reintroducir el día que se acote qué debe mostrar realmente (historial de soluciones, vista previa por candidata, etc.). | 🟢 Resuelto |
| DT-0016 | DT-UX | El Comparador de soluciones (`studio/panels/comparator_panel.py`) puede mostrar varias "soluciones" con las 5 métricas agregadas (algoritmo, piezas colocadas, aprovechamiento, desperdicio, puntuación) idénticas entre sí, aunque el motor ya deduplica por geometría y las soluciones subyacentes SÍ son distintas (verificado con el proyecto demo: 4 candidatas de `vertical_permutation` con las mismas 3 piezas en orden de apilado diferente — mismo aprovechamiento/puntuación porque el hueco total no depende del orden). Ninguna columna de la tabla revela esa diferencia real (qué pieza va dónde), ni hay vista previa del lienzo por candidata antes de aplicarla — solo se puede ver aplicando una, mirando, deshaciendo y probando la siguiente. Detectado probando datos reales. Pendiente de acotar qué mostrar por solución (¿vista previa en miniatura del lienzo? ¿orden/posición de piezas en la tabla?) antes de programarlo. | 🔴 Abierto |

---

## Política de gestión

- La deuda técnica deberá revisarse al cierre de cada Sprint.
- Ninguna versión mayor del producto se publicará sin revisar este documento.
- Las deudas resueltas permanecerán registradas como histórico.
- La prioridad podrá modificarse, pero nunca desaparecerá el registro.

---

## Relación con otros documentos

- DOC-002 — Arquitectura.
- DOC-003 — Roadmap.
- DOC-004 — Backlog.
- DOC-005 — Registro de Decisiones.
- ADR relacionados.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- definir métricas de deuda técnica;
- establecer umbrales de aceptación por versión;
- integrar este documento en el proceso de cierre de Sprint.