# Graph Report - .  (2026-07-09)

## Corpus Check
- Corpus is ~32,011 words - fits in a single context window. You may not need a graph.

## Summary
- 1008 nodes · 1910 edges · 75 communities (56 shown, 19 thin omitted)
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 539 edges (avg confidence: 0.78)
- Token cost: 124,217 input · 0 output

## Community Hubs (Navigation)
- Qt Workspace Canvas
- CLI, Presenters & Strategies
- Manifesto & Algorithm Catalog
- Studio Functional Docs & Commands
- Skyline Algorithm Core
- Core Architecture ADRs
- Project Foundational Docs
- Rectangle Geometry
- Masterplan Product & Manifesto Docs
- Studio Commands (Undo/Redo)
- Solver Internal Architecture Docs
- MaxRects Contact Heuristics
- MaxRects Beam Search Variant
- Studio Main Window
- MaxRects Core Algorithm
- MaxRects Free Rectangle
- Board Domain & Candidate Pipeline Tests
- Placement & Collision
- Free Space Generator & Assembly Solution
- Studio Project Manager
- Architecture Docs: Core Layers
- Studio App & Layout Service
- Solver Evaluation & Objectives
- MaxRects Search & Generic Best-Solution Picker
- Domain Package
- Domain Constraints & Data Model Docs
- Sequential Solver
- Board Orderings (shared)
- Studio Board & Piece Models
- Generator Registry & Tests
- Workspace Blueprint ADRs
- Candidate Validation & Dedup
- Skyline Generator
- Architecture Docs: Studio & Commands Citation
- Horizontal/Vertical Generators & Docs
- Candidate Pipeline & Scoring Docs
- Beam Search (generic, orphaned)
- Layout Bounds
- MaxRects Core Algorithm (place/find)
- MaxRects Generator & Tests
- SVG Exporter
- Studio Board Item (Qt)
- MaxRects Candidate Tests
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
1. `Project` - 83 edges
2. `Board` - 72 edges
3. `AssemblySolution` - 70 edges
4. `MaxRects` - 46 edges
5. `BoardPlacement` - 43 edges
6. `ProjectConstraints` - 37 edges
7. `BoardPieceItem` - 31 edges
8. `BoardWorkspace` - 29 edges
9. `MaxRectsPlacement` - 27 edges
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
- `MaxRects — algoritmo geométrico real` --references--> `MaxRects`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/solver_architecture.md → src/boardcomposer/solver/maxrects/maxrects.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BoardComposer Core Principles** — project_philosophy_multiple_solutions, project_philosophy_explainability, project_philosophy_configurable_scoring, project_philosophy_modular_architecture, project_philosophy_ai_complement [EXTRACTED 1.00]
- **BoardComposer Roadmap Phases** — roadmap_fase0_fundamentos, roadmap_fase1_motor_minimo, roadmap_fase2_datos, roadmap_fase3_visualizacion, roadmap_fase4_app_macos [EXTRACTED 1.00]
- **Flujo del pipeline de candidatos** — docs_algorithms_candidate_pipeline, docs_algorithms_generator_registry, docs_scoring_evaluate [EXTRACTED 1.00]
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
- **Cadena de llamadas MaxRects clásico** — docs_solver_architecture_maxrects_family, docs_solver_architecture_search_best_solution, docs_solver_architecture_maxrects_class, docs_solver_architecture_generator_registry [EXTRACTED 1.00]
- **Variante beam search de MaxRects no registrada en producción** — docs_solver_architecture_maxrects_beam_variant, docs_solver_architecture_beam_search_generic, docs_solver_architecture_generator_registry [INFERRED 0.75]
- **Patrón validar-ejecutar-recargar de MainWindow** — docs_studio_placementvalidator, docs_studio_commandmanager, docs_studio_mainwindow [EXTRACTED 1.00]
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (75 total, 19 thin omitted)

### Community 0 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (20): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, BoardPieceItem (+12 more)

### Community 1 - "CLI, Presenters & Strategies"
Cohesion: 0.06
Nodes (43): ABC, CLI (cli.py), Estrategias de optimización (OptimizationStrategy), build_demo_project(), main(), Presenter, JsonPresenter, solutions_to_json() (+35 more)

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

### Community 6 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 7 - "Rectangle Geometry"
Cohesion: 0.10
Nodes (16): Rectangle (primitiva geométrica), Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit() (+8 more)

### Community 8 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 9 - "Studio Commands (Undo/Redo)"
Cohesion: 0.09
Nodes (10): Protocol, Command, CommandManager, Command manager for undo/redo., Stores undo and redo stacks., Base command protocol for Studio undo/redo., DeletePieceCommand, Studio command system. (+2 more)

### Community 10 - "Solver Internal Architecture Docs"
Cohesion: 0.09
Nodes (29): BoardOrdering, Arquitectura interna del Solver, BaseSolver — ABC con solve() abstracto, beam_search.py — beam search genérico independiente del dominio, board_ordering.py — órdenes de tablas compartidos, CandidatePipeline — pipeline de generación/filtrado/puntuación, GENERATOR_REGISTRY — registro de generadores de producción, GeometrySolver — solver de producción (+21 more)

