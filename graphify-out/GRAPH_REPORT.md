# Graph Report - .  (2026-07-10)

## Corpus Check
- Corpus is ~35,195 words - fits in a single context window. You may not need a graph.

## Summary
- 1151 nodes · 2303 edges · 65 communities (50 shown, 15 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 548 edges (avg confidence: 0.78)
- Token cost: 166,398 input · 0 output

## Community Hubs (Navigation)
- Studio Export (SVG/PDF)
- Qt Workspace Canvas
- CSV Data & Solver Strategies
- Architecture Docs: ADRs & Core Layers
- Manifesto & Algorithm Catalog
- Studio App Entry Point
- Skyline Algorithm Core
- Core Architecture ADRs
- MaxRects Free Rectangle
- Project Foundational Docs
- Rectangle Geometry
- Studio Main Window
- Masterplan Product & Manifesto Docs
- Studio Commands (Undo/Redo)
- Beam Search (generic) & MaxRects Beam Docs
- Solver Architecture Docs & DT-0002
- Assembly Solution & Scoring
- Board Domain & Ordering
- Domain Package
- Placement & Collision
- Architecture Docs: Core/CLI Dependency Rule
- Horizontal/Vertical Generators
- Domain Explanation & Data Model
- MaxRects Beam vs Classic Route
- Candidate Pipeline & Dedup
- MaxRects Heuristics Package
- MaxRects Contact Heuristics
- Generator Registry & Tests
- MaxRects Core Algorithm (find/place)
- Workspace Blueprint ADRs
- Free Space Generator & Registry
- MaxRects Beam Search Tests
- Sequential Solver (reference implementation)
- MaxRects Runner
- Layout Bounds
- MaxRects Generator & Tests
- MaxRects Engine
- SVG Exporter (Core)
- Skyline Runner
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
- `Board (dataclass)` --documents--> `Board`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/board.py
- `Reglas de explicación textual` --references--> `SolutionExplanation`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/scoring.md → src/boardcomposer/domain/explanation.py
- `BoardPlacement (dataclass)` --documents--> `BoardPlacement`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/placement.py
- `SolutionScore (dataclass)` --documents--> `SolutionScore`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/data_model.md → src/boardcomposer/domain/score.py
- `Generador Horizontal (fuerza bruta)` --references--> `generate_horizontal_permutations()`  [EXTRACTED]
  /Volumes/BACKUPS_PROYECTOS/__03.-Github_Repositories/boardcomposer/docs/algorithms.md → src/boardcomposer/solver/layout_generator.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **BoardComposer Core Principles** — project_philosophy_multiple_solutions, project_philosophy_explainability, project_philosophy_configurable_scoring, project_philosophy_modular_architecture, project_philosophy_ai_complement [EXTRACTED 1.00]
- **BoardComposer Roadmap Phases** — roadmap_fase0_fundamentos, roadmap_fase1_motor_minimo, roadmap_fase2_datos, roadmap_fase3_visualizacion, roadmap_fase4_app_macos [EXTRACTED 1.00]
- **Core/Studio/CLI layering under the no-interface-dependency rule** — docs_architecture_core, docs_architecture_studio, docs_architecture_cli, docs_architecture_dependency_rule [EXTRACTED 1.00]
- **Composición de AssemblySolution** — docs_data_model_assembly_solution, docs_data_model_board_placement, docs_data_model_solution_score [EXTRACTED 1.00]
- **Optimization Algorithms Compared as a Laboratory** — doc_000_manifiesto_skyline, doc_000_manifiesto_maxrects, doc_000_manifiesto_beam_search, doc_000_manifiesto_algoritmos_geneticos, doc_000_manifiesto_cp_sat [EXTRACTED 1.00]
- **Interfaces consumen el Core mediante APIs públicas** — masterplan_doc_002_arquitectura_core, masterplan_doc_002_arquitectura_studio, masterplan_doc_002_arquitectura_cli, masterplan_doc_002_arquitectura_api [EXTRACTED 1.00]
- **Domain, Solver y Exporters se apoyan en el Geometry Engine** — masterplan_doc_002_arquitectura_domain, masterplan_doc_002_arquitectura_solver, masterplan_doc_002_arquitectura_exporters, masterplan_doc_002_arquitectura_geometry_engine [EXTRACTED 1.00]
- **Tabla 'Backlog inicial' (IDE-0001 a IDE-0008)** — masterplan_doc_004_backlog_ide_0001, masterplan_doc_004_backlog_ide_0002, masterplan_doc_004_backlog_ide_0003, masterplan_doc_004_backlog_ide_0004, masterplan_doc_004_backlog_ide_0005, masterplan_doc_004_backlog_ide_0006, masterplan_doc_004_backlog_ide_0007, masterplan_doc_004_backlog_ide_0008 [EXTRACTED 1.00]
- **Elementos P0/P1 completados (IDE-0001 a IDE-0005)** — masterplan_doc_004_backlog_ide_0001, masterplan_doc_004_backlog_ide_0002, masterplan_doc_004_backlog_ide_0003, masterplan_doc_004_backlog_ide_0004, masterplan_doc_004_backlog_ide_0005 [INFERRED 0.85]
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

## Communities (65 total, 15 thin omitted)

### Community 0 - "Studio Export (SVG/PDF)"
Cohesion: 0.06
Nodes (65): studio/export/ (svg_export.py, pdf_export.py, solution_bridge.py), tests/conftest.py (QT_QPA_PLATFORM=offscreen), Exportación — studio/export/ (SVG/PDF export feature), IDE-0005 reference in studio.md (Exportación PDF/SVG), pdf_export.py — export_project_to_pdf, solution_bridge.py — studio_project_to_solution, svg_export.py — export_project_to_svg, tests/test_pdf_export.py (+57 more)

### Community 1 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 2 - "CSV Data & Solver Strategies"
Cohesion: 0.05
Nodes (51): ABC, Formato de entrada CSV, data/samples/basic_boards.csv (ejemplo), ScoringWeights (scoring_weights.py), Estrategias de optimización (OptimizationStrategy), BaseSolver (ABC), GeometrySolver (solver de produccion), SequentialSolver (+43 more)

### Community 3 - "Architecture Docs: ADRs & Core Layers"
Cohesion: 0.05
Nodes (50): DOC-002-Arquitectura.md, DOC-008 (future API layer reference), docs/architecture.md (Architecture documentation), ADR-003 (Event Bus), ADR-010 (PlacementValidator as source of truth), balanced_strategy (default solve strategy), Command Protocol (name/redo/undo), CommandManager (undo/redo stacks) (+42 more)

### Community 4 - "Manifesto & Algorithm Catalog"
Cohesion: 0.06
Nodes (49): BoardComposer Studio, DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), Comparación de algoritmos — todo puede compararse, CP-SAT, Explicabilidad — la explicación forma parte del resultado, MaxRects (algoritmo de optimización) (+41 more)

