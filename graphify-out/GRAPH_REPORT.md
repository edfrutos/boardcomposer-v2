# Graph Report - .  (2026-07-08)

## Corpus Check
- Corpus is ~30,168 words - fits in a single context window. You may not need a graph.

## Summary
- 987 nodes · 1888 edges · 69 communities (60 shown, 9 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 543 edges (avg confidence: 0.78)
- Token cost: 72,622 input · 0 output

## Community Hubs (Navigation)
- Qt Workspace Canvas
- CLI, Presenters & Strategies
- Skyline Algorithm & Docs
- Core Architecture ADRs
- Project Foundational Docs
- Rectangle Geometry & Data Model Docs
- Masterplan Product & Manifesto Docs
- Studio Commands (Undo/Redo)
- Architecture Docs: Core Layers & Studio Bridge
- MaxRects Contact Heuristics
- Studio Main Window
- Assembly Solution & Candidate Validation
- Placement & Collision
- MaxRects Free Rectangle
- Board Domain & Ordering
- MaxRects Core Algorithm
- Solver Search Strategies
- Studio Main Window & Board Models
- MaxRects Beam State & Scoring
- Domain Package & Explanation Docs
- Studio Project Manager
- SCR-007 Export Screen
- Manifesto Algorithm Catalog & Decisions Index
- Horizontal/Vertical Generators & Docs
- Domain Constraints & Data Model Docs
- Studio App & Layout Service
- Backlog Items & UI Screens Catalog
- Technical Debt Registry (DOC-006)
- Sequential Solver
- Solver Evaluation & Objectives
- Generator Registry & Tests
- Selection Manager
- Workspace Blueprint ADRs
- Free Space Generator & Generator Registry
- MaxRects Core Algorithm (place/split/prune)
- Skyline Generator
- Event Bus
- MASTERPLAN.md Current Block
- MaxRects Beam Runner & Engine
- Roadmap Phases & Future Ideas
- MaxRects Runner
- Beam Search (generic)
- Layout Bounds
- Candidate Pipeline & Scoring Docs
- Skyline Runner (board orderings)
- SVG Exporter
- CSV Data Requirements
- Architecture Dependency Rule & DOC-002
- Sample Data Requirement
- Multiple Solutions Requirement
- Configurable Scoring Requirement
- Project Structure: Scripts
- Project Structure: Tests
- Package Entry Point
- README Current State

## God Nodes (most connected - your core abstractions)
1. `Project` - 83 edges
2. `Board` - 72 edges
3. `AssemblySolution` - 70 edges
4. `MaxRects` - 45 edges
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
- `CLI (cli.py)` --references--> `build_demo_project()`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/cli.py

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
- **Registro inicial de deuda técnica (DT-0001 a DT-0004)** — masterplan_doc_006_deudatecnica_dt_0001, masterplan_doc_006_deudatecnica_dt_0002, masterplan_doc_006_deudatecnica_dt_0003, masterplan_doc_006_deudatecnica_dt_0004 [EXTRACTED 1.00]
- **Clasificación de categorías de deuda técnica** — masterplan_doc_006_deudatecnica_dt_a_arquitectura, masterplan_doc_006_deudatecnica_dt_c_codigo, masterplan_doc_006_deudatecnica_dt_t_tests, masterplan_doc_006_deudatecnica_dt_d_documentacion, masterplan_doc_006_deudatecnica_dt_p_rendimiento, masterplan_doc_006_deudatecnica_dt_ux_experiencia_usuario [EXTRACTED 1.00]
- **Explicabilidad y confianza como eje transversal (Producto + UX)** — masterplan_doc_001_producto_propuesta_valor, masterplan_doc_001_producto_problema, masterplan_doc_007_ux_studio_objetivos_experiencia [INFERRED 0.85]
- **Command Pattern for Studio Workspace Actions** — masterplan_masterplan_commandmanager, masterplan_masterplan_movepiececommand, masterplan_masterplan_rotatepiececommand [INFERRED 0.85]
- **Arquitectura reactiva y trazable del Core** — adr_adr_003_event_bus_decision, adr_adr_005_timeline_decision, adr_adr_008_arquitectura_basada_en_commands_command_pattern_decision [INFERRED 0.85]
- **Consolidación arquitectónica del Workspace** — adr_adr_010_placementvalidator_decision, adr_adr_011_workspace_blueprint_decision, adr_adr_012_selectioncontroller_decision, adr_adr_013_geometry_engine_decision [INFERRED 0.85]
- **Flujo completo de usuario en BoardComposer Studio** — flows_flw_001_crear_proyecto_flow, flows_flw_002_importar_csv_flow, flows_flw_003_generar_soluciones_flow, flows_flw_004_comparar_flow, flows_flw_005_exportar_flow, flows_flw_006_editar_proyecto_flow [EXTRACTED 1.00]
- **BoardComposer Functional Requirements** — docs_requirements_rf001, docs_requirements_rf002, docs_requirements_rf003, docs_requirements_rf004, docs_requirements_rf005, docs_requirements_rf006 [EXTRACTED 1.00]
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (69 total, 9 thin omitted)

### Community 0 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 1 - "CLI, Presenters & Strategies"
Cohesion: 0.06
Nodes (43): ABC, Estrategias de optimización (OptimizationStrategy), build_demo_project(), main(), Presenter, JsonPresenter, solutions_to_json(), solution_to_text() (+35 more)

### Community 2 - "Skyline Algorithm & Docs"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 3 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 4 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 5 - "Rectangle Geometry & Data Model Docs"
Cohesion: 0.10
Nodes (16): Rectangle (primitiva geométrica), Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit() (+8 more)

### Community 6 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 7 - "Studio Commands (Undo/Redo)"
Cohesion: 0.09
Nodes (10): Protocol, Command, CommandManager, Command manager for undo/redo., Stores undo and redo stacks., Base command protocol for Studio undo/redo., DeletePieceCommand, Studio command system. (+2 more)

### Community 8 - "Architecture Docs: Core Layers & Studio Bridge"
Cohesion: 0.07
Nodes (25): ADR-003 (EventBus), ADR-008 (patrón Command para undo/redo), CLI (cli.py), Core (src/boardcomposer/), DOC-008 (masterplan, capa API futura), Capa export/, Capa geometry/, Capa io/ (+17 more)

### Community 9 - "MaxRects Contact Heuristics"
Cohesion: 0.15
Nodes (24): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), best_area_fit(), best_bottom_left_fit(), best_long_side_fit() (+16 more)

