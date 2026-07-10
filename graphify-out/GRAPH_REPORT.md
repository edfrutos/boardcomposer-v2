# Graph Report - .  (2026-07-10)

## Corpus Check
- Corpus is ~35,948 words - fits in a single context window. You may not need a graph.

## Summary
- 1220 nodes · 2397 edges · 79 communities (64 shown, 15 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 554 edges (avg confidence: 0.78)
- Token cost: 109,230 input · 0 output

## Community Hubs (Navigation)
- Studio Export (SVG/PDF)
- Qt Workspace Canvas
- CLI & CSV Data Format
- Manifesto & Algorithm Catalog
- Skyline Algorithm Core
- Core Architecture ADRs
- Solver Hierarchy & Sequential Solver
- MaxRects Free Rectangle
- Studio App Entry Point
- Project Foundational Docs
- Rectangle Geometry
- Studio Commands (Undo/Redo)
- Beam Search (generic)
- Manifesto Product Docs
- Generator Registry & Board Domain
- Board Ordering & Domain
- MaxRects Beam vs Classic Route
- Candidate Pipeline & Assembly Solution
- Domain Package
- Placement & Collision
- Architecture Docs: API Section & DOC-008
- Domain Explanation & Data Model
- Solver Evaluation & Objectives
- Studio Commands ADRs
- HTTP API (Flask)
- MaxRects Contact Heuristics
- Architecture Docs: Domain & LayoutService
- MaxRects Heuristics Package
- MaxRects Engine & Runner
- Studio Commands ADR Citations
- Backlog & Project Persistence Docs
- Generator Registry & Tests
- Solver Architecture Docs & DT-0002
- MaxRects Core Algorithm (find/place)
- Architecture Docs: Core Package Layers
- Selection Manager
- Workspace Blueprint ADRs
- Free Space Generator & MaxRects Beam Docs
- Studio Export Docs
- Studio Docs: Comparator & Layout Flow
- Studio Docs: DT-0001 & Build System
- Event Bus
- Studio Docs: Panels (Inspector/Comparator)
- Architecture Docs: Core Independence & Manifesto
- Layout Bounds
- Workspace Components (Blueprint)
- Candidate Pipeline & Scoring Docs
- Technical Debt Registry Cross-References
- Technical Debt: Dead Modules Removed (DT-0004)
- MaxRects Generator & Tests
- Skyline Runner
- SVG Exporter (Core)
- Workbench App
- CSV Data Requirements
- Sample Data Requirement
- Multiple Solutions Requirement
- Configurable Scoring Requirement
- Roadmap Phase 2 & Priorities
- Pytest Qt Conftest
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
1. `Project` - 84 edges
2. `AssemblySolution` - 75 edges
3. `Board` - 72 edges
4. `MaxRects` - 47 edges
5. `BoardPlacement` - 44 edges
6. `StudioProject` - 42 edges
7. `ProjectConstraints` - 36 edges
8. `MainWindow` - 31 edges
9. `BoardPieceItem` - 31 edges
10. `StudioPiece` - 29 edges

## Surprising Connections (you probably didn't know these)
- `build_demo_project()` --references--> `build_demo_project()`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/cli.py
- `Board (dataclass)` --documents--> `Board`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/board.py
- `Reglas de explicación textual` --references--> `SolutionExplanation`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/scoring.md → src/boardcomposer/domain/explanation.py
- `BoardPlacement (dataclass)` --documents--> `BoardPlacement`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/placement.py
- `SolutionScore (dataclass)` --documents--> `SolutionScore`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/score.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BoardComposer Core Principles** — project_philosophy_multiple_solutions, project_philosophy_explainability, project_philosophy_configurable_scoring, project_philosophy_modular_architecture, project_philosophy_ai_complement [EXTRACTED 1.00]
- **BoardComposer Roadmap Phases** — roadmap_fase0_fundamentos, roadmap_fase1_motor_minimo, roadmap_fase2_datos, roadmap_fase3_visualizacion, roadmap_fase4_app_macos [EXTRACTED 1.00]
- **Core internal layers (domain/solver/io/export/presenters/geometry/layout)** — docs_architecture_core, docs_architecture_domain, docs_architecture_geometry, docs_architecture_layout, docs_architecture_solver, docs_architecture_io, docs_architecture_export, docs_architecture_presenters [EXTRACTED 1.00]
- **Studio internal submodules** — docs_architecture_studio, docs_architecture_studio_models, docs_architecture_workspace, docs_architecture_commands, docs_architecture_events, docs_architecture_selection, docs_architecture_project_module, docs_architecture_panels, docs_architecture_studio_export, docs_architecture_layout_service, docs_architecture_main_window [EXTRACTED 1.00]
- **API HTTP endpoints** — docs_architecture_api, docs_architecture_health_endpoint, docs_architecture_strategies_endpoint, docs_architecture_solve_endpoint [EXTRACTED 1.00]
- **Composición de AssemblySolution** — docs_data_model_assembly_solution, docs_data_model_board_placement, docs_data_model_solution_score [EXTRACTED 1.00]
- **Optimization Algorithms Compared as a Laboratory** — doc_000_manifiesto_skyline, doc_000_manifiesto_maxrects, doc_000_manifiesto_beam_search, doc_000_manifiesto_algoritmos_geneticos, doc_000_manifiesto_cp_sat [EXTRACTED 1.00]
- **Interfaces consumen el Core mediante APIs públicas** — masterplan_doc_002_arquitectura_core, masterplan_doc_002_arquitectura_studio, masterplan_doc_002_arquitectura_cli, masterplan_doc_002_arquitectura_api [EXTRACTED 1.00]
- **Domain, Solver y Exporters se apoyan en el Geometry Engine** — masterplan_doc_002_arquitectura_domain, masterplan_doc_002_arquitectura_solver, masterplan_doc_002_arquitectura_exporters, masterplan_doc_002_arquitectura_geometry_engine [EXTRACTED 1.00]
- **Backlog initial items IDE-0001..IDE-0008** — masterplan_doc_004_backlog, masterplan_doc_004_backlog_ide_0001, masterplan_doc_004_backlog_ide_0002, masterplan_doc_004_backlog_ide_0003, masterplan_doc_004_backlog_ide_0004, masterplan_doc_004_backlog_ide_0005, masterplan_doc_004_backlog_ide_0006, masterplan_doc_004_backlog_ide_0007, masterplan_doc_004_backlog_ide_0008 [EXTRACTED 1.00]
- **Cobertura de documentación funcional de Studio (DT-0001)** — masterplan_doc_006_deudatecnica_dt_0001, docs_studio_studioservices, docs_studio_projectmanager, docs_studio_commandmanager, docs_studio_selectionmanager, docs_studio_placementvalidator, docs_studio_dragcontroller, docs_studio_layout_resolution_flow, docs_studio_eventbus [EXTRACTED 1.00]
- **Explicabilidad y confianza como eje transversal (Producto + UX)** — masterplan_doc_001_producto_propuesta_valor, masterplan_doc_001_producto_problema, masterplan_doc_007_ux_studio_objetivos_experiencia [INFERRED 0.85]
- **Command Pattern for Studio Workspace Actions** — masterplan_masterplan_commandmanager, masterplan_masterplan_movepiececommand, masterplan_masterplan_rotatepiececommand [INFERRED 0.85]
- **Arquitectura reactiva y trazable del Core** — adr_adr_003_event_bus_decision, adr_adr_005_timeline_decision, adr_adr_008_arquitectura_basada_en_commands_command_pattern_decision [INFERRED 0.85]
- **Consolidación arquitectónica del Workspace** — adr_adr_010_placementvalidator_decision, adr_adr_011_workspace_blueprint_decision, adr_adr_012_selectioncontroller_decision, adr_adr_013_geometry_engine_decision [INFERRED 0.85]
- **Flujo completo de usuario en BoardComposer Studio** — flows_flw_001_crear_proyecto_flow, flows_flw_002_importar_csv_flow, flows_flw_003_generar_soluciones_flow, flows_flw_004_comparar_flow, flows_flw_005_exportar_flow, flows_flw_006_editar_proyecto_flow [EXTRACTED 1.00]
- **BoardComposer Functional Requirements** — docs_requirements_rf001, docs_requirements_rf002, docs_requirements_rf003, docs_requirements_rf004, docs_requirements_rf005, docs_requirements_rf006 [EXTRACTED 1.00]
- **Implementacion de MaxRects Beam Search** — docs_algorithms_maxrects_beam_search, docs_solver_architecture_maxrects_beam_route, solver_generators_maxrects_beam_generator, solver_maxrects_search_generate_beam_maxrects_solution, solver_maxrects_beam_runner_iter_beam_maxrects_solutions, maxrects_beam_search_states [EXTRACTED 1.00]
- **SequentialSolver como implementacion de referencia (v0.1)** — docs_solver_architecture_sequential_solver, docs_solver_architecture_sequential_solver_rationale, solver_sequential_solver_sequentialsolver [INFERRED 0.85]
- **Exportación PDF/SVG feature (IDE-0005, done)** — docs_studio_export, docs_studio_solution_bridge, docs_studio_svg_export, docs_studio_pdf_export, docs_architecture_studio_export, masterplan_doc_004_backlog_ide_0005 [EXTRACTED 1.00]
- **Studio export pipeline: project -> AssemblySolution -> file** — docs_studio_solution_bridge, docs_studio_svg_export, docs_studio_pdf_export, docs_studio_mainwindow_export_actions [EXTRACTED 1.00]
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (79 total, 15 thin omitted)

### Community 0 - "Studio Export (SVG/PDF)"
Cohesion: 0.06
Nodes (57): Export the current Studio workspace state to standalone files (IDE-0005)., export_project_to_pdf(), Path, PDF export for the current Studio workspace state (IDE-0005).  Draws the same re, Bridge from the current Studio workspace state to a Core AssemblySolution.  Pure, studio_project_to_solution(), export_project_to_svg(), Path (+49 more)

### Community 1 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 2 - "CLI & CSV Data Format"
Cohesion: 0.07
Nodes (37): ABC, Formato de entrada CSV, data/samples/basic_boards.csv (ejemplo), build_demo_project(), main(), load_project_from_csv(), Path, Presenter (+29 more)

### Community 3 - "Manifesto & Algorithm Catalog"
Cohesion: 0.06
Nodes (47): BoardComposer Studio, DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), Comparación de algoritmos — todo puede compararse, CP-SAT, Explicabilidad — la explicación forma parte del resultado, MaxRects (algoritmo de optimización) (+39 more)

