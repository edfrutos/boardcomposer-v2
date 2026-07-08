# Graph Report - .  (2026-07-08)

## Corpus Check
- Corpus is ~30,259 words - fits in a single context window. You may not need a graph.

## Summary
- 987 nodes · 1891 edges · 69 communities (59 shown, 10 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 542 edges (avg confidence: 0.78)
- Token cost: 176,712 input · 0 output

## Community Hubs (Navigation)
- Qt Workspace Canvas
- Skyline Algorithm & Docs
- Rectangle Geometry & Bounds
- Core Architecture ADRs
- Domain Constraints & Data Model Docs
- Assembly Solution & Scoring Docs
- Packing Runner & Commands
- MaxRects Beam Search & Docs
- Project Foundational Docs
- Masterplan Product & Manifesto Docs
- Board Domain & Ordering
- MaxRects Core Algorithm
- Studio Main Window
- Architecture Docs: Studio & ADR Citations
- MaxRects Free Rectangle
- MaxRects Beam Runner & Engine
- Domain Package & Explanation Docs
- Studio Main Window & Board Models
- Studio Project Manager
- Solver Strategies & Presenters Tests
- Manifesto Algorithm Catalog
- Placement & Constraints Validator
- MaxRects Contact Heuristics
- Architecture Docs: Core Layers
- Studio App & Layout Service
- Horizontal/Vertical Generators & Docs
- Presenters & JSON Output
- MaxRects Heuristics
- Selection Manager
- Workspace Blueprint ADRs
- Geometry Collision & Layout Validation
- Candidate Pipeline & Geometry Solver
- SCR-007 Export Screen
- Backlog Items
- CLI & Architecture Docs
- Event Bus
- MASTERPLAN.md Current Block
- Roadmap Phases
- MaxRects Placement Ops
- Scoring Weights Presets
- UI Screens Catalog (SCR-001..004)
- Free Space Generator & Docs
- Skyline Runner
- SCR-007 Export Formats
- Base Solver & Sequential Solver
- SVG Exporter
- Generator Utils Protocol
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
2. `Board` - 74 edges
3. `AssemblySolution` - 70 edges
4. `BoardPlacement` - 45 edges
5. `MaxRects` - 45 edges
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
- `Capa domain/` --references--> `Board`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/architecture.md → src/boardcomposer/domain/board.py

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
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (69 total, 10 thin omitted)

### Community 0 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 1 - "Skyline Algorithm & Docs"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 2 - "Rectangle Geometry & Bounds"
Cohesion: 0.07
Nodes (19): Rectangle (primitiva geométrica), Rectangle, bounding_rectangle(), FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_bounding_rectangle(), test_bounding_rectangle_empty() (+11 more)

### Community 3 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 4 - "Domain Constraints & Data Model Docs"
Cohesion: 0.09
Nodes (32): Capa domain/, Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, Project, generate_maxrects_solution(), SequentialSolver (+24 more)

### Community 5 - "Assembly Solution & Scoring Docs"
Cohesion: 0.08
Nodes (25): Métricas de puntuación (objectives.py), AssemblySolution, deduplicate_solutions(), solution_signature(), evaluate(), horizontal_generator(), maxrects_generator(), skyline_generator() (+17 more)

### Community 6 - "Packing Runner & Commands"
Cohesion: 0.08
Nodes (14): Protocol, PackingAlgorithm, place_all_boards(), PlacementLike, to_board_placement(), Command, CommandManager, Command manager for undo/redo. (+6 more)

### Community 7 - "MaxRects Beam Search & Docs"
Cohesion: 0.08
Nodes (26): Variante Beam Search de MaxRects, Score, beam_search(), BeamSearchConfig, search_states(), score_state(), _beam_candidate(), generate_beam_maxrects_solution() (+18 more)

### Community 8 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 9 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 10 - "Board Domain & Ordering"
Cohesion: 0.10
Nodes (22): Board, largest_area_first(), longest_edge_first(), original_order(), generators_by_name(), LayoutGenerator, _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline() (+14 more)

### Community 11 - "MaxRects Core Algorithm"
Cohesion: 0.12
Nodes (14): MaxRects, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles(), test_custom_heuristic_is_used(), test_find_best_rectangle() (+6 more)

### Community 12 - "Studio Main Window"
Cohesion: 0.17
Nodes (4): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window.

### Community 13 - "Architecture Docs: Studio & ADR Citations"
Cohesion: 0.10
Nodes (18): ADR-003 (EventBus), ADR-008 (patrón Command para undo/redo), Capa io/, layout_service.py (puente explícito Studio-Core), main_window.py, BoardComposer Studio (studio/), studio/commands/ (patrón Command: CommandManager, MovePieceCommand, RotatePieceCommand, DeletePieceCommand), studio/events/ (EventBus síncrono) (+10 more)

### Community 14 - "MaxRects Free Rectangle"
Cohesion: 0.12
Nodes (13): FreeRectangle, Heuristic, test_free_rectangle_area(), test_free_rectangle_fits_piece(), test_free_rectangle_rejects_large_piece(), test_intersection_detected(), test_intersection_not_detected(), test_resolve_overlaps_removes_free_rectangle_intersections() (+5 more)

### Community 15 - "MaxRects Beam Runner & Engine"
Cohesion: 0.17
Nodes (14): BoardOrdering, _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, iter_maxrects_candidates(), generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size() (+6 more)

### Community 16 - "Domain Package & Explanation Docs"
Cohesion: 0.21
Nodes (5): SolutionExplanation (dataclass), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 17 - "Studio Main Window & Board Models"
Cohesion: 0.18
Nodes (11): Main window for BoardComposer Studio., Board model for BoardComposer Studio., Board data used by the Studio workspace., StudioBoard, Piece model for BoardComposer Studio., Piece data used by the Studio workspace., StudioPiece, Placement model for BoardComposer Studio. (+3 more)

### Community 18 - "Studio Project Manager"
Cohesion: 0.14
Nodes (6): In-memory project data used by BoardComposer Studio., StudioProject, Project services for BoardComposer Studio., ProjectManager, Project manager for BoardComposer Studio., Owns the currently opened Studio project.

### Community 19 - "Solver Strategies & Presenters Tests"
Cohesion: 0.16
Nodes (12): balanced_strategy(), compact_first_strategy(), material_first_strategy(), test_solutions_to_json_contains_strategy_metadata(), test_material_strategy_enables_skyline_generator(), test_balanced_strategy(), test_compact_first_strategy(), test_material_first_strategy() (+4 more)

### Community 20 - "Manifesto Algorithm Catalog"
Cohesion: 0.16
Nodes (16): DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), CP-SAT, MaxRects (algoritmo de optimización), Skyline (algoritmo de optimización), Fase 1 — Core (Completada), IDE-0006 — API pública (+8 more)

