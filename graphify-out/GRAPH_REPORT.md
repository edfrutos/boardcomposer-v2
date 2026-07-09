# Graph Report - .  (2026-07-09)

## Corpus Check
- Corpus is ~32,111 words - fits in a single context window. You may not need a graph.

## Summary
- 1015 nodes · 1964 edges · 71 communities (52 shown, 19 thin omitted)
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 543 edges (avg confidence: 0.78)
- Token cost: 107,756 input · 0 output

## Community Hubs (Navigation)
- Qt Workspace Canvas
- Architecture Docs: Core Layers & CLI
- Manifesto & Algorithm Catalog
- Studio Functional Docs & Commands
- Skyline Algorithm Core
- Core Architecture ADRs
- Algorithms Docs: Generator Registry
- Project Foundational Docs
- Rectangle Geometry
- Masterplan Product & Manifesto Docs
- Studio Commands (Undo/Redo)
- Beam Search (generic) & MaxRects Beam
- Studio Main Window
- Domain Constraints & Data Model Docs
- MaxRects Free Rectangle
- Placement & Collision
- Project Domain & Free Space Generator
- MaxRects Core Algorithm
- Domain Package
- Candidate Pipeline & Validation
- Studio Main Window & Board Models
- Studio Project Manager
- Board Domain & Ordering
- Assembly Solution & Layout Generator
- MaxRects Contact Heuristics
- MaxRects Heuristics Package
- MaxRects Core Algorithm (place/split/prune)
- Generator Registry & Tests
- Studio App & Layout Service
- Workspace Blueprint ADRs
- Board Orderings (shared)
- Architecture Docs: Studio Bridge
- CSV Loader & Data Format
- Solver Evaluation & Objectives
- MaxRects Beam Runner & Engine
- MaxRects Runner
- Sequential Solver (reference implementation)
- Layout Bounds
- Candidate Pipeline & Scoring Docs
- MaxRects Generator & Tests
- SVG Exporter
- CSV Data Requirements
- Architecture Dependency Rule & DOC-002
- Sample Data Requirement
- Multiple Solutions Requirement
- Configurable Scoring Requirement
- Project Structure: Scripts
- Project Structure: Tests
- Roadmap Phase 3
- Roadmap Phase 4
- Roadmap Phase 5
- Backlog: Export PDF/SVG
- Backlog: Public API
- Backlog: AI Assistant
- Backlog: Plugin System
- Technical Debt Classification
- Technical Debt: Test Coverage (DT-0003)
- Technical Debt: Dead Modules Removed (DT-0004)
- Package Entry Point
- README Current State