### Community 4 - "Skyline Algorithm Core"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 5 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 6 - "Solver Hierarchy & Sequential Solver"
Cohesion: 0.09
Nodes (24): BaseSolver (ABC), GeometrySolver (solver de produccion), SequentialSolver, SequentialSolver es el Motor v0.1 original del proyecto; se mantiene como implementacion de referencia, no es codigo muerto, BaseSolver, CandidatePipeline, GeometrySolver, LayoutService (+16 more)

### Community 7 - "MaxRects Free Rectangle"
Cohesion: 0.08
Nodes (27): FreeRectangle, MaxRects, Heuristic, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles() (+19 more)

### Community 8 - "Studio App Entry Point"
Cohesion: 0.09
Nodes (15): QMainWindow, main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., MainWindow, Refresh inspector panel for the selected piece., Main application window., Content builder for the Comparador panel (SCR-003 — Comparador de Soluciones). (+7 more)

### Community 9 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 10 - "Rectangle Geometry"
Cohesion: 0.10
Nodes (16): Rectangle (primitiva geométrica), Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit() (+8 more)

### Community 11 - "Studio Commands (Undo/Redo)"
Cohesion: 0.09
Nodes (10): Protocol, Command, CommandManager, Command manager for undo/redo., Stores undo and redo stacks., Base command protocol for Studio undo/redo., DeletePieceCommand, Studio command system. (+2 more)