### Community 21 - "Placement & Constraints Validator"
Cohesion: 0.16
Nodes (8): BoardPlacement, respects_constraints(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_board_placement_area(), test_board_placement_bounds(), test_board_placement_rejects_negative_position(), test_custom_scoring_weights()

### Community 22 - "MaxRects Contact Heuristics"
Cohesion: 0.29
Nodes (13): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), MaxRectsPlacement, test_contact_score_accumulates_multiple_contacts(), test_contact_score_with_bottom_edge() (+5 more)

### Community 23 - "Architecture Docs: Core Layers"
Cohesion: 0.13
Nodes (15): Pipeline de candidatos (CandidatePipeline), Core (src/boardcomposer/), DOC-008 (masterplan, capa API futura), Capa export/, Capa geometry/, Capa layout/, Capa presenters/, Capa solver/ (+7 more)

### Community 24 - "Studio App & Layout Service"
Cohesion: 0.18
Nodes (8): main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., LayoutService, Bridge between BoardComposer Studio and the core layout engine., Application services for BoardComposer Studio., Container for shared Studio services., StudioServices

### Community 25 - "Horizontal/Vertical Generators & Docs"
Cohesion: 0.21
Nodes (11): Generadores Horizontal / Vertical (fuerza bruta), vertical_generator(), generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution(), test_generate_horizontal_solution(), test_generate_vertical_solution() (+3 more)

### Community 26 - "Presenters & JSON Output"
Cohesion: 0.37
Nodes (7): ABC, Presenter, JsonPresenter, solutions_to_json(), solution_to_text(), TextPresenter, OptimizationStrategy

### Community 27 - "MaxRects Heuristics"
Cohesion: 0.26
Nodes (11): best_area_fit(), best_bottom_left_fit(), best_long_side_fit(), best_short_side_fit(), test_best_area_fit_prefers_less_waste(), test_best_area_fit_returns_none_without_candidates(), test_best_long_side_fit_prefers_shorter_long_side(), test_best_long_side_fit_returns_none_without_candidates() (+3 more)

### Community 28 - "Selection Manager"
Cohesion: 0.19
Nodes (4): Selection services for BoardComposer Studio., Selection manager for BoardComposer Studio., Tracks selected Studio object identifiers., SelectionManager

### Community 29 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 30 - "Geometry Collision & Layout Validation"
Cohesion: 0.24
Nodes (7): placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision()

### Community 31 - "Candidate Pipeline & Geometry Solver"
Cohesion: 0.35
Nodes (7): CandidatePipeline, GeometrySolver, build_two_board_project(), test_geometry_solver_includes_expected_layout_families(), test_geometry_solver_matches_candidate_pipeline(), test_geometry_solver_returns_solutions(), test_geometry_solver_sorts_solutions_by_score()

