# Graph Report - .  (2026-07-08)

## Corpus Check
- Corpus is ~28,581 words - fits in a single context window. You may not need a graph.

## Summary
- 906 nodes · 1793 edges · 60 communities (52 shown, 8 thin omitted)
- Extraction: 69% EXTRACTED · 30% INFERRED · 1% AMBIGUOUS · INFERRED: 542 edges (avg confidence: 0.78)
- Token cost: 362,428 input · 0 output

## Community Hubs (Navigation)
- Qt Workspace Canvas
- Manifesto & Algorithm Comparison
- CLI & Presenters
- Skyline Algorithm Core
- Core Architecture ADRs
- Packing Runner & Commands
- Project Foundational Docs
- Geometry & Free Space
- MaxRects Contact Heuristics
- MaxRects Core Algorithm
- Studio Main Window
- MaxRects Free Rectangle
- Board Domain & Candidate Pipeline
- Placement & Collision
- Constraints & Skyline Generator
- Studio App & Layout Service
- Domain Package
- Assembly Solution & Layout Generator
- MaxRects Beam State & Scoring
- Solver Search Strategies
- Studio Project Manager
- Solver Evaluation & Objectives
- Board Ordering & Skyline Runner
- Sequential Solver
- Studio Board & Piece Models
- Generator Registry & Tests
- Selection Manager
- Workspace Blueprint ADRs
- Beam Search
- Candidate Validation & Dedup
- MaxRects Runner
- Event Bus
- Free Space Generator
- CSV Loader & Project Check
- Layout Bounds
- MaxRects Engine
- MaxRects Generator
- SVG Exporter
- Generator Utils Protocol
- CSV Data Requirements
- Sample Data Requirement
- Multiple Solutions Requirement
- Configurable Scoring Requirement
- Project Structure: Scripts
- Project Structure: Tests
- Package Entry Point
- README Current State