### Community 5 - "Studio App Entry Point"
Cohesion: 0.06
Nodes (23): EventHandler, main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., EventBus, Event bus for BoardComposer Studio., Simple synchronous event bus., Event services for BoardComposer Studio. (+15 more)

### Community 6 - "Skyline Algorithm Core"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 7 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 8 - "MaxRects Free Rectangle"
Cohesion: 0.08
Nodes (27): FreeRectangle, MaxRects, Heuristic, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles() (+19 more)

### Community 9 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 10 - "Rectangle Geometry"
Cohesion: 0.10
Nodes (16): Rectangle (primitiva geométrica), Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit() (+8 more)

### Community 11 - "Studio Main Window"
Cohesion: 0.11
Nodes (12): QMainWindow, MainWindow, Refresh inspector panel for the selected piece., Main application window., Content builder for the Comparador panel (SCR-003 — Comparador de Soluciones)., render_comparison(), _row(), _solution() (+4 more)

### Community 12 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 13 - "Studio Commands (Undo/Redo)"
Cohesion: 0.09
Nodes (10): Protocol, Command, CommandManager, Command manager for undo/redo., Stores undo and redo stacks., Base command protocol for Studio undo/redo., DeletePieceCommand, Studio command system. (+2 more)

### Community 14 - "Beam Search (generic) & MaxRects Beam Docs"
Cohesion: 0.09
Nodes (22): Trade-off de Beam Search: mas combinaciones heuristica/orden a cambio de mas coste computacional, Variante Beam Search de MaxRects (maxrects_beam, beam_width=4), Score, beam_search(), BeamSearchConfig, _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic (+14 more)