### Community 11 - "MaxRects Contact Heuristics"
Cohesion: 0.14
Nodes (24): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), best_area_fit(), best_bottom_left_fit(), best_long_side_fit() (+16 more)

### Community 12 - "MaxRects Beam Search Variant"
Cohesion: 0.13
Nodes (15): Variante Beam Search de MaxRects, _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, search_states(), score_state(), _beam_candidate(), Heuristic (+7 more)

### Community 13 - "Studio Main Window"
Cohesion: 0.17
Nodes (4): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window.

### Community 14 - "MaxRects Core Algorithm"
Cohesion: 0.14
Nodes (11): MaxRects, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_custom_heuristic_is_used(), test_find_best_rectangle(), test_find_best_rectangle_can_rotate(), test_find_best_rectangle_prefers_less_waste(), test_find_best_rectangle_returns_none_when_it_does_not_fit() (+3 more)

### Community 15 - "MaxRects Free Rectangle"
Cohesion: 0.12
Nodes (13): FreeRectangle, Heuristic, test_free_rectangle_area(), test_free_rectangle_fits_piece(), test_free_rectangle_rejects_large_piece(), test_intersection_detected(), test_intersection_not_detected(), test_resolve_overlaps_removes_free_rectangle_intersections() (+5 more)

### Community 16 - "Board Domain & Candidate Pipeline Tests"
Cohesion: 0.13
Nodes (12): Board, test_candidate_pipeline_returns_ranked_solutions(), test_solutions_to_json_contains_strategy_metadata(), test_generate_horizontal_solution(), test_generate_vertical_solution(), test_generate_horizontal_permutations(), test_generate_vertical_permutations(), test_horizontal_permutations_fallback_when_too_many_boards() (+4 more)

### Community 17 - "Placement & Collision"
Cohesion: 0.16
Nodes (11): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision() (+3 more)

### Community 18 - "Free Space Generator & Assembly Solution"
Cohesion: 0.15
Nodes (12): Generador Free Space, AssemblySolution, generate_free_space_solution(), free_space_generator(), horizontal_generator(), maxrects_generator(), skyline_generator(), vertical_generator() (+4 more)

### Community 19 - "Studio Project Manager"
Cohesion: 0.14
Nodes (6): In-memory project data used by BoardComposer Studio., StudioProject, Project services for BoardComposer Studio., ProjectManager, Project manager for BoardComposer Studio., Owns the currently opened Studio project.

### Community 20 - "Architecture Docs: Core Layers"
Cohesion: 0.12
Nodes (13): Core (src/boardcomposer/), DOC-008 (masterplan, capa API futura), Capa export/, Capa geometry/, Capa io/, Capa layout/, Capa presenters/, Formato de entrada CSV (+5 more)

### Community 21 - "Studio App & Layout Service"
Cohesion: 0.15
Nodes (10): layout_service.py (puente explícito Studio-Core), main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., LayoutService, Bridge between BoardComposer Studio and the core layout engine., Main window for BoardComposer Studio., Application services for BoardComposer Studio. (+2 more)

### Community 22 - "Solver Evaluation & Objectives"
Cohesion: 0.18
Nodes (12): Métricas de puntuación (objectives.py), evaluate(), compactness(), material_utilization(), placed_board_ratio(), rotation_ratio(), test_evaluation_returns_score(), test_compactness() (+4 more)

### Community 23 - "MaxRects Search & Generic Best-Solution Picker"
Cohesion: 0.21
Nodes (12): generate_beam_maxrects_solution(), generate_best_maxrects_solution(), search_best_solution(), generate_best_skyline_solution(), _project(), test_beam_records_selected_heuristic(), test_beam_solution_records_strategy(), test_beam_width_one_matches_classic() (+4 more)

### Community 24 - "Domain Package"
Cohesion: 0.22
Nodes (3): SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 25 - "Domain Constraints & Data Model Docs"
Cohesion: 0.17
Nodes (10): Capa domain/, Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, test_constraints_accept_empty_values(), test_constraints_reject_invalid_max_length(), test_constraints_reject_invalid_max_width() (+2 more)

### Community 26 - "Sequential Solver"
Cohesion: 0.25
Nodes (10): Project, SequentialSolver, test_project_accepts_custom_constraints(), test_project_has_default_constraints(), test_sequential_solver_places_boards_in_sequence(), test_sequential_solver_returns_one_solution(), test_solver_respects_max_width(), test_solver_rotates_board_when_allowed() (+2 more)

### Community 27 - "Board Orderings (shared)"
Cohesion: 0.20
Nodes (11): largest_area_first(), longest_edge_first(), original_order(), _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions(), test_largest_area_first() (+3 more)

### Community 28 - "Studio Board & Piece Models"
Cohesion: 0.22
Nodes (8): Board model for BoardComposer Studio., Piece model for BoardComposer Studio., Piece data used by the Studio workspace., StudioPiece, Placement model for BoardComposer Studio., Placement data for a piece inside a board., StudioPlacement, Project model for BoardComposer Studio.