## God Nodes (most connected - your core abstractions)
1. `Project` - 81 edges
2. `Board` - 72 edges
3. `AssemblySolution` - 68 edges
4. `MaxRects` - 45 edges
5. `BoardPlacement` - 43 edges
6. `ProjectConstraints` - 35 edges
7. `BoardPieceItem` - 31 edges
8. `BoardWorkspace` - 29 edges
9. `MaxRectsPlacement` - 27 edges
10. `FreeRectangle` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Principle: modular architecture` --semantically_similar_to--> `Decision: core independent of PySide6/files/AI`  [INFERRED] [semantically similar]
  PROJECT_PHILOSOPHY.md → DECISIONS.md
- `test_cli_project_constraints_from_cli_options()` --calls--> `ProjectConstraints`  [INFERRED]
  tests/test_cli.py → src/boardcomposer/domain/constraints.py
- `Vision: professional tool exploring thousands of board-assembly combinations, evolving toward AI, visual analysis and CAD export` --semantically_similar_to--> `BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms`  [INFERRED] [semantically similar]
  docs/vision.md → AI_CONTEXT.md
- `Initial scope: flat 2D composition, rectangular boards, mm measurements, UI-independent engine, console output` --semantically_similar_to--> `Decision: start with 2D flat assembly of rectangular boards`  [INFERRED] [semantically similar]
  NOTEBOOK.md → DECISIONS.md
- `Initial scope: flat 2D composition, rectangular boards, mm measurements, UI-independent engine, console output` --semantically_similar_to--> `Decision: core independent of PySide6/files/AI`  [INFERRED] [semantically similar]
  NOTEBOOK.md → DECISIONS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BoardComposer Core Principles** — project_philosophy_multiple_solutions, project_philosophy_explainability, project_philosophy_configurable_scoring, project_philosophy_modular_architecture, project_philosophy_ai_complement [EXTRACTED 1.00]
- **BoardComposer Roadmap Phases** — roadmap_fase0_fundamentos, roadmap_fase1_motor_minimo, roadmap_fase2_datos, roadmap_fase3_visualizacion, roadmap_fase4_app_macos [EXTRACTED 1.00]
- **BoardComposer Functional Requirements** — docs_requirements_rf001, docs_requirements_rf002, docs_requirements_rf003, docs_requirements_rf004, docs_requirements_rf005, docs_requirements_rf006 [EXTRACTED 1.00]
- **Core Architecture Layers** — docs_masterplan_doc_002_arquitectura_core, docs_masterplan_doc_002_arquitectura_domain, docs_masterplan_doc_002_arquitectura_solver, docs_masterplan_doc_002_arquitectura_exporters, docs_masterplan_doc_002_arquitectura_geometry_engine [EXTRACTED 1.00]
- **Optimization Algorithms Compared as a Laboratory** — docs_masterplan_doc_000_manifiesto_skyline, docs_masterplan_doc_000_manifiesto_maxrects, docs_masterplan_doc_000_manifiesto_beam_search, docs_masterplan_doc_000_manifiesto_algoritmos_geneticos, docs_masterplan_doc_000_manifiesto_cp_sat [EXTRACTED 1.00]
- **Command Pattern for Studio Workspace Actions** — docs_masterplan_masterplan_commandmanager, docs_masterplan_masterplan_movepiececommand, docs_masterplan_masterplan_rotatepiececommand [INFERRED 0.85]
- **Consolidación arquitectónica del Workspace** — docs_masterplan_adr_adr_010_placementvalidator_decision, docs_masterplan_adr_adr_011_workspace_blueprint_decision, docs_masterplan_adr_adr_012_selectioncontroller_decision, docs_masterplan_adr_adr_013_geometry_engine_decision [INFERRED 0.85]
- **Arquitectura reactiva y trazable del Core** — docs_masterplan_adr_adr_003_event_bus_decision, docs_masterplan_adr_adr_005_timeline_decision, docs_masterplan_adr_adr_008_arquitectura_basada_en_commands_command_pattern_decision [INFERRED 0.85]
- **Flujo completo de usuario en BoardComposer Studio** — docs_masterplan_ui_flows_flw_001_crear_proyecto_flow, docs_masterplan_ui_flows_flw_002_importar_csv_flow, docs_masterplan_ui_flows_flw_003_generar_soluciones_flow, docs_masterplan_ui_flows_flw_004_comparar_flow, docs_masterplan_ui_flows_flw_005_exportar_flow, docs_masterplan_ui_flows_flw_006_editar_proyecto_flow [EXTRACTED 1.00]

## Communities (60 total, 8 thin omitted)

### Community 0 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 1 - "Manifesto & Algorithm Comparison"
Cohesion: 0.06
Nodes (67): DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), Comparación de algoritmos — todo puede compararse, CP-SAT, Explicabilidad — la explicación forma parte del resultado, MaxRects (algoritmo de optimización), Skyline (algoritmo de optimización) (+59 more)

### Community 2 - "CLI & Presenters"
Cohesion: 0.07
Nodes (40): ABC, build_demo_project(), main(), Presenter, JsonPresenter, solutions_to_json(), solution_to_text(), TextPresenter (+32 more)

### Community 3 - "Skyline Algorithm Core"
Cohesion: 0.07
Nodes (20): SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost(), test_prefers_less_fragmented_candidate() (+12 more)

### Community 4 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 5 - "Packing Runner & Commands"
Cohesion: 0.08
Nodes (15): Protocol, PackingAlgorithm, place_all_boards(), PlacementLike, to_board_placement(), Command, CommandManager, Command manager for undo/redo. (+7 more)

### Community 6 - "Project Foundational Docs"
Cohesion: 0.06
Nodes (42): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), docs/algorithms.md (currently empty placeholder), docs/architecture.md (currently empty placeholder) (+34 more)

### Community 7 - "Geometry & Free Space"
Cohesion: 0.10
Nodes (15): Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit(), test_free_space_fits_rectangle() (+7 more)

### Community 8 - "MaxRects Contact Heuristics"
Cohesion: 0.12
Nodes (26): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), best_area_fit(), best_bottom_left_fit(), best_long_side_fit() (+18 more)

### Community 9 - "MaxRects Core Algorithm"
Cohesion: 0.11
Nodes (14): MaxRects, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles(), test_custom_heuristic_is_used(), test_find_best_rectangle() (+6 more)

### Community 10 - "Studio Main Window"
Cohesion: 0.17
Nodes (4): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window.

### Community 11 - "MaxRects Free Rectangle"
Cohesion: 0.12
Nodes (13): FreeRectangle, Heuristic, test_free_rectangle_area(), test_free_rectangle_fits_piece(), test_free_rectangle_rejects_large_piece(), test_intersection_detected(), test_intersection_not_detected(), test_resolve_overlaps_removes_free_rectangle_intersections() (+5 more)

### Community 12 - "Board Domain & Candidate Pipeline"
Cohesion: 0.12
Nodes (12): Board, test_candidate_pipeline_returns_ranked_solutions(), test_solutions_to_json_contains_strategy_metadata(), test_generate_horizontal_solution(), test_generate_vertical_solution(), test_generate_horizontal_permutations(), test_generate_vertical_permutations(), test_horizontal_permutations_fallback_when_too_many_boards() (+4 more)

### Community 13 - "Placement & Collision"
Cohesion: 0.16
Nodes (11): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision() (+3 more)

### Community 14 - "Constraints & Skyline Generator"
Cohesion: 0.16
Nodes (13): ProjectConstraints, generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project., test_constraints_accept_empty_values(), test_constraints_reject_invalid_max_length(), test_constraints_reject_invalid_max_width(), test_geometry_solver_respects_constraints() (+5 more)

### Community 15 - "Studio App & Layout Service"
Cohesion: 0.15
Nodes (10): main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., LayoutService, Bridge between BoardComposer Studio and the core layout engine., Placement data for a piece inside a board., StudioPlacement, Application services for BoardComposer Studio. (+2 more)

### Community 16 - "Domain Package"
Cohesion: 0.23
Nodes (4): SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 17 - "Assembly Solution & Layout Generator"
Cohesion: 0.18
Nodes (11): AssemblySolution, horizontal_generator(), vertical_generator(), generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution(), test_solution_explanation_accepts_values() (+3 more)

### Community 18 - "MaxRects Beam State & Scoring"
Cohesion: 0.17
Nodes (10): _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, score_state(), MaxRectsState, test_score_state_prefers_more_placements(), test_clone_creates_independent_state(), test_expand_creates_child_states() (+2 more)

### Community 19 - "Solver Search Strategies"
Cohesion: 0.21
Nodes (12): generate_beam_maxrects_solution(), generate_best_maxrects_solution(), search_best_solution(), generate_best_skyline_solution(), _project(), test_beam_records_selected_heuristic(), test_beam_solution_records_strategy(), test_beam_width_one_matches_classic() (+4 more)

### Community 20 - "Studio Project Manager"
Cohesion: 0.15
Nodes (6): In-memory project data used by BoardComposer Studio., StudioProject, Project services for BoardComposer Studio., ProjectManager, Project manager for BoardComposer Studio., Owns the currently opened Studio project.

### Community 21 - "Solver Evaluation & Objectives"
Cohesion: 0.17
Nodes (11): evaluate(), compactness(), material_utilization(), placed_board_ratio(), rotation_ratio(), test_evaluation_returns_score(), test_compactness(), test_material_utilization() (+3 more)

### Community 22 - "Board Ordering & Skyline Runner"
Cohesion: 0.20
Nodes (11): largest_area_first(), longest_edge_first(), original_order(), _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions(), test_largest_area_first() (+3 more)

### Community 23 - "Sequential Solver"
Cohesion: 0.27
Nodes (10): Project, SequentialSolver, test_project_accepts_custom_constraints(), test_project_has_default_constraints(), test_sequential_solver_places_boards_in_sequence(), test_sequential_solver_returns_one_solution(), test_solver_respects_max_width(), test_solver_rotates_board_when_allowed() (+2 more)

### Community 24 - "Studio Board & Piece Models"
Cohesion: 0.22
Nodes (8): Board model for BoardComposer Studio., Board data used by the Studio workspace., StudioBoard, Piece model for BoardComposer Studio., Piece data used by the Studio workspace., StudioPiece, Placement model for BoardComposer Studio., Project model for BoardComposer Studio.

### Community 25 - "Generator Registry & Tests"
Cohesion: 0.22
Nodes (10): generators_by_name(), LayoutGenerator, _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_generators_by_name(), test_maxrects_generator_is_registered(), test_skyline_generator_is_registered(), _run() (+2 more)

### Community 26 - "Selection Manager"
Cohesion: 0.19
Nodes (4): Selection services for BoardComposer Studio., Selection manager for BoardComposer Studio., Tracks selected Studio object identifiers., SelectionManager

### Community 27 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 28 - "Beam Search"
Cohesion: 0.24
Nodes (8): Score, beam_search(), BeamSearchConfig, search_states(), State, test_beam_search_keeps_best_states(), test_beam_search_stops_when_no_candidates(), test_search_states_places_board()

### Community 29 - "Candidate Validation & Dedup"
Cohesion: 0.22
Nodes (6): respects_constraints(), deduplicate_solutions(), solution_signature(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_deduplicate_solutions_removes_duplicates()

### Community 30 - "MaxRects Runner"
Cohesion: 0.29
Nodes (9): BoardOrdering, generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size(), _place_all_boards(), Heuristic, _to_board_placement(), _beam_candidate() (+1 more)

### Community 31 - "Event Bus"
Cohesion: 0.24
Nodes (5): EventHandler, EventBus, Event bus for BoardComposer Studio., Simple synchronous event bus., Event services for BoardComposer Studio.

### Community 32 - "Free Space Generator"
Cohesion: 0.25
Nodes (6): generate_free_space_solution(), free_space_generator(), maxrects_generator(), skyline_generator(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit()

### Community 33 - "CSV Loader & Project Check"
Cohesion: 0.29
Nodes (4): Path, main(), load_project_from_csv(), test_load_project_from_csv()

### Community 34 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 35 - "MaxRects Engine"
Cohesion: 0.53
Nodes (4): iter_maxrects_candidates(), _project(), test_iter_maxrects_candidates_can_use_beam(), test_iter_maxrects_candidates_uses_classic_candidates_by_default()

### Community 36 - "MaxRects Generator"
Cohesion: 0.47
Nodes (4): generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 38 - "Generator Utils Protocol"
Cohesion: 0.50
Nodes (3): SolutionGenerator, LayoutGenerator, single_solution_generator()

### Community 39 - "CSV Data Requirements"
Cohesion: 0.67
Nodes (3): Data directory (data/samples/: sample CSVs), RF-002 Import from CSV/Excel, CSV input format: id,length_mm,width_mm,thickness_mm

## Ambiguous Edges - Review These
- `Phase 0 - Foundations` → `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`  [AMBIGUOUS]
  docs/estructura.md · relation: conceptually_related_to
- `DOC-000 — Manifiesto del Proyecto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-001-Manifiesto.md (contiene el contenido de Especificación del Producto, duplicado)` → `DOC-003 — Roadmap del Producto`  [AMBIGUOUS]
  docs/masterplan/DOC-001-Manifiesto.md · relation: references
- `DOC-001-Manifiesto.md (contiene el contenido de Especificación del Producto, duplicado)` → `DOC-004 — Backlog del Producto`  [AMBIGUOUS]
  docs/masterplan/DOC-001-Manifiesto.md · relation: references
- `DOC-001 — Especificación del Producto` → `DOC-003 — Roadmap del Producto`  [AMBIGUOUS]
  docs/masterplan/DOC-001-Producto.md · relation: references
- `DOC-001 — Especificación del Producto` → `DOC-004 — Backlog del Producto`  [AMBIGUOUS]
  docs/masterplan/DOC-001-Producto.md · relation: references
- `DOC-001 — Especificación del Producto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-002 — Arquitectura del Sistema` → `DOC-003 — Roadmap del Producto`  [AMBIGUOUS]
  docs/masterplan/DOC-002-Arquitectura.md · relation: references
- `DOC-002 — Arquitectura del Sistema` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-003 — Roadmap del Producto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-004 — Backlog del Producto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-007 — UX / BoardComposer Studio` → `SCR-005 — Gestión del Proyecto`  [AMBIGUOUS]
  docs/masterplan/DOC-007-UX-Studio.md · relation: references

## Knowledge Gaps
- **50 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Phase 0 - Foundations` and `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `DOC-000 — Manifiesto del Proyecto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-001-Manifiesto.md (contiene el contenido de Especificación del Producto, duplicado)` and `DOC-003 — Roadmap del Producto`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-001-Manifiesto.md (contiene el contenido de Especificación del Producto, duplicado)` and `DOC-004 — Backlog del Producto`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-001 — Especificación del Producto` and `DOC-003 — Roadmap del Producto`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-001 — Especificación del Producto` and `DOC-004 — Backlog del Producto`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-001 — Especificación del Producto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._