### Community 10 - "Studio Main Window"
Cohesion: 0.17
Nodes (4): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window.

### Community 11 - "Assembly Solution & Candidate Validation"
Cohesion: 0.13
Nodes (12): AssemblySolution, respects_constraints(), deduplicate_solutions(), solution_signature(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_deduplicate_solutions_removes_duplicates(), test_evaluation_returns_score() (+4 more)

### Community 12 - "Placement & Collision"
Cohesion: 0.14
Nodes (12): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision() (+4 more)

### Community 13 - "MaxRects Free Rectangle"
Cohesion: 0.12
Nodes (13): FreeRectangle, Heuristic, test_free_rectangle_area(), test_free_rectangle_fits_piece(), test_free_rectangle_rejects_large_piece(), test_intersection_detected(), test_intersection_not_detected(), test_resolve_overlaps_removes_free_rectangle_intersections() (+5 more)

### Community 14 - "Board Domain & Ordering"
Cohesion: 0.15
Nodes (12): Board, largest_area_first(), longest_edge_first(), original_order(), test_largest_area_first(), test_longest_edge_first(), test_original_order(), test_candidate_pipeline_returns_ranked_solutions() (+4 more)

### Community 15 - "MaxRects Core Algorithm"
Cohesion: 0.14
Nodes (14): MaxRects, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles(), test_custom_heuristic_is_used(), test_find_best_rectangle() (+6 more)

### Community 16 - "Solver Search Strategies"
Cohesion: 0.18
Nodes (14): _beam_candidate(), generate_beam_maxrects_solution(), generate_best_maxrects_solution(), Heuristic, search_best_solution(), generate_best_skyline_solution(), _project(), test_beam_records_selected_heuristic() (+6 more)

### Community 17 - "Studio Main Window & Board Models"
Cohesion: 0.17
Nodes (11): Main window for BoardComposer Studio., Board model for BoardComposer Studio., Board data used by the Studio workspace., StudioBoard, Piece model for BoardComposer Studio., Piece data used by the Studio workspace., StudioPiece, Placement model for BoardComposer Studio. (+3 more)

### Community 18 - "MaxRects Beam State & Scoring"
Cohesion: 0.16
Nodes (10): Variante Beam Search de MaxRects, search_states(), score_state(), MaxRectsState, test_search_states_places_board(), test_score_state_prefers_more_placements(), test_clone_creates_independent_state(), test_expand_creates_child_states() (+2 more)

### Community 19 - "Domain Package & Explanation Docs"
Cohesion: 0.21
Nodes (5): SolutionExplanation (dataclass), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 20 - "Studio Project Manager"
Cohesion: 0.14
Nodes (6): In-memory project data used by BoardComposer Studio., StudioProject, Project services for BoardComposer Studio., ProjectManager, Project manager for BoardComposer Studio., Owns the currently opened Studio project.

### Community 21 - "SCR-007 Export Screen"
Cohesion: 0.16
Nodes (17): BoardComposer Studio, Criterios de aceptación, Evolución prevista, Flujo principal de exportación, Formato CSV, Formato DXF, Formato Imagen (PNG/JPEG), Formato JSON (+9 more)

### Community 22 - "Manifesto Algorithm Catalog & Decisions Index"
Cohesion: 0.16
Nodes (16): DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), CP-SAT, MaxRects (algoritmo de optimización), Skyline (algoritmo de optimización), Fase 1 — Core (Completada), IDE-0006 — API pública (+8 more)