### Community 29 - "Generator Registry & Tests"
Cohesion: 0.22
Nodes (10): LayoutGenerator, generators_by_name(), _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_generators_by_name(), test_maxrects_generator_is_registered(), test_skyline_generator_is_registered(), _run() (+2 more)

### Community 30 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 31 - "Candidate Validation & Dedup"
Cohesion: 0.22
Nodes (6): respects_constraints(), deduplicate_solutions(), solution_signature(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_deduplicate_solutions_removes_duplicates()

### Community 32 - "Skyline Generator"
Cohesion: 0.24
Nodes (8): generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project., test_skyline_default_width_considers_rotation(), test_skyline_generator_uses_rotation_when_allowed(), test_generate_skyline_solution(), test_skyline_generator_preserves_layout_name(), test_skyline_generator_stacks_when_width_is_limited()

### Community 33 - "Architecture Docs: Studio & Commands Citation"
Cohesion: 0.22
Nodes (10): ADR-003 (EventBus), ADR-008 (patrón Command para undo/redo), main_window.py, BoardComposer Studio (studio/), studio/commands/ (patrón Command: CommandManager, MovePieceCommand, RotatePieceCommand, DeletePieceCommand), studio/events/ (EventBus síncrono), studio/models/ (StudioProject, StudioBoard, StudioPiece, StudioPlacement), studio/project/ (ProjectManager) (+2 more)

### Community 34 - "Horizontal/Vertical Generators & Docs"
Cohesion: 0.42
Nodes (8): Registro de generadores (GENERATOR_REGISTRY), Generadores Horizontal / Vertical (fuerza bruta), SolutionExplanation (dataclass), SolutionExplanation, generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution()

### Community 35 - "Candidate Pipeline & Scoring Docs"
Cohesion: 0.25
Nodes (8): Pipeline de candidatos (CandidatePipeline), Capa solver/, AssemblySolution (dataclass frozen), BoardPlacement (dataclass), SolutionScore (dataclass), Cálculo evaluate(), Reglas de explicación textual, ScoringWeights (scoring_weights.py)

### Community 36 - "Beam Search (generic, orphaned)"
Cohesion: 0.39
Nodes (6): Score, beam_search(), BeamSearchConfig, State, test_beam_search_keeps_best_states(), test_beam_search_stops_when_no_candidates()

### Community 37 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 38 - "MaxRects Core Algorithm (place/find)"
Cohesion: 0.40
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 39 - "MaxRects Generator & Tests"
Cohesion: 0.47
Nodes (4): generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 41 - "Studio Board Item (Qt)"
Cohesion: 0.50
Nodes (4): Board data used by the Studio workspace., StudioBoard, create_board_item(), QGraphicsRectItem

### Community 42 - "MaxRects Candidate Tests"
Cohesion: 0.50
Nodes (3): test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles()

### Community 43 - "CSV Data Requirements"
Cohesion: 0.67
Nodes (3): Data directory (data/samples/: sample CSVs), RF-002 Import from CSV/Excel, CSV input format: id,length_mm,width_mm,thickness_mm

## Ambiguous Edges - Review These
- `Phase 0 - Foundations` → `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/estructura.md · relation: conceptually_related_to
- `DOC-000 — Manifiesto del Proyecto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references

## Knowledge Gaps
- **114 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+109 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Phase 0 - Foundations` and `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `DOC-000 — Manifiesto del Proyecto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `LayoutService` connect `Studio App & Layout Service` to `CLI, Presenters & Strategies`, `Domain Constraints & Data Model Docs`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Why does `Project` connect `Sequential Solver` to `Skyline Generator`, `CLI, Presenters & Strategies`, `Horizontal/Vertical Generators & Docs`, `MaxRects Generator & Tests`, `Solver Internal Architecture Docs`, `MaxRects Beam Search Variant`, `Board Domain & Candidate Pipeline Tests`, `Free Space Generator & Assembly Solution`, `Architecture Docs: Core Layers`, `MaxRects Search & Generic Best-Solution Picker`, `Domain Package`, `Domain Constraints & Data Model Docs`, `Board Orderings (shared)`, `Generator Registry & Tests`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `Board` connect `Board Domain & Candidate Pipeline Tests` to `Skyline Generator`, `CLI, Presenters & Strategies`, `Horizontal/Vertical Generators & Docs`, `Rectangle Geometry`, `MaxRects Generator & Tests`, `Solver Internal Architecture Docs`, `MaxRects Beam Search Variant`, `Architecture Docs: Core Layers`, `MaxRects Search & Generic Best-Solution Picker`, `Domain Package`, `Domain Constraints & Data Model Docs`, `Sequential Solver`, `Board Orderings (shared)`, `Generator Registry & Tests`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `Project` (e.g. with `Board` and `ProjectConstraints`) actually correct?**
  _`Project` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `Board` (e.g. with `build_demo_project()` and `Project`) actually correct?**
  _`Board` has 54 INFERRED edges - model-reasoned connections that need verification._