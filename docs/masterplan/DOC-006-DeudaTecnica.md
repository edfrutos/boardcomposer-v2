

# BoardComposer

## Documento 6 — Gestión de la Deuda Técnica

**Código:** DOC-006
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 26/07/2026

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
| DT-0011 | DT-UX | El `.app` de `IDE-0011` no está firmado ni notarizado por Apple (`codesign -dv`: `flags=0x2(adhoc)`, `TeamIdentifier=not set`; `spctl --assess` lo rechaza con "no usable signature") y solo se genera para macOS/arm64 (sin Windows/Linux ni Intel). Verificado con una build real (18/07/2026): el aviso de Gatekeeper "no se puede abrir porque Apple no puede comprobar que no contiene malware" **no** aparece al abrir un `.app` compilado en local (`make package` + `open`/doble clic en Finder) — solo se activa si el fichero lleva el atributo `com.apple.quarantine`, que macOS añade al descargarlo desde fuera (navegador, Mail, AirDrop). El asset que publica `IDE-0011` en cada release de GitHub sí quedará marcado así al descargarse, así que quien lo baje desde ahí verá el aviso aunque una build local no lo muestre. Ninguno de los dos bloquea el uso previsto (distribución interna/personal, ejecutando una build propia o aceptando el aviso una vez tras descargar el release); firma+notarización requerirían una cuenta de Apple Developer, y Windows/Linux/Intel un runner de CI adicional por plataforma. Abordar solo si se necesita distribución pública o fuera de macOS Apple Silicon. **Mitigado, no resuelto (27/07/2026, `DEC-0017`):** descartada la firma autofirmada, que no sirve de nada — Gatekeeper solo confía en certificados emitidos por Apple, así que un certificado propio deja exactamente el mismo aviso. Hecho lo que sí se puede sin cuenta de pago: (a) el bundle identifier pasa de `app` —el basename de `app.py`, ni único ni notarizable— a `com.efjdefrutos.boardcomposer.studio` vía `--macos-signed-app-name`, más `--macos-app-version` cuya coherencia con `pyproject.toml` verifica `scripts/check_project.py`; (b) `docs/INSTALL-macos.md` acompaña al `.zip` en cada release sin firmar, con el `xattr -dr com.apple.quarantine` que resuelve el aviso y la explicación de por qué aparece; (c) `scripts/sign_and_notarize.sh` (firma *inside-out*, sin `--deep` porque Apple lo desaconseja para firmar, hardened runtime, `notarytool --wait`, `stapler`) y los pasos condicionales de `package-studio.yml` quedan escritos y a la espera: el día que existan los secrets (`MACOS_CERTIFICATE_P12`, `MACOS_CERTIFICATE_PASSWORD`, `MACOS_SIGNING_IDENTITY`, `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD`) las releases salen firmadas y notarizadas sin tocar una línea. Sigue abierto porque el aviso de Gatekeeper solo desaparece con cuenta de Apple Developer (99 USD/año), y porque Windows/Linux/Intel siguen sin cubrirse. | 🔴 Abierto |
| DT-0012 | DT-UX | `MainWindow._new_project()` (`studio/main_window.py`) llamaba a `_load_demo_project()`, el mismo método que se ejecuta al arrancar Studio — "Nuevo proyecto" nunca creaba un proyecto vacío, siempre recargaba la demo. Detectado probando datos reales tras el empaquetado (`IDE-0011`). Resuelto: `_new_project()` construye ahora un `StudioProject` vacío (`project_id` generado con `uuid.uuid4()`, sin tableros/piezas/colocaciones). | 🟢 Resuelto |
| DT-0013 | DT-UX | Studio no permitía crear ni editar tablas o piezas desde la interfaz: el menú "Editar" solo tenía deshacer/rehacer/rotar/eliminar (todas sobre piezas ya existentes), el Inspector (`inspector_panel.py`) era de solo lectura, y `BoardWorkspace._add_board()`/`_add_pieces()` únicamente dibujaban datos que ya estaban en el `StudioProject` cargado — no creaban nada nuevo. `docs/masterplan/ui/flows/FLW-006-Editar-Proyecto.md` ya documentaba el flujo previsto (validación, historial, deshacer/rehacer). Resuelto en 5 fases (PR #31–#35): Fase A — `board_id` en `StudioPlacement`, persistencia y migración retrocompatible; Fase B — `AddBoardCommand`/`EditBoardCommand`/`AddPieceCommand`/`EditPieceCommand` deshacibles vía `CommandManager`; Fase C — tablero activo rastreado y renderizado en `BoardWorkspace`, seleccionable desde el Explorer; Fase D — `BoardDialog`/`PieceDialog` (`studio/dialogs/`) y menús "Proyecto"/"Editar" para alta/edición con validación; Fase E — `LayoutService` (`solve_current_project()`, `compare_solutions()`, `apply_last_solution_to_current_project()`, `apply_comparison_solution()`) resuelve el tablero objetivo a partir del tablero activo del workspace en vez de asumir siempre `boards[0]`. | 🟢 Resuelto |
| DT-0014 | DT-UX | `BoardDialog`/`PieceDialog` (`studio/dialogs/`) no pedían grosor (`thickness_mm`) ni cantidad al crear un tablero o pieza — solo Id/Largo/Ancho/Material. Detectado probando datos reales tras `DT-0013`. Resuelto: `thickness_mm: float = 19.0` añadido a `StudioBoard`/`StudioPiece` (persistido en `.bcstudio.json`, con el mismo valor por defecto para migrar ficheros antiguos sin esa clave) y expuesto como campo "Grosor" en ambos diálogos; `LayoutService.to_core_project()` usa ahora `piece.thickness_mm` en vez del `19` fijo que tenía antes. "Cantidad" resuelto como una comodidad del propio diálogo, no un campo del modelo: un `QSpinBox` "Cantidad" (solo visible al añadir, no al editar) crea N tableros/piezas idénticos de una vez, con ids derivados (`p1`, `p1-2`, `p1-3`…) vía el helper `_generate_ids()`. | 🟢 Resuelto |
| DT-0015 | DT-UX | El nodo "Soluciones" del Explorer (`studio/main_window.py`, `_reload_explorer()`) se creaba y se añadía al árbol pero nunca se rellenaba — permanecía vacío siempre. Detectado probando datos reales tras `DT-0013`. Resuelto quitando el nodo del Explorer (decisión explícita: no prometer una funcionalidad sin implementar); se podrá reintroducir el día que se acote qué debe mostrar realmente (historial de soluciones, vista previa por candidata, etc.). | 🟢 Resuelto |
| DT-0016 | DT-UX | El Comparador de soluciones (`studio/panels/comparator_panel.py`) podía mostrar varias "soluciones" con las 5 métricas agregadas (algoritmo, piezas colocadas, aprovechamiento, desperdicio, puntuación) idénticas entre sí, aunque el motor ya deduplica por geometría y las soluciones subyacentes SÍ son distintas (verificado con el proyecto demo: 4 candidatas de `vertical_permutation` con las mismas 3 piezas en orden de apilado diferente — mismo aprovechamiento/puntuación porque el hueco total no depende del orden). Ninguna columna revelaba esa diferencia real. Resuelto con una fila nueva "Orden de piezas" (`_piece_order()`): las piezas de cada solución ordenadas por posición (arriba-abajo, izquierda-derecha) y unidas con `→`, verificado con el mismo escenario del proyecto demo (4 candidatas, mismas 92.4 de puntuación, órdenes `P-001 → P-002 → P-003` / `P-001 → P-003 → P-002` / `P-002 → P-001 → P-003` / `P-002 → P-003 → P-001`). Vista previa en miniatura del lienzo por candidata queda fuera de alcance (no acotada, mayor esfuerzo). | 🟢 Resuelto |
| DT-0017 | DT-C | Corrección multi-tablero posterior a `v0.2.0`: `LayoutService` seguía razonando como si el proyecto tuviera un solo tablero. Aplicar una disposición vaciaba las colocaciones del resto de tableros (`_apply_solution()` limpiaba la lista completa); `to_core_project()` empaquetaba todas las piezas del proyecto sin mirar dónde estaban ya colocadas (resolver el tablero B duplicaba una pieza ya puesta en el A) ni comprobar `thickness_mm` (piezas forzadas en tableros de otro grosor); y las piezas sobrantes se descartaban aunque quedaran tableros vacíos. Resuelto: sustitución solo de las colocaciones del tablero resuelto, exclusión de piezas ya colocadas en otro tablero y de grosor no coincidente, y `_fill_other_empty_boards_with_leftovers()` — que solo prueba tableros completamente vacíos, para no rebarajar uno ya ordenado. Del mismo bloque: `RotatePieceCommand` no sincronizaba `placement.rotated` (la exportación salía en la orientación original) y `MoveToBoardCommand` reasignaba el `board_id` sin validar grosor, límites ni solapes — resueltos con `studio/workspace/placement_fit.py` (`piece_fits_on_board()`, `find_free_position()`), el equivalente sin Qt de `PlacementValidator` para lo que ocurre fuera de la escena gráfica. | 🟢 Resuelto |
| DT-0018 | DT-C | Números no finitos aceptados en todas las rutas de entrada externa: `json.loads()` interpreta `"NaN"`/`"Infinity"` como flotantes y toda comparación contra `NaN` es falsa, así que las guardas `< 0`/`<= 0` los dejaban pasar hasta el solver, la puntuación o la exportación (`/solve` respondía `500` en vez de `400`). Los modelos de Studio, además, no validaban nada: un `.bcstudio.json` manipulado podía sembrar un tablero de -500 mm. Resuelto exigiendo `math.isfinite()` en `Board`, `ProjectConstraints`, `BoardPlacement`, `SolutionScore` y componentes, los pesos que devuelve la IA en `suggest_strategy()`, el importador CSV de Studio y `StudioBoard`/`StudioPiece`/`StudioPlacement` (esta última solo finitud, no signo: una coordenada negativa es un estado transitorio legítimo al arrastrar una pieza fuera del tablero). Del mismo bloque: `project_from_dict()` aceptaba colocaciones que apuntaban a piezas o tableros ausentes del fichero y fallaba después, sin protección, al renderizar el workspace — ahora se descartan (proyecto dañado pero recuperable) y se informan por el callback `on_warning`, que `MainWindow` muestra en un diálogo. | 🟢 Resuelto |
| DT-0019 | DT-UX | Un fichero de entrada malformado volcaba un traceback de Python desde la CLI (`ValueError` de `float()`, `KeyError` por columna ausente, `FileNotFoundError`), sin indicar qué fila fallaba — el importador de Studio ya lo hacía bien, los cargadores del Core no. Resuelto: ambos comprueban las columnas obligatorias por adelantado y envuelven cada fila, lanzando `LoaderError` con el número de línea (la cabecera es la fila 1, así que coincide con lo que el usuario ve en su editor); `LoaderError` hereda de `ValueError` para no romper a quien ya lo capturaba. El cargador de Excel cubre además la hoja vacía y la fila con distinto número de celdas que la cabecera. La CLI los convierte, junto a `OSError`, en un mensaje de una línea y código de salida 1. | 🟢 Resuelto |
| DT-0020 | DT-C | El ancho de sierra (`StudioProject.kerf_mm`, menú "Proyecto" → "Ancho de sierra…", `SetKerfCommand`) se configura y se persiste, pero solo lo consume el arrastre interactivo: `BoardWorkspace.constrain_piece_position()` lo pasa a `PlacementValidator.constrain_position()` como separación al hacer *snap*. No lo tienen en cuenta el solver (`LayoutService.to_core_project()` no lo traslada a `ProjectConstraints`, y el Core no tiene concepto de kerf), ni `piece_fits_on_board()`, ni la exportación SVG/PDF/DXF — una disposición generada o un fichero exportado asumen corte de anchura cero, así que el material real no cuadrará con el plano si se configuró un kerf. Requiere decidir antes si el kerf pertenece al dominio del Core (afecta a `ProjectConstraints` y a todos los generadores) o se queda como ayuda visual de Studio. Resuelto con `DEC-0016`: se queda fuera del Core y se traduce en Studio. `LayoutService.to_core_project()` entrega cada pieza ensanchada un corte a la derecha y otro abajo, **y el tablero también** — lo segundo cancela lo primero, de modo que N piezas en fila necesitan los N-1 cortes reales y no N (sin ello, una pieza del ancho completo del tablero dejaba de caber, que es el caso más común: cortes transversales). `piece_fits_on_board()`/`find_free_position()` aceptan `kerf_mm` y ensanchan tanto la pieza candidata como sus vecinas, con lo que la separación exigida es exactamente un corte en cualquier dirección. La exportación sigue dibujando las dimensiones reales: el kerf es espacio reservado en el tablero, no parte de la pieza. Aproximación conservadora en dos dimensiones, exacta en una. | 🟢 Resuelto |

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