### Community 23 - "Horizontal/Vertical Generators & Docs"
Cohesion: 0.18
Nodes (13): Registro de generadores (GENERATOR_REGISTRY), Generadores Horizontal / Vertical (fuerza bruta), Capa solver/, vertical_generator(), generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution() (+5 more)

### Community 24 - "Domain Constraints & Data Model Docs"
Cohesion: 0.18
Nodes (12): Capa domain/, Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, generate_maxrects_solution(), test_constraints_accept_empty_values(), test_constraints_reject_invalid_max_length() (+4 more)

### Community 25 - "Studio App & Layout Service"
Cohesion: 0.19
Nodes (8): main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., LayoutService, Bridge between BoardComposer Studio and the core layout engine., Application services for BoardComposer Studio., Container for shared Studio services., StudioServices

### Community 26 - "Backlog Items & UI Screens Catalog"
Cohesion: 0.26
Nodes (14): Explicabilidad — la explicación forma parte del resultado, Fase 2 — BoardComposer Studio (En curso), DOC-004 — Backlog del Producto, IDE-0001 — Workspace interactivo, IDE-0002 — Comparador de algoritmos, IDE-0003 — Inspector de piezas, IDE-0004 — Gestión de proyectos, IDE-0005 — Exportación PDF/SVG (+6 more)

### Community 27 - "Technical Debt Registry (DOC-006)"
Cohesion: 0.20
Nodes (14): ADR relacionados (referencia genérica), DOC-006 — Gestión de la Deuda Técnica, DT-0001 — Completar documentación funcional de BoardComposer Studio (Pendiente), DT-0002 — Revisar y documentar arquitectura interna del Solver tras nuevos algoritmos (Pendiente), DT-0003 — Mantener cobertura de pruebas por encima del objetivo definido (Controlado), DT-0004 — Eliminación de módulos solver sin uso: solver/packing_runner.py (runner+selector genérico, commit 8feea6b) y solver/generator_utils.py (adaptador single_solution_generator, commit ab7b963), tras adoptarse CandidatePipeline/evaluate() y el envoltorio manual de generators.py (Resuelto), DT-A — Arquitectura (problemas de diseño estructural), DT-C — Código (duplicación, complejidad, refactor pendiente) (+6 more)

### Community 28 - "Sequential Solver"
Cohesion: 0.27
Nodes (10): Project, SequentialSolver, test_project_accepts_custom_constraints(), test_project_has_default_constraints(), test_sequential_solver_places_boards_in_sequence(), test_sequential_solver_returns_one_solution(), test_solver_respects_max_width(), test_solver_rotates_board_when_allowed() (+2 more)

### Community 29 - "Solver Evaluation & Objectives"
Cohesion: 0.27
Nodes (10): Métricas de puntuación (objectives.py), evaluate(), compactness(), material_utilization(), placed_board_ratio(), rotation_ratio(), test_compactness(), test_material_utilization() (+2 more)

### Community 30 - "Generator Registry & Tests"
Cohesion: 0.22
Nodes (10): LayoutGenerator, generators_by_name(), _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_generators_by_name(), test_maxrects_generator_is_registered(), test_skyline_generator_is_registered(), _run() (+2 more)

### Community 31 - "Selection Manager"
Cohesion: 0.19
Nodes (4): Selection services for BoardComposer Studio., Selection manager for BoardComposer Studio., Tracks selected Studio object identifiers., SelectionManager