### Community 15 - "Solver Architecture Docs & DT-0002"
Cohesion: 0.06
Nodes (32): Algoritmos (docs/algorithms.md), Arquitectura interna del Solver (docs/solver_architecture.md), Fase 1 — Core (Completada), ADR relacionados, BaseSolver, [build-system], Gestión de la Deuda Técnica (DOC-006), DOC-002 — Arquitectura (+24 more)

### Community 16 - "Assembly Solution & Scoring"
Cohesion: 0.13
Nodes (19): AssemblySolution (dataclass frozen), BoardPlacement (dataclass), SolutionScore (dataclass), Cálculo evaluate(), Reglas de explicación textual, Métricas de puntuación (objectives.py), AssemblySolution, compactness() (+11 more)

### Community 17 - "Board Domain & Ordering"
Cohesion: 0.12
Nodes (16): board_ordering.py: ordenes de tablas compartidos, Board, largest_area_first(), longest_edge_first(), original_order(), _candidate_orders(), test_largest_area_first(), test_longest_edge_first() (+8 more)

### Community 18 - "Domain Package"
Cohesion: 0.12
Nodes (18): Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, skyline_generator(), generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project. (+10 more)

### Community 19 - "Placement & Collision"
Cohesion: 0.14
Nodes (12): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_deduplicate_solutions_removes_duplicates(), test_has_overlaps_accepts_valid_layout() (+4 more)

### Community 20 - "Architecture Docs: Core/CLI Dependency Rule"
Cohesion: 0.13
Nodes (20): CLI (cli.py), Core (src/boardcomposer/), Dependency rule: Core never depends on any interface, domain/ (Board, Project, AssemblySolution, etc.), Core export/ (solution_to_svg), geometry/ (Rectangle primitive), io/ (load_project_from_csv), layout/ (FreeSpaceManager) (+12 more)

### Community 21 - "Horizontal/Vertical Generators"
Cohesion: 0.20
Nodes (14): Project, horizontal_generator(), vertical_generator(), generate_horizontal_permutations(), generate_horizontal_solution(), generate_vertical_permutations(), generate_vertical_solution(), test_generate_horizontal_solution() (+6 more)

### Community 22 - "Domain Explanation & Data Model"
Cohesion: 0.21
Nodes (5): SolutionExplanation (dataclass), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 23 - "MaxRects Beam vs Classic Route"
Cohesion: 0.22
Nodes (14): maxrects/beam.py no reutiliza beam_search.py; candidato a revisar si hace falta mantener ambas implementaciones, beam_search.py: implementacion generica de beam search, Ruta MaxRects con Beam Search (maxrects_beam, beam_width=4), Ruta clasica MaxRects (sin beam search), maxrects_engine.py: tercera via de comparacion (workbench/tools), Familia MaxRects (modulos maxrects_*), Por que hay tantos ficheros maxrects_*: crecimiento incremental con cada algoritmo anadido, search.py::search_best_solution(): criterio interno compartido (+6 more)

### Community 24 - "Candidate Pipeline & Dedup"
Cohesion: 0.17
Nodes (9): Pipeline de candidatos (CandidatePipeline), respects_constraints(), deduplicate_solutions(), solution_signature(), evaluate(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_evaluation_returns_score() (+1 more)

### Community 25 - "MaxRects Heuristics Package"
Cohesion: 0.23
Nodes (12): Paquete solver/maxrects/ (logica geometrica), best_area_fit(), best_bottom_left_fit(), best_long_side_fit(), best_short_side_fit(), test_best_area_fit_prefers_less_waste(), test_best_area_fit_returns_none_without_candidates(), test_best_long_side_fit_prefers_shorter_long_side() (+4 more)

### Community 26 - "MaxRects Contact Heuristics"
Cohesion: 0.29
Nodes (13): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), MaxRectsPlacement, test_contact_score_accumulates_multiple_contacts(), test_contact_score_with_bottom_edge() (+5 more)

