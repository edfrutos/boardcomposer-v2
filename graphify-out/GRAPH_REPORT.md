# Graph Report - .  (2026-07-10)

## Corpus Check
- Corpus is ~34,166 words - fits in a single context window. You may not need a graph.

## Summary
- 1112 nodes · 2268 edges · 70 communities (53 shown, 17 thin omitted)
- Extraction: 75% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 552 edges (avg confidence: 0.78)
- Token cost: 101,959 input · 0 output

## Community Hubs (Navigation)
- Solver Hierarchy & Strategies
- Candidate Pipeline & Scoring
- Manifesto & Algorithm Catalog
- Board Domain & Generator Registry
- Studio Docs: Layout Flow & Comparator Rationale
- Skyline Algorithm Core
- Rectangle Geometry & Layout Bounds
- Core Architecture ADRs
- Studio Commands (Undo/Redo)
- MaxRects Beam vs Classic Route
- Project Foundational Docs
- Masterplan Product & Manifesto Docs
- Solver Architecture Docs & DT-0002
- Domain Package
- Architecture Docs: Core Layers & CLI
- Studio Docs: Inspector & MainWindow
- Studio Main Window
- Studio App & Layout Service
- MaxRects Free Rectangle
- Qt Workspace Canvas
- MaxRects Beam Runner
- MaxRects Core Algorithm
- Solver Evaluation & Scoring
- Studio Board Piece Item (Qt)
- Generator Registry & Solver Layer
- Drag Controller & Board Workspace
- Studio Project Manager
- MaxRects Heuristics Package
- MaxRects Contact Heuristics
- MaxRects Beam State & Scoring
- MaxRects Core Algorithm (find/place)
- Placement Validator
- Studio Project Persistence
- Workspace Blueprint ADRs
- Beam Search (generic) & MaxRects Beam Docs
- Geometry Collision & Layout Validation
- Comparator Panel & MainWindow Wiring
- Backlog: Fase 2 Complete (IDE-0001..0004)
- Selection Controller
- Studio Board & Piece Models
- Free Space Generator & Tests
- MaxRects Generator & Tests
- SVG Exporter
- Studio Board Item (Qt)
- CSV Data Requirements
- Architecture Dependency Rule & DOC-002
- Sample Data Requirement
- Multiple Solutions Requirement
- Configurable Scoring Requirement
- Roadmap Phase 2 & Priorities
- Project Structure: Scripts
- Project Structure: Tests
- Roadmap Phase 3
- Roadmap Phase 4
- Roadmap Phase 5
- Technical Debt: Performance
- Technical Debt: UX
- Package Entry Point
- README Current State

## God Nodes (most connected - your core abstractions)
1. `Project` - 85 edges
2. `AssemblySolution` - 75 edges
3. `Board` - 73 edges
4. `MaxRects` - 47 edges
5. `BoardPlacement` - 44 edges
6. `ProjectConstraints` - 37 edges
7. `BoardPieceItem` - 31 edges
8. `MainWindow` - 30 edges
9. `BoardWorkspace` - 29 edges
10. `MaxRectsPlacement` - 28 edges