### Community 12 - "Beam Search (generic)"
Cohesion: 0.10
Nodes (20): Score, beam_search(), BeamSearchConfig, _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, search_states(), score_state() (+12 more)

### Community 13 - "Manifesto Product Docs"
Cohesion: 0.08
Nodes (30): BoardComposer (Producto), Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor, Usuarios objetivo (6 niveles), API (+22 more)

### Community 14 - "Generator Registry & Board Domain"
Cohesion: 0.14
Nodes (22): Generador Vertical (fuerza bruta), Project, horizontal_generator(), vertical_generator(), generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution() (+14 more)

### Community 15 - "Board Ordering & Domain"
Cohesion: 0.12
Nodes (14): board_ordering.py: ordenes de tablas compartidos, Board, largest_area_first(), longest_edge_first(), original_order(), test_largest_area_first(), test_longest_edge_first(), test_original_order() (+6 more)

### Community 16 - "MaxRects Beam vs Classic Route"
Cohesion: 0.17
Nodes (19): maxrects/beam.py no reutiliza beam_search.py; candidato a revisar si hace falta mantener ambas implementaciones, beam_search.py: implementacion generica de beam search, Ruta MaxRects con Beam Search (maxrects_beam, beam_width=4), Ruta clasica MaxRects (sin beam search), maxrects_engine.py: tercera via de comparacion (workbench/tools), Familia MaxRects (modulos maxrects_*), Por que hay tantos ficheros maxrects_*: crecimiento incremental con cada algoritmo anadido, search.py::search_best_solution(): criterio interno compartido (+11 more)