### Community 32 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 33 - "Free Space Generator & Generator Registry"
Cohesion: 0.20
Nodes (8): Generador Free Space, generate_free_space_solution(), free_space_generator(), horizontal_generator(), maxrects_generator(), skyline_generator(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit()

### Community 34 - "MaxRects Core Algorithm (place/split/prune)"
Cohesion: 0.22
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 35 - "Skyline Generator"
Cohesion: 0.24
Nodes (8): generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project., test_skyline_default_width_considers_rotation(), test_skyline_generator_uses_rotation_when_allowed(), test_generate_skyline_solution(), test_skyline_generator_preserves_layout_name(), test_skyline_generator_stacks_when_width_is_limited()

### Community 36 - "Event Bus"
Cohesion: 0.24
Nodes (5): EventHandler, EventBus, Event bus for BoardComposer Studio., Simple synchronous event bus., Event services for BoardComposer Studio.

### Community 37 - "MASTERPLAN.md Current Block"
Cohesion: 0.24
Nodes (10): MASTERPLAN — Estado del Proyecto, ADR-010, ADR-011, ADR-012, BoardWorkspace, CommandManager, MovePieceCommand, PlacementValidator (+2 more)

### Community 38 - "MaxRects Beam Runner & Engine"
Cohesion: 0.29
Nodes (7): _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, iter_maxrects_candidates(), _project(), test_iter_maxrects_candidates_can_use_beam(), test_iter_maxrects_candidates_uses_classic_candidates_by_default()

### Community 39 - "Roadmap Phases & Future Ideas"
Cohesion: 0.22
Nodes (9): Comparación de algoritmos — todo puede compararse, DOC-003 — Roadmap del Producto, Asistencia mediante IA, Fase 3 — Plataforma, Fase 4 — Inteligencia, Fase 5 — Ecosistema, Plugins, IDE-0007 — Asistente IA (+1 more)

### Community 40 - "MaxRects Runner"
Cohesion: 0.39
Nodes (7): BoardOrdering, generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size(), _place_all_boards(), Heuristic, _to_board_placement()

### Community 41 - "Beam Search (generic)"
Cohesion: 0.39
Nodes (6): Score, beam_search(), BeamSearchConfig, State, test_beam_search_keeps_best_states(), test_beam_search_stops_when_no_candidates()

### Community 42 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 43 - "Candidate Pipeline & Scoring Docs"
Cohesion: 0.29
Nodes (7): Pipeline de candidatos (CandidatePipeline), AssemblySolution (dataclass frozen), BoardPlacement (dataclass), SolutionScore (dataclass), Cálculo evaluate(), Reglas de explicación textual, ScoringWeights (scoring_weights.py)

### Community 44 - "Skyline Runner (board orderings)"
Cohesion: 0.43
Nodes (5): _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions(), test_candidate_orders()

### Community 46 - "CSV Data Requirements"
Cohesion: 0.67
Nodes (3): Data directory (data/samples/: sample CSVs), RF-002 Import from CSV/Excel, CSV input format: id,length_mm,width_mm,thickness_mm

## Ambiguous Edges - Review These
- `Phase 0 - Foundations` → `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/estructura.md · relation: conceptually_related_to
- `DOC-000 — Manifiesto del Proyecto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-003 — Roadmap del Producto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references
- `DOC-004 — Backlog del Producto` → `DOC-005 — Registro de Decisiones`  [AMBIGUOUS]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/masterplan/DOC-005-Decisiones.md · relation: references

## Knowledge Gaps
- **94 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+89 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Phase 0 - Foundations` and `Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `DOC-000 — Manifiesto del Proyecto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-003 — Roadmap del Producto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `DOC-004 — Backlog del Producto` and `DOC-005 — Registro de Decisiones`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `LayoutService` connect `Studio App & Layout Service` to `Architecture Docs: Core Layers & Studio Bridge`, `CLI, Presenters & Strategies`, `Studio Main Window & Board Models`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Why does `Board` connect `Board Domain & Ordering` to `CLI, Presenters & Strategies`, `Free Space Generator & Generator Registry`, `Skyline Generator`, `Rectangle Geometry & Data Model Docs`, `MaxRects Beam Runner & Engine`, `Architecture Docs: Core Layers & Studio Bridge`, `MaxRects Runner`, `Skyline Runner (board orderings)`, `Solver Search Strategies`, `MaxRects Beam State & Scoring`, `Domain Package & Explanation Docs`, `Horizontal/Vertical Generators & Docs`, `Domain Constraints & Data Model Docs`, `Studio App & Layout Service`, `Sequential Solver`, `Generator Registry & Tests`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Why does `Project` connect `Sequential Solver` to `CLI, Presenters & Strategies`, `Free Space Generator & Generator Registry`, `Skyline Generator`, `MaxRects Beam Runner & Engine`, `Architecture Docs: Core Layers & Studio Bridge`, `MaxRects Runner`, `Skyline Runner (board orderings)`, `Board Domain & Ordering`, `Solver Search Strategies`, `Domain Package & Explanation Docs`, `Horizontal/Vertical Generators & Docs`, `Domain Constraints & Data Model Docs`, `Studio App & Layout Service`, `Generator Registry & Tests`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._