## Surprising Connections (you probably didn't know these)
- `Capa geometry/` --references--> `Rectangle`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/geometry/rectangle.py
- `CLI (cli.py)` --references--> `build_demo_project()`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/cli.py
- `Capa domain/` --references--> `Board`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/domain/board.py
- `Board (dataclass)` --documents--> `Board`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/board.py
- `ProjectConstraints (dataclass)` --documents--> `ProjectConstraints`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/constraints.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BoardComposer Core Principles** — project_philosophy_multiple_solutions, project_philosophy_explainability, project_philosophy_configurable_scoring, project_philosophy_modular_architecture, project_philosophy_ai_complement [EXTRACTED 1.00]
- **BoardComposer Roadmap Phases** — roadmap_fase0_fundamentos, roadmap_fase1_motor_minimo, roadmap_fase2_datos, roadmap_fase3_visualizacion, roadmap_fase4_app_macos [EXTRACTED 1.00]
- **Puente Studio-Core** — docs_architecture_studio, docs_architecture_layout_service, docs_architecture_core [EXTRACTED 1.00]
- **Composición de AssemblySolution** — docs_data_model_assembly_solution, docs_data_model_board_placement, docs_data_model_solution_score [EXTRACTED 1.00]
- **Optimization Algorithms Compared as a Laboratory** — doc_000_manifiesto_skyline, doc_000_manifiesto_maxrects, doc_000_manifiesto_beam_search, doc_000_manifiesto_algoritmos_geneticos, doc_000_manifiesto_cp_sat [EXTRACTED 1.00]
- **Interfaces consumen el Core mediante APIs públicas** — masterplan_doc_002_arquitectura_core, masterplan_doc_002_arquitectura_studio, masterplan_doc_002_arquitectura_cli, masterplan_doc_002_arquitectura_api [EXTRACTED 1.00]
- **Domain, Solver y Exporters se apoyan en el Geometry Engine** — masterplan_doc_002_arquitectura_domain, masterplan_doc_002_arquitectura_solver, masterplan_doc_002_arquitectura_exporters, masterplan_doc_002_arquitectura_geometry_engine [EXTRACTED 1.00]
- **Fase 2 — ítems P0 del backlog completados** — masterplan_doc_004_backlog_ide_0001, masterplan_doc_004_backlog_ide_0002, masterplan_doc_004_backlog_ide_0003, masterplan_doc_004_backlog_ide_0004, masterplan_doc_004_backlog_fase2_p0 [INFERRED 0.75]
- **Cobertura de documentación funcional de Studio (DT-0001)** — masterplan_doc_006_deudatecnica_dt_0001, docs_studio_studioservices, docs_studio_projectmanager, docs_studio_commandmanager, docs_studio_selectionmanager, docs_studio_placementvalidator, docs_studio_dragcontroller, docs_studio_layout_resolution_flow, docs_studio_eventbus [EXTRACTED 1.00]
- **Explicabilidad y confianza como eje transversal (Producto + UX)** — masterplan_doc_001_producto_propuesta_valor, masterplan_doc_001_producto_problema, masterplan_doc_007_ux_studio_objetivos_experiencia [INFERRED 0.85]
- **Command Pattern for Studio Workspace Actions** — masterplan_masterplan_commandmanager, masterplan_masterplan_movepiececommand, masterplan_masterplan_rotatepiececommand [INFERRED 0.85]
- **Arquitectura reactiva y trazable del Core** — adr_adr_003_event_bus_decision, adr_adr_005_timeline_decision, adr_adr_008_arquitectura_basada_en_commands_command_pattern_decision [INFERRED 0.85]
- **Consolidación arquitectónica del Workspace** — adr_adr_010_placementvalidator_decision, adr_adr_011_workspace_blueprint_decision, adr_adr_012_selectioncontroller_decision, adr_adr_013_geometry_engine_decision [INFERRED 0.85]
- **Flujo completo de usuario en BoardComposer Studio** — flows_flw_001_crear_proyecto_flow, flows_flw_002_importar_csv_flow, flows_flw_003_generar_soluciones_flow, flows_flw_004_comparar_flow, flows_flw_005_exportar_flow, flows_flw_006_editar_proyecto_flow [EXTRACTED 1.00]
- **BoardComposer Functional Requirements** — docs_requirements_rf001, docs_requirements_rf002, docs_requirements_rf003, docs_requirements_rf004, docs_requirements_rf005, docs_requirements_rf006 [EXTRACTED 1.00]
- **Implementacion de MaxRects Beam Search** — docs_algorithms_maxrects_beam_search, docs_solver_architecture_maxrects_beam_route, solver_generators_maxrects_beam_generator, solver_maxrects_search_generate_beam_maxrects_solution, solver_maxrects_beam_runner_iter_beam_maxrects_solutions, maxrects_beam_search_states [EXTRACTED 1.00]
- **SequentialSolver como implementacion de referencia (v0.1)** — docs_solver_architecture_sequential_solver, docs_solver_architecture_sequential_solver_rationale, solver_sequential_solver_sequentialsolver [INFERRED 0.85]
- **Comparador de soluciones (comparator_panel + LayoutService + material_first_strategy) implementa IDE-0002** — docs_studio_comparator_panel, docs_studio_layoutservice, docs_studio_material_first_strategy, masterplan_doc_004_backlog_ide_0002 [EXTRACTED 1.00]
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (70 total, 17 thin omitted)

### Community 0 - "Solver Hierarchy & Strategies"
Cohesion: 0.06
Nodes (45): ABC, Estrategias de optimización (OptimizationStrategy), BaseSolver (ABC), GeometrySolver (solver de produccion), SequentialSolver, SequentialSolver es el Motor v0.1 original del proyecto; se mantiene como implementacion de referencia, no es codigo muerto, build_demo_project(), main() (+37 more)

### Community 1 - "Candidate Pipeline & Scoring"
Cohesion: 0.07
Nodes (30): Pipeline de candidatos (CandidatePipeline), AssemblySolution (dataclass frozen), BoardPlacement (dataclass), Métricas de puntuación (objectives.py), BoardPlacement, AssemblySolution, respects_constraints(), deduplicate_solutions() (+22 more)