### Community 32 - "SCR-007 Export Screen"
Cohesion: 0.31
Nodes (10): BoardComposer Studio, Criterios de aceptación, Evolución prevista, Flujo principal de exportación, Opciones de exportación, Pantalla de Exportación (SCR-007), Principios de interacción, Selección de solución (+2 more)

### Community 33 - "Backlog Items"
Cohesion: 0.20
Nodes (10): DOC-004 — Backlog del Producto, IDE-0001 — Workspace interactivo, IDE-0002 — Comparador de algoritmos, IDE-0003 — Inspector de piezas, IDE-0004 — Gestión de proyectos, IDE-0005 — Exportación PDF/SVG, DOC-006 — Gestión de la Deuda Técnica, DT-0001 — Completar documentación funcional de BoardComposer Studio (+2 more)

### Community 34 - "CLI & Architecture Docs"
Cohesion: 0.29
Nodes (8): CLI (cli.py), build_demo_project(), main(), strategy_by_name(), test_build_demo_project(), test_cli_json_fields_are_stable(), test_cli_project_constraints_from_cli_options(), test_strategy_argument_is_supported()

### Community 35 - "Event Bus"
Cohesion: 0.24
Nodes (5): EventHandler, EventBus, Event bus for BoardComposer Studio., Simple synchronous event bus., Event services for BoardComposer Studio.

### Community 36 - "MASTERPLAN.md Current Block"
Cohesion: 0.24
Nodes (10): MASTERPLAN — Estado del Proyecto, ADR-010, ADR-011, ADR-012, BoardWorkspace, CommandManager, MovePieceCommand, PlacementValidator (+2 more)

### Community 37 - "Roadmap Phases"
Cohesion: 0.22
Nodes (9): Comparación de algoritmos — todo puede compararse, DOC-003 — Roadmap del Producto, Asistencia mediante IA, Fase 3 — Plataforma, Fase 4 — Inteligencia, Fase 5 — Ecosistema, Plugins, IDE-0007 — Asistente IA (+1 more)

### Community 38 - "MaxRects Placement Ops"
Cohesion: 0.28
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 39 - "Scoring Weights Presets"
Cohesion: 0.36
Nodes (7): balanced(), compact_first(), material_first(), ScoringWeights, test_balanced_profile(), test_compact_first_profile(), test_material_first_profile()

### Community 40 - "UI Screens Catalog (SCR-001..004)"
Cohesion: 0.54
Nodes (8): Explicabilidad — la explicación forma parte del resultado, Fase 2 — BoardComposer Studio (En curso), SCR-001 — Pantalla de Inicio, SCR-002 — Workspace, SCR-003 — Comparador de Soluciones, SCR-004 — Inspector Contextual, SCR-005 — Gestión del Proyecto, SCR-006 — Preferencias

### Community 41 - "Free Space Generator & Docs"
Cohesion: 0.29
Nodes (6): Generador Free Space, Registro de generadores (GENERATOR_REGISTRY), generate_free_space_solution(), free_space_generator(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit()

### Community 42 - "Skyline Runner"
Cohesion: 0.43
Nodes (5): _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions(), test_candidate_orders()

### Community 43 - "SCR-007 Export Formats"
Cohesion: 0.29
Nodes (7): Formato CSV, Formato DXF, Formato Imagen (PNG/JPEG), Formato JSON, Formato PDF, Formato SVG, Formatos disponibles

### Community 46 - "Generator Utils Protocol"
Cohesion: 0.50
Nodes (3): SolutionGenerator, LayoutGenerator, single_solution_generator()

### Community 47 - "CSV Data Requirements"
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
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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
- **Why does `LayoutService` connect `Studio App & Layout Service` to `Domain Constraints & Data Model Docs`, `Architecture Docs: Studio & ADR Citations`, `Candidate Pipeline & Geometry Solver`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `Board` connect `Board Domain & Ordering` to `CLI & Architecture Docs`, `Rectangle Geometry & Bounds`, `Domain Constraints & Data Model Docs`, `Packing Runner & Commands`, `MaxRects Beam Search & Docs`, `Free Space Generator & Docs`, `Skyline Runner`, `Architecture Docs: Studio & ADR Citations`, `MaxRects Beam Runner & Engine`, `Domain Package & Explanation Docs`, `Solver Strategies & Presenters Tests`, `Horizontal/Vertical Generators & Docs`, `Candidate Pipeline & Geometry Solver`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `Project` connect `Domain Constraints & Data Model Docs` to `CLI & Architecture Docs`, `Assembly Solution & Scoring Docs`, `MaxRects Beam Search & Docs`, `Free Space Generator & Docs`, `Board Domain & Ordering`, `Skyline Runner`, `Architecture Docs: Studio & ADR Citations`, `MaxRects Beam Runner & Engine`, `Domain Package & Explanation Docs`, `Solver Strategies & Presenters Tests`, `Horizontal/Vertical Generators & Docs`, `Presenters & JSON Output`, `Candidate Pipeline & Geometry Solver`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._