## God Nodes (most connected - your core abstractions)
1. `Project` - 85 edges
2. `Board` - 73 edges
3. `AssemblySolution` - 71 edges
4. `MaxRects` - 47 edges
5. `BoardPlacement` - 43 edges
6. `ProjectConstraints` - 37 edges
7. `BoardPieceItem` - 31 edges
8. `BoardWorkspace` - 29 edges
9. `MaxRectsPlacement` - 28 edges
10. `FreeRectangle` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Reglas de explicación textual` --references--> `SolutionExplanation`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/scoring.md → src/boardcomposer/domain/explanation.py
- `BoardPlacement (dataclass)` --documents--> `BoardPlacement`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/placement.py
- `SolutionScore (dataclass)` --documents--> `SolutionScore`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/score.py
- `Capa geometry/` --references--> `Rectangle`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/geometry/rectangle.py
- `Generador Free Space` --references--> `generate_free_space_solution()`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/algorithms.md → src/boardcomposer/solver/free_space_generator.py

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
- **Explicabilidad y confianza como eje transversal (Producto + UX)** — masterplan_doc_001_producto_propuesta_valor, masterplan_doc_001_producto_problema, masterplan_doc_007_ux_studio_objetivos_experiencia [INFERRED 0.85]
- **Command Pattern for Studio Workspace Actions** — masterplan_masterplan_commandmanager, masterplan_masterplan_movepiececommand, masterplan_masterplan_rotatepiececommand [INFERRED 0.85]
- **Arquitectura reactiva y trazable del Core** — adr_adr_003_event_bus_decision, adr_adr_005_timeline_decision, adr_adr_008_arquitectura_basada_en_commands_command_pattern_decision [INFERRED 0.85]
- **Consolidación arquitectónica del Workspace** — adr_adr_010_placementvalidator_decision, adr_adr_011_workspace_blueprint_decision, adr_adr_012_selectioncontroller_decision, adr_adr_013_geometry_engine_decision [INFERRED 0.85]
- **Flujo completo de usuario en BoardComposer Studio** — flows_flw_001_crear_proyecto_flow, flows_flw_002_importar_csv_flow, flows_flw_003_generar_soluciones_flow, flows_flw_004_comparar_flow, flows_flw_005_exportar_flow, flows_flw_006_editar_proyecto_flow [EXTRACTED 1.00]
- **BoardComposer Functional Requirements** — docs_requirements_rf001, docs_requirements_rf002, docs_requirements_rf003, docs_requirements_rf004, docs_requirements_rf005, docs_requirements_rf006 [EXTRACTED 1.00]
- **Implementacion de MaxRects Beam Search** — docs_algorithms_maxrects_beam_search, docs_solver_architecture_maxrects_beam_route, solver_generators_maxrects_beam_generator, solver_maxrects_search_generate_beam_maxrects_solution, solver_maxrects_beam_runner_iter_beam_maxrects_solutions, maxrects_beam_search_states [EXTRACTED 1.00]
- **SequentialSolver como implementacion de referencia (v0.1)** — docs_solver_architecture_sequential_solver, docs_solver_architecture_sequential_solver_rationale, solver_sequential_solver_sequentialsolver [INFERRED 0.85]
- **Patrón validar-ejecutar-recargar de MainWindow** — docs_studio_placementvalidator, docs_studio_commandmanager, docs_studio_mainwindow [EXTRACTED 1.00]
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (71 total, 19 thin omitted)

### Community 0 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 1 - "Architecture Docs: Core Layers & CLI"
Cohesion: 0.05
Nodes (54): ABC, CLI (cli.py), Core (src/boardcomposer/), DOC-008 (masterplan, capa API futura), Capa export/, Capa geometry/, Capa layout/, Capa presenters/ (+46 more)

### Community 2 - "Manifesto & Algorithm Catalog"
Cohesion: 0.06
Nodes (49): BoardComposer Studio, DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), Comparación de algoritmos — todo puede compararse, CP-SAT, Explicabilidad — la explicación forma parte del resultado, MaxRects (algoritmo de optimización) (+41 more)

### Community 3 - "Studio Functional Docs & Commands"
Cohesion: 0.05
Nodes (33): ADR-003 — Event Bus, ADR-010 — Validación de colocación como fuente única de verdad, BoardComposer Studio — documentación funcional, Command — Protocol de undo/redo, CommandManager — pilas de undo/redo, DeletePieceCommand, DragController — arrastre de piezas, EventBus — pub/sub síncrono aún sin conectar (+25 more)

### Community 4 - "Skyline Algorithm Core"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 5 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 6 - "Algorithms Docs: Generator Registry"
Cohesion: 0.08
Nodes (37): Algoritmos (docs/algorithms.md), Trade-off de Beam Search: mas combinaciones heuristica/orden a cambio de mas coste computacional, Generador Free Space, Registro de generadores (GENERATOR_REGISTRY), Generador Horizontal (fuerza bruta), Variante Beam Search de MaxRects (maxrects_beam, beam_width=4), Generador Vertical (fuerza bruta), Arquitectura interna del Solver (docs/solver_architecture.md) (+29 more)

### Community 7 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 8 - "Rectangle Geometry"
Cohesion: 0.10
Nodes (16): Rectangle (primitiva geométrica), Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit() (+8 more)

### Community 9 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 10 - "Studio Commands (Undo/Redo)"
Cohesion: 0.09
Nodes (10): Protocol, Command, CommandManager, Command manager for undo/redo., Stores undo and redo stacks., Base command protocol for Studio undo/redo., DeletePieceCommand, Studio command system. (+2 more)

### Community 11 - "Beam Search (generic) & MaxRects Beam"
Cohesion: 0.12
Nodes (15): Score, beam_search(), BeamSearchConfig, search_states(), score_state(), MaxRectsState, State, test_beam_search_keeps_best_states() (+7 more)

### Community 12 - "Studio Main Window"
Cohesion: 0.17
Nodes (4): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window.

### Community 13 - "Domain Constraints & Data Model Docs"
Cohesion: 0.13
Nodes (15): Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project., test_constraints_accept_empty_values() (+7 more)

### Community 14 - "MaxRects Free Rectangle"
Cohesion: 0.12
Nodes (13): FreeRectangle, Heuristic, test_free_rectangle_area(), test_free_rectangle_fits_piece(), test_free_rectangle_rejects_large_piece(), test_intersection_detected(), test_intersection_not_detected(), test_resolve_overlaps_removes_free_rectangle_intersections() (+5 more)

### Community 15 - "Placement & Collision"
Cohesion: 0.16
Nodes (11): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision() (+3 more)

### Community 16 - "Project Domain & Free Space Generator"
Cohesion: 0.14
Nodes (13): Project, generate_free_space_solution(), free_space_generator(), test_candidate_pipeline_returns_ranked_solutions(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit(), test_generate_horizontal_solution(), test_generate_vertical_solution() (+5 more)

### Community 17 - "MaxRects Core Algorithm"
Cohesion: 0.14
Nodes (14): MaxRects, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles(), test_custom_heuristic_is_used(), test_find_best_rectangle() (+6 more)

### Community 18 - "Domain Package"
Cohesion: 0.20
Nodes (6): Capa domain/, SolutionExplanation (dataclass), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 19 - "Candidate Pipeline & Validation"
Cohesion: 0.14
Nodes (10): Pipeline de candidatos (CandidatePipeline), respects_constraints(), deduplicate_solutions(), solution_signature(), evaluate(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_deduplicate_solutions_removes_duplicates() (+2 more)

### Community 20 - "Studio Main Window & Board Models"
Cohesion: 0.18
Nodes (11): Main window for BoardComposer Studio., Board model for BoardComposer Studio., Board data used by the Studio workspace., StudioBoard, Piece model for BoardComposer Studio., Piece data used by the Studio workspace., StudioPiece, Placement model for BoardComposer Studio. (+3 more)

### Community 21 - "Studio Project Manager"
Cohesion: 0.14
Nodes (6): In-memory project data used by BoardComposer Studio., StudioProject, Project services for BoardComposer Studio., ProjectManager, Project manager for BoardComposer Studio., Owns the currently opened Studio project.

### Community 22 - "Board Domain & Ordering"
Cohesion: 0.15
Nodes (10): Board, largest_area_first(), test_largest_area_first(), test_longest_edge_first(), test_original_order(), test_solutions_to_json_contains_strategy_metadata(), test_board_area(), test_board_requires_positive_dimensions() (+2 more)

### Community 23 - "Assembly Solution & Layout Generator"
Cohesion: 0.18
Nodes (11): AssemblySolution, horizontal_generator(), vertical_generator(), generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution(), test_solution_explanation_accepts_values() (+3 more)

### Community 24 - "MaxRects Contact Heuristics"
Cohesion: 0.29
Nodes (13): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), MaxRectsPlacement, test_contact_score_accumulates_multiple_contacts(), test_contact_score_with_bottom_edge() (+5 more)

### Community 25 - "MaxRects Heuristics Package"
Cohesion: 0.25
Nodes (12): Paquete solver/maxrects/ (logica geometrica), best_area_fit(), best_bottom_left_fit(), best_long_side_fit(), best_short_side_fit(), test_best_area_fit_prefers_less_waste(), test_best_area_fit_returns_none_without_candidates(), test_best_long_side_fit_prefers_shorter_long_side() (+4 more)

### Community 26 - "MaxRects Core Algorithm (place/split/prune)"
Cohesion: 0.22
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 27 - "Generator Registry & Tests"
Cohesion: 0.21
Nodes (11): LayoutGenerator, generators_by_name(), _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_generators_by_name(), test_maxrects_beam_generator_is_registered(), test_maxrects_generator_is_registered(), test_skyline_generator_is_registered() (+3 more)

### Community 28 - "Studio App & Layout Service"
Cohesion: 0.20
Nodes (8): main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., LayoutService, Bridge between BoardComposer Studio and the core layout engine., Application services for BoardComposer Studio., Container for shared Studio services., StudioServices

### Community 29 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 30 - "Board Orderings (shared)"
Cohesion: 0.26
Nodes (8): board_ordering.py: ordenes de tablas compartidos, longest_edge_first(), original_order(), _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions(), test_candidate_orders()

### Community 31 - "Architecture Docs: Studio Bridge"
Cohesion: 0.20
Nodes (11): ADR-003 (EventBus), ADR-008 (patrón Command para undo/redo), layout_service.py (puente explícito Studio-Core), main_window.py, BoardComposer Studio (studio/), studio/commands/ (patrón Command: CommandManager, MovePieceCommand, RotatePieceCommand, DeletePieceCommand), studio/events/ (EventBus síncrono), studio/models/ (StudioProject, StudioBoard, StudioPiece, StudioPlacement) (+3 more)

### Community 32 - "CSV Loader & Data Format"
Cohesion: 0.20
Nodes (7): Capa io/, Formato de entrada CSV, data/samples/basic_boards.csv (ejemplo), Path, main(), load_project_from_csv(), test_load_project_from_csv()

### Community 33 - "Solver Evaluation & Objectives"
Cohesion: 0.29
Nodes (9): Métricas de puntuación (objectives.py), compactness(), material_utilization(), placed_board_ratio(), rotation_ratio(), test_compactness(), test_material_utilization(), test_placed_board_ratio() (+1 more)

### Community 34 - "MaxRects Beam Runner & Engine"
Cohesion: 0.29
Nodes (7): _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, iter_maxrects_candidates(), _project(), test_iter_maxrects_candidates_can_use_beam(), test_iter_maxrects_candidates_uses_classic_candidates_by_default()

### Community 35 - "MaxRects Runner"
Cohesion: 0.31
Nodes (8): BoardOrdering, generate_maxrects_candidate(), _maxrects_size(), _place_all_boards(), Heuristic, _to_board_placement(), _beam_candidate(), Heuristic

### Community 36 - "Sequential Solver (reference implementation)"
Cohesion: 0.36
Nodes (7): SequentialSolver, test_sequential_solver_places_boards_in_sequence(), test_sequential_solver_returns_one_solution(), test_solver_respects_max_width(), test_solver_rotates_board_when_allowed(), test_solver_score_combines_usage_and_waste(), test_solver_wraps_to_next_row_when_length_exceeded()

### Community 37 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 38 - "Candidate Pipeline & Scoring Docs"
Cohesion: 0.33
Nodes (6): Capa solver/, AssemblySolution (dataclass frozen), BoardPlacement (dataclass), SolutionScore (dataclass), Cálculo evaluate(), Reglas de explicación textual

### Community 39 - "MaxRects Generator & Tests"
Cohesion: 0.47
Nodes (4): generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 41 - "CSV Data Requirements"
Cohesion: 0.67
Nodes (3): Data directory (data/samples/: sample CSVs), RF-002 Import from CSV/Excel, CSV input format: id,length_mm,width_mm,thickness_mm

## Ambiguous Edges - Review These
- `Phase 0 - Foundations` → `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/estructura.md · relation: conceptually_related_to
- `DOC-000 — Manifiesto del Proyecto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references

## Knowledge Gaps
- **113 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+108 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Phase 0 - Foundations` and `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `DOC-000 — Manifiesto del Proyecto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `LayoutService` connect `Studio App & Layout Service` to `Architecture Docs: Core Layers & CLI`, `Domain Constraints & Data Model Docs`, `Architecture Docs: Studio Bridge`?**
  _High betweenness centrality (0.300) - this node is a cross-community bridge._