### Community 17 - "Candidate Pipeline & Assembly Solution"
Cohesion: 0.14
Nodes (12): Pipeline de candidatos (CandidatePipeline), AssemblySolution, respects_constraints(), deduplicate_solutions(), solution_signature(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_deduplicate_solutions_removes_duplicates() (+4 more)

### Community 18 - "Domain Package"
Cohesion: 0.14
Nodes (16): Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, skyline_generator(), generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project. (+8 more)

### Community 19 - "Placement & Collision"
Cohesion: 0.16
Nodes (11): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision() (+3 more)

### Community 20 - "Architecture Docs: API Section & DOC-008"
Cohesion: 0.14
Nodes (19): DOC-008 — API y Extensibilidad, Evaluation (módulo de evaluación de soluciones), API (src/boardcomposer/api.py), API v1 deliberately minimal scope (vs DOC-008-API broader vision), balanced strategy, BoardComposer, build_demo_project(), CandidatePipeline (+11 more)

### Community 21 - "Domain Explanation & Data Model"
Cohesion: 0.21
Nodes (5): SolutionExplanation (dataclass), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 22 - "Solver Evaluation & Objectives"
Cohesion: 0.18
Nodes (12): Métricas de puntuación (objectives.py), evaluate(), compactness(), material_utilization(), placed_board_ratio(), rotation_ratio(), test_evaluation_returns_score(), test_compactness() (+4 more)

### Community 23 - "Studio Commands ADRs"
Cohesion: 0.18
Nodes (16): ADR-003 (Event Bus), ADR-010 (PlacementValidator as source of truth), Command Protocol (name/redo/undo), CommandManager (undo/redo stacks), DeletePieceCommand, DragController (piece drag begin/clear), EventBus (sync pub/sub, unused infrastructure), MovePieceCommand (+8 more)

### Community 24 - "HTTP API (Flask)"
Cohesion: 0.14
Nodes (4): Flask, create_app(), Minimal HTTP API over the Core (IDE-0006 — API pública).  Thin adapter, same rol, client()

### Community 25 - "MaxRects Contact Heuristics"
Cohesion: 0.29
Nodes (13): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), MaxRectsPlacement, test_contact_score_accumulates_multiple_contacts(), test_contact_score_with_bottom_edge() (+5 more)

### Community 26 - "Architecture Docs: Domain & LayoutService"
Cohesion: 0.18
Nodes (15): AssemblySolution, Board, BoardPlacement, domain/ (immutable models), LayoutService (layout_service.py), Project, ProjectConstraints, solution_bridge.py (+7 more)

### Community 27 - "MaxRects Heuristics Package"
Cohesion: 0.25
Nodes (12): Paquete solver/maxrects/ (logica geometrica), best_area_fit(), best_bottom_left_fit(), best_long_side_fit(), best_short_side_fit(), test_best_area_fit_prefers_less_waste(), test_best_area_fit_returns_none_without_candidates(), test_best_long_side_fit_prefers_shorter_long_side() (+4 more)

### Community 28 - "MaxRects Engine & Runner"
Cohesion: 0.22
Nodes (11): BoardOrdering, iter_maxrects_candidates(), generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size(), _place_all_boards(), Heuristic, _to_board_placement() (+3 more)

### Community 29 - "Studio Commands ADR Citations"
Cohesion: 0.14
Nodes (14): ADR-003 (EventBus decoupling), ADR-008 (Command pattern for undo/redo), CommandManager, studio/commands/, DeletePieceCommand, Regla de dependencia (Studio -> Core only, never reverse), EventBus, studio/events/ (+6 more)