### Community 27 - "Generator Registry & Tests"
Cohesion: 0.21
Nodes (11): LayoutGenerator, generators_by_name(), _placed(), test_maxrects_places_at_least_as_many_boards_as_skyline(), test_generators_by_name(), test_maxrects_beam_generator_is_registered(), test_maxrects_generator_is_registered(), test_skyline_generator_is_registered() (+3 more)

### Community 28 - "MaxRects Core Algorithm (find/place)"
Cohesion: 0.24
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 29 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 30 - "Free Space Generator & Registry"
Cohesion: 0.22
Nodes (8): Generador Free Space, Registro de generadores (GENERATOR_REGISTRY), Generador Horizontal (fuerza bruta), Generador Vertical (fuerza bruta), generate_free_space_solution(), free_space_generator(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit()

### Community 31 - "MaxRects Beam Search Tests"
Cohesion: 0.36
Nodes (8): generate_beam_maxrects_solution(), _project(), test_beam_records_selected_heuristic(), test_beam_solution_records_strategy(), test_beam_width_one_matches_classic(), index(), render_solution(), render_svg()

### Community 32 - "Sequential Solver (reference implementation)"
Cohesion: 0.36
Nodes (7): SequentialSolver, test_sequential_solver_places_boards_in_sequence(), test_sequential_solver_returns_one_solution(), test_solver_respects_max_width(), test_solver_rotates_board_when_allowed(), test_solver_score_combines_usage_and_waste(), test_solver_wraps_to_next_row_when_length_exceeded()

### Community 33 - "MaxRects Runner"
Cohesion: 0.39
Nodes (7): BoardOrdering, generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size(), _place_all_boards(), Heuristic, _to_board_placement()

### Community 34 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 35 - "MaxRects Generator & Tests"
Cohesion: 0.38
Nodes (5): maxrects_generator(), generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 36 - "MaxRects Engine"
Cohesion: 0.53
Nodes (4): iter_maxrects_candidates(), _project(), test_iter_maxrects_candidates_can_use_beam(), test_iter_maxrects_candidates_uses_classic_candidates_by_default()

### Community 38 - "Skyline Runner"
Cohesion: 0.83
Nodes (3): _default_skyline_width(), _generate_for_order(), iter_skyline_solutions()

### Community 39 - "CSV Data Requirements"
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
- **137 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+132 more)
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
- **Why does `AssemblySolution` connect `Assembly Solution & Scoring` to `Studio Export (SVG/PDF)`, `CSV Data & Solver Strategies`, `Studio App Entry Point`, `Studio Main Window`, `Beam Search (generic) & MaxRects Beam Docs`, `Domain Package`, `Placement & Collision`, `Horizontal/Vertical Generators`, `Domain Explanation & Data Model`, `MaxRects Beam vs Classic Route`, `Candidate Pipeline & Dedup`, `Free Space Generator & Registry`, `MaxRects Beam Search Tests`, `MaxRects Runner`, `Layout Bounds`, `MaxRects Generator & Tests`, `MaxRects Engine`, `SVG Exporter (Core)`, `Skyline Runner`?**
  _High betweenness centrality (0.297) - this node is a cross-community bridge._
- **Why does `render_comparison()` connect `Studio Main Window` to `Studio Export (SVG/PDF)`, `Assembly Solution & Scoring`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `studio_project_to_solution()` connect `Studio Export (SVG/PDF)` to `Assembly Solution & Scoring`, `Placement & Collision`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Project` (e.g. with `Board` and `ProjectConstraints`) actually correct?**
  _`Project` has 38 INFERRED edges - model-reasoned connections that need verification._