- **Why does `Board` connect `Board Domain & Ordering` to `CSV Loader & Data Format`, `Architecture Docs: Core Layers & CLI`, `MaxRects Beam Runner & Engine`, `MaxRects Runner`, `Sequential Solver (reference implementation)`, `Algorithms Docs: Generator Registry`, `MaxRects Generator & Tests`, `Rectangle Geometry`, `Beam Search (generic) & MaxRects Beam`, `Domain Constraints & Data Model Docs`, `Project Domain & Free Space Generator`, `Domain Package`, `Assembly Solution & Layout Generator`, `Generator Registry & Tests`, `Board Orderings (shared)`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `Project` connect `Project Domain & Free Space Generator` to `CSV Loader & Data Format`, `Architecture Docs: Core Layers & CLI`, `MaxRects Beam Runner & Engine`, `MaxRects Runner`, `Sequential Solver (reference implementation)`, `Algorithms Docs: Generator Registry`, `MaxRects Generator & Tests`, `Domain Constraints & Data Model Docs`, `Domain Package`, `Board Domain & Ordering`, `Assembly Solution & Layout Generator`, `Generator Registry & Tests`, `Board Orderings (shared)`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Project` (e.g. with `Board` and `ProjectConstraints`) actually correct?**
  _`Project` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 55 inferred relationships involving `Board` (e.g. with `build_demo_project()` and `Project`) actually correct?**
  _`Board` has 55 INFERRED edges - model-reasoned connections that need verification._