### Community 30 - "Backlog & Project Persistence Docs"
Cohesion: 0.14
Nodes (14): project_io.py (.bcstudio.json persistence), studio/project/, ProjectManager, DOC-004 Backlog del Producto, Estado actual del documento: En revisión (pendiente Épicas/Roadmap/flujo Idea-Épica-Sprint-Implementación-Liberación), Estados (Idea/Planificada/En desarrollo/Completada/Bloqueada/Descartada), Formato de una entrada del Backlog, IDE-0004 Gestión de proyectos (Completada, P1) (+6 more)

### Community 31 - "Generator Registry & Tests"
Cohesion: 0.21
Nodes (11): LayoutGenerator, generators_by_name(), _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_generators_by_name(), test_maxrects_beam_generator_is_registered(), test_maxrects_generator_is_registered(), test_skyline_generator_is_registered() (+3 more)

### Community 32 - "Solver Architecture Docs & DT-0002"
Cohesion: 0.15
Nodes (13): Algoritmos (docs/algorithms.md), Arquitectura interna del Solver (docs/solver_architecture.md), Fase 1 — Core (Completada), BaseSolver, DT-0002 Arquitectura interna del Solver (Resuelto), GENERATOR_REGISTRY, GeometrySolver (en producción), maxrects_beam_runner.py (+5 more)

### Community 33 - "MaxRects Core Algorithm (find/place)"
Cohesion: 0.24
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 34 - "Architecture Docs: Core Package Layers"
Cohesion: 0.15
Nodes (11): boardcomposer Core (src/boardcomposer/), export/ (Core SVG export), FreeSpaceManager, geometry/ (Rectangle & collision utilities), io/ (project import), layout/ (free space management), place_board_in_first_space, presenters/ (result formatting) (+3 more)

### Community 35 - "Selection Manager"
Cohesion: 0.19
Nodes (4): Selection services for BoardComposer Studio., Selection manager for BoardComposer Studio., Tracks selected Studio object identifiers., SelectionManager

### Community 36 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 37 - "Free Space Generator & MaxRects Beam Docs"
Cohesion: 0.20
Nodes (9): Trade-off de Beam Search: mas combinaciones heuristica/orden a cambio de mas coste computacional, Generador Free Space, Registro de generadores (GENERATOR_REGISTRY), Generador Horizontal (fuerza bruta), Variante Beam Search de MaxRects (maxrects_beam, beam_width=4), generate_free_space_solution(), free_space_generator(), test_generate_free_space_solution() (+1 more)

### Community 38 - "Studio Export Docs"
Cohesion: 0.25
Nodes (11): pdf_export.py, studio/export/, svg_export.py, tests/conftest.py (QT_QPA_PLATFORM=offscreen), Exportación — studio/export/ (SVG/PDF export feature), IDE-0005 reference in studio.md (Exportación PDF/SVG), pdf_export.py — export_project_to_pdf, solution_bridge.py — studio_project_to_solution (+3 more)

### Community 39 - "Studio Docs: Comparator & Layout Flow"
Cohesion: 0.22
Nodes (10): balanced_strategy (default solve strategy), Comparator panel (render_comparison), Layout resolution flow (solve then apply), LayoutService (bridge to Core), MainWindow (orchestration), MainWindow._export_svg / _export_pdf (Exportar menu actions), material_first_strategy (comparison strategy), MAX_COMPARISON_SOLUTIONS constant (4) (+2 more)

### Community 40 - "Studio Docs: DT-0001 & Build System"
Cohesion: 0.20
Nodes (10): DOC-006-DeudaTecnica.md, DOC-007-UX-Studio.md, docs/studio.md (Studio functional documentation), DT-0001 (technical debt item covered by studio.md), [build-system], DT-0005 pyproject.toml no empaquetaba studio/ correctamente (Resuelto), DT-A — Arquitectura, [tool.setuptools.packages.find] (where = ["src", "."]) (+2 more)

### Community 41 - "Event Bus"
Cohesion: 0.24
Nodes (5): EventHandler, EventBus, Event bus for BoardComposer Studio., Simple synchronous event bus., Event services for BoardComposer Studio.

### Community 42 - "Studio Docs: Panels (Inspector/Comparator)"
Cohesion: 0.22
Nodes (9): comparator_panel.py, inspector_panel.py, studio/panels/, IDE-0002 reference in studio.md (Comparador), IDE-0003 reference in studio.md (Inspector), Inspector panel (render_project/render_board/render_piece), SCR-004-Inspector spec, IDE-0002 Comparador de algoritmos (Completada, P0) (+1 more)