### Community 2 - "Manifesto & Algorithm Catalog"
Cohesion: 0.06
Nodes (49): BoardComposer Studio, DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), Comparación de algoritmos — todo puede compararse, CP-SAT, Explicabilidad — la explicación forma parte del resultado, MaxRects (algoritmo de optimización) (+41 more)

### Community 3 - "Board Domain & Generator Registry"
Cohesion: 0.09
Nodes (32): LayoutGenerator, Board, Project, generators_by_name(), SequentialSolver, _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_candidate_pipeline_returns_ranked_solutions() (+24 more)

### Community 4 - "Studio Docs: Layout Flow & Comparator Rationale"
Cohesion: 0.07
Nodes (32): balanced_strategy — estrategia por defecto de solve_current_project, Rationale: calcular-antes-de-aplicar es intencional, dos operaciones distintas sin ApplyLayoutCommand en el undo/redo, Rationale: SCR-003 pide número de cortes, tiempo de cálculo, fragmentación y tiempo de mecanizado; ninguno se calcula en el dominio actual, se omiten con nota explícita en vez de inventarse; tampoco hay miniaturas gráficas ni 'fijar como favorita', Comparador de soluciones (comparator_panel) — render_comparison, tabla HTML de comparación, BoardComposer Studio — documentación funcional, EventBus — pub/sub síncrono, Generador free_space, Generador horizontal (+24 more)

### Community 5 - "Skyline Algorithm Core"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 6 - "Rectangle Geometry & Layout Bounds"
Cohesion: 0.07
Nodes (19): Rectangle (primitiva geométrica), Rectangle, bounding_rectangle(), FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_bounding_rectangle(), test_bounding_rectangle_empty() (+11 more)

### Community 7 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 8 - "Studio Commands (Undo/Redo)"
Cohesion: 0.08
Nodes (16): Command — Protocol con name/redo/undo, Rationale: los comandos no validan colisiones por sí mismos; la validación (PlacementValidator) ocurre antes de ejecutar el comando, CommandManager — pilas de undo/redo, DeletePieceCommand, MovePieceCommand, RotatePieceCommand, Protocol, Command (+8 more)

### Community 9 - "MaxRects Beam vs Classic Route"
Cohesion: 0.09
Nodes (32): maxrects/beam.py no reutiliza beam_search.py; candidato a revisar si hace falta mantener ambas implementaciones, beam_search.py: implementacion generica de beam search, Ruta MaxRects con Beam Search (maxrects_beam, beam_width=4), Ruta clasica MaxRects (sin beam search), maxrects_engine.py: tercera via de comparacion (workbench/tools), Familia MaxRects (modulos maxrects_*), Por que hay tantos ficheros maxrects_*: crecimiento incremental con cada algoritmo anadido, board_ordering.py: ordenes de tablas compartidos (+24 more)

### Community 10 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 11 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 12 - "Solver Architecture Docs & DT-0002"
Cohesion: 0.06
Nodes (32): Algoritmos (docs/algorithms.md), Arquitectura interna del Solver (docs/solver_architecture.md), Fase 1 — Core (Completada), ADR relacionados, BaseSolver, [build-system], Gestión de la Deuda Técnica (DOC-006), DOC-002 — Arquitectura (+24 more)

### Community 13 - "Domain Package"
Cohesion: 0.10
Nodes (19): Capa domain/, Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project. (+11 more)

### Community 14 - "Architecture Docs: Core Layers & CLI"
Cohesion: 0.08
Nodes (24): ADR-003 (EventBus), ADR-008 (patrón Command para undo/redo), CLI (cli.py), Core (src/boardcomposer/), DOC-008 (masterplan, capa API futura), Capa export/, Capa geometry/, Capa io/ (+16 more)

### Community 15 - "Studio Docs: Inspector & MainWindow"
Cohesion: 0.21
Nodes (21): Rationale: campos de SCR-004 no soportados por el modelo de datos actual (descripción/fecha de proyecto, espesor, restricciones) se omiten en vez de rellenarse con valores inventados, Inspector contextual (inspector_panel) — render_project/render_board/render_piece/render_empty, Main window for BoardComposer Studio., Board data used by the Studio workspace., StudioBoard, Piece data used by the Studio workspace., StudioPiece, Placement data for a piece inside a board. (+13 more)

### Community 16 - "Studio Main Window"
Cohesion: 0.18
Nodes (4): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window.