### Community 43 - "Architecture Docs: Core Independence & Manifesto"
Cohesion: 0.32
Nodes (8): Core Independence Principle (Core never depends on any interface), DOC-000 — Manifiesto, DOC-001 — Especificación del Producto, ADR (Architecture Decision Records), DOC-002 — Arquitectura del Sistema, Evolución prevista (Arquitectura), DOC-003 — Roadmap, DOC-004 — Backlog

### Community 44 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 45 - "Workspace Components (Blueprint)"
Cohesion: 0.29
Nodes (7): BoardPieceItem, BoardWorkspace, DragController, PlacementValidator, SelectionController, studio/workspace/, IDE-0001 Workspace interactivo (Completada, P0)

### Community 46 - "Candidate Pipeline & Scoring Docs"
Cohesion: 0.29
Nodes (7): AssemblySolution (dataclass frozen), BoardPlacement (dataclass), SolutionScore (dataclass), Cálculo evaluate(), Reglas de explicación textual, ScoringWeights (scoring_weights.py), Estrategias de optimización (OptimizationStrategy)

### Community 47 - "Technical Debt Registry Cross-References"
Cohesion: 0.29
Nodes (7): ADR relacionados, Gestión de la Deuda Técnica (DOC-006), DOC-002 — Arquitectura, DOC-003 — Roadmap, DOC-005 — Registro de Decisiones, DT-0003 Cobertura de pruebas (Controlado), DT-T — Tests

### Community 48 - "Technical Debt: Dead Modules Removed (DT-0004)"
Cohesion: 0.29
Nodes (6): DT-0004 Módulos runner/adaptador sin uso eliminados (Resuelto), DT-C — Código, solver/generator_utils.py (eliminado), generators.py (envoltorio manual), solver/packing_runner.py (eliminado), single_solution_generator (adaptador)

### Community 49 - "MaxRects Generator & Tests"
Cohesion: 0.38
Nodes (5): maxrects_generator(), generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 50 - "Skyline Runner"
Cohesion: 0.43
Nodes (5): _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions(), test_candidate_orders()

### Community 52 - "Workbench App"
Cohesion: 0.70
Nodes (4): demo_project(), index(), render_solution(), render_svg()

### Community 53 - "CSV Data Requirements"
Cohesion: 0.67
Nodes (3): Data directory (data/samples/: sample CSVs), RF-002 Import from CSV/Excel, CSV input format: id,length_mm,width_mm,thickness_mm

## Ambiguous Edges - Review These
- `Phase 0 - Foundations` → `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/estructura.md · relation: conceptually_related_to
- `DOC-000 — Manifiesto del Proyecto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DT-0002 Arquitectura interna del Solver (Resuelto)` → `Arquitectura interna del Solver (docs/solver_architecture.md)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/solver_architecture.md · relation: references

## Knowledge Gaps
- **156 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Phase 0 - Foundations` and `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `DOC-000 — Manifiesto del Proyecto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DT-0002 Arquitectura interna del Solver (Resuelto)` and `Arquitectura interna del Solver (docs/solver_architecture.md)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `AssemblySolution` connect `Candidate Pipeline & Assembly Solution` to `Studio Export (SVG/PDF)`, `CLI & CSV Data Format`, `Free Space Generator & MaxRects Beam Docs`, `Solver Hierarchy & Sequential Solver`, `Studio App Entry Point`, `Layout Bounds`, `Beam Search (generic)`, `Candidate Pipeline & Scoring Docs`, `Generator Registry & Board Domain`, `MaxRects Beam vs Classic Route`, `MaxRects Generator & Tests`, `Domain Package`, `SVG Exporter (Core)`, `Placement & Collision`, `Domain Explanation & Data Model`, `Solver Evaluation & Objectives`, `Skyline Runner`, `MaxRects Engine & Runner`?**
  _High betweenness centrality (0.283) - this node is a cross-community bridge._
- **Why does `render_comparison()` connect `Studio App Entry Point` to `Studio Export (SVG/PDF)`, `Candidate Pipeline & Assembly Solution`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `GeometrySolver` connect `Solver Hierarchy & Sequential Solver` to `CLI & CSV Data Format`, `Architecture Docs: API Section & DOC-008`, `Board Ordering & Domain`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Project` (e.g. with `Board` and `ProjectConstraints`) actually correct?**
  _`Project` has 38 INFERRED edges - model-reasoned connections that need verification._