### Community 17 - "Studio App & Layout Service"
Cohesion: 0.15
Nodes (13): main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., LayoutService, Bridge between BoardComposer Studio and the core layout engine., Application services for BoardComposer Studio., Container for shared Studio services., StudioServices (+5 more)

### Community 18 - "MaxRects Free Rectangle"
Cohesion: 0.12
Nodes (13): FreeRectangle, Heuristic, test_free_rectangle_area(), test_free_rectangle_fits_piece(), test_free_rectangle_rejects_large_piece(), test_intersection_detected(), test_intersection_not_detected(), test_resolve_overlaps_removes_free_rectangle_intersections() (+5 more)

### Community 19 - "Qt Workspace Canvas"
Cohesion: 0.16
Nodes (6): QGraphicsView, QMouseEvent, QPoint, QWheelEvent, BoardWorkspace, QPointF

### Community 20 - "MaxRects Beam Runner"
Cohesion: 0.15
Nodes (16): BoardOrdering, _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, iter_maxrects_candidates(), generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size() (+8 more)

### Community 21 - "MaxRects Core Algorithm"
Cohesion: 0.14
Nodes (14): MaxRects, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles(), test_custom_heuristic_is_used(), test_find_best_rectangle() (+6 more)

### Community 22 - "Solver Evaluation & Scoring"
Cohesion: 0.18
Nodes (9): SolutionExplanation (dataclass), SolutionScore (dataclass), Cálculo evaluate(), Reglas de explicación textual, ScoringWeights (scoring_weights.py), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values() (+1 more)

### Community 23 - "Studio Board Piece Item (Qt)"
Cohesion: 0.16
Nodes (4): QGraphicsRectItem, BoardPieceItem, create_piece_item(), apply_selection()

### Community 24 - "Generator Registry & Solver Layer"
Cohesion: 0.16
Nodes (14): Registro de generadores (GENERATOR_REGISTRY), Generador Horizontal (fuerza bruta), Generador Vertical (fuerza bruta), Capa solver/, horizontal_generator(), maxrects_beam_generator(), skyline_generator(), vertical_generator() (+6 more)

### Community 25 - "Drag Controller & Board Workspace"
Cohesion: 0.17
Nodes (7): DragController — arrastre de piezas, Rationale: DragController deliberadamente mínimo, evita comandos de undo/redo vacíos cuando no hubo movimiento real, QGraphicsScene, Interactive board workspace for BoardComposer Studio., DragController, add_grid(), WorkspaceCamera

### Community 26 - "Studio Project Manager"
Cohesion: 0.14
Nodes (5): In-memory project data used by BoardComposer Studio., StudioProject, ProjectManager, Project manager for BoardComposer Studio., Owns the currently opened Studio project.

### Community 27 - "MaxRects Heuristics Package"
Cohesion: 0.23
Nodes (12): Paquete solver/maxrects/ (logica geometrica), best_area_fit(), best_bottom_left_fit(), best_long_side_fit(), best_short_side_fit(), test_best_area_fit_prefers_less_waste(), test_best_area_fit_returns_none_without_candidates(), test_best_long_side_fit_prefers_shorter_long_side() (+4 more)

### Community 28 - "MaxRects Contact Heuristics"
Cohesion: 0.29
Nodes (13): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), MaxRectsPlacement, test_contact_score_accumulates_multiple_contacts(), test_contact_score_with_bottom_edge() (+5 more)

### Community 29 - "MaxRects Beam State & Scoring"
Cohesion: 0.18
Nodes (8): score_state(), MaxRectsState, test_search_states_places_board(), test_score_state_prefers_more_placements(), test_clone_creates_independent_state(), test_expand_creates_child_states(), test_expand_returns_one_child_per_candidate(), test_state_can_be_created()

### Community 30 - "MaxRects Core Algorithm (find/place)"
Cohesion: 0.22
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 31 - "Placement Validator"
Cohesion: 0.33
Nodes (5): PlacementValidator — única fuente de verdad para colocar/rotar piezas, QRectF, PlacementValidator, QPointF, Única fuente de verdad para validar colocaciones.

### Community 32 - "Studio Project Persistence"
Cohesion: 0.34
Nodes (11): Persistencia de proyecto (project_io) — serialización y ficheros .bcstudio.json, Project services for BoardComposer Studio., load_project_from_file(), project_from_dict(), project_to_dict(), Path, JSON persistence for BoardComposer Studio projects., save_project_to_file() (+3 more)

### Community 33 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 34 - "Beam Search (generic) & MaxRects Beam Docs"
Cohesion: 0.24
Nodes (9): Trade-off de Beam Search: mas combinaciones heuristica/orden a cambio de mas coste computacional, Variante Beam Search de MaxRects (maxrects_beam, beam_width=4), Score, beam_search(), BeamSearchConfig, search_states(), State, test_beam_search_keeps_best_states() (+1 more)

### Community 35 - "Geometry Collision & Layout Validation"
Cohesion: 0.24
Nodes (7): placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision()

### Community 36 - "Comparator Panel & MainWindow Wiring"
Cohesion: 0.35
Nodes (8): Content builder for the Comparador panel (SCR-003 — Comparador de Soluciones)., render_comparison(), _row(), _solution(), test_render_comparison_includes_strengths_and_weaknesses(), test_render_comparison_notes_missing_metrics_are_not_fabricated(), test_render_comparison_shows_one_column_per_solution(), test_render_comparison_with_no_solutions_explains_how_to_generate()

### Community 37 - "Backlog: Fase 2 Complete (IDE-0001..0004)"
Cohesion: 0.27
Nodes (10): DOC-004 — Backlog del Producto, Fase 2 — ítems P0 completados (IDE-0001..IDE-0004 todos 🟢), IDE-0001 — Workspace interactivo (🟢 Completada, P0), IDE-0002 — Comparador de algoritmos (🟢 Completada, P0), IDE-0003 — Inspector de piezas (🟢 Completada, P0), IDE-0004 — Gestión de proyectos (🟢 Completada, P1), IDE-0005 — Exportación PDF/SVG (🔵 Planificada, P1), IDE-0006 — API pública (⚪ Idea, P2) (+2 more)

### Community 39 - "Studio Board & Piece Models"
Cohesion: 0.31
Nodes (4): Board model for BoardComposer Studio., Piece model for BoardComposer Studio., Placement model for BoardComposer Studio., Project model for BoardComposer Studio.

### Community 40 - "Free Space Generator & Tests"
Cohesion: 0.33
Nodes (5): Generador Free Space, generate_free_space_solution(), free_space_generator(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit()

### Community 41 - "MaxRects Generator & Tests"
Cohesion: 0.38
Nodes (5): maxrects_generator(), generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 44 - "CSV Data Requirements"
Cohesion: 0.67
Nodes (3): Data directory (data/samples/: sample CSVs), RF-002 Import from CSV/Excel, CSV input format: id,length_mm,width_mm,thickness_mm

## Ambiguous Edges - Review These
- `Phase 0 - Foundations` → `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/estructura.md · relation: conceptually_related_to
- `DOC-000 — Manifiesto del Proyecto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DT-0002 Arquitectura interna del Solver (Resuelto)` → `Arquitectura interna del Solver (docs/solver_architecture.md)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/solver_architecture.md · relation: references
- `SCR-003 — Comparador de Soluciones` → `Comparador de soluciones (comparator_panel) — render_comparison, tabla HTML de comparación`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/studio.md · relation: conceptually_related_to
- `SCR-004 — Inspector Contextual` → `Inspector contextual (inspector_panel) — render_project/render_board/render_piece/render_empty`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/studio.md · relation: conceptually_related_to

## Knowledge Gaps
- **130 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+125 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Phase 0 - Foundations` and `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `DOC-000 — Manifiesto del Proyecto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DT-0002 Arquitectura interna del Solver (Resuelto)` and `Arquitectura interna del Solver (docs/solver_architecture.md)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `SCR-003 — Comparador de Soluciones` and `Comparador de soluciones (comparator_panel) — render_comparison, tabla HTML de comparación`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `SCR-004 — Inspector Contextual` and `Inspector contextual (inspector_panel) — render_project/render_board/render_piece/render_empty`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `AssemblySolution` connect `Candidate Pipeline & Scoring` to `Solver Hierarchy & Strategies`, `Comparator Panel & MainWindow Wiring`, `Rectangle Geometry & Layout Bounds`, `Free Space Generator & Tests`, `MaxRects Generator & Tests`, `SVG Exporter`, `MaxRects Beam vs Classic Route`, `Domain Package`, `Studio App & Layout Service`, `MaxRects Beam Runner`, `Solver Evaluation & Scoring`, `Generator Registry & Solver Layer`?**
  _High betweenness centrality (0.346) - this node is a cross-community bridge._
- **Why does `render_comparison()` connect `Comparator Panel & MainWindow Wiring` to `Studio Main Window`, `Candidate Pipeline & Scoring`, `Studio Docs: Layout Flow & Comparator Rationale`, `Studio Docs: Inspector & MainWindow`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._