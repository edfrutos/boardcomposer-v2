# Graph Report - .  (2026-07-09)

## Corpus Check
- Corpus is ~33,208 words - fits in a single context window. You may not need a graph.

## Summary
- 1085 nodes · 2135 edges · 68 communities (53 shown, 15 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 540 edges (avg confidence: 0.78)
- Token cost: 91,982 input · 0 output

## Community Hubs (Navigation)
- Inspector Panel & Studio Commands
- Qt Workspace Canvas
- Solver Hierarchy & Strategies
- Manifesto & Algorithm Catalog
- Skyline Algorithm Core
- Core Architecture ADRs
- MaxRects Core Algorithm
- Studio App Entry Point
- Project Foundational Docs
- Rectangle Geometry
- Masterplan Product & Manifesto Docs
- Generator Registry & Free Space
- Architecture Docs: Core Layers & CLI
- Studio Commands (Undo/Redo)
- MaxRects Beam vs Classic Route
- Architecture Docs: Studio Bridge & ADRs
- Domain Package
- Solver Objectives & Assembly Solution
- Placement & Collision
- MaxRects Beam Runner & Scoring
- Candidate Pipeline & Dedup
- Domain Explanation & Data Model
- Board Orderings (shared)
- Board Domain & Sequential Solver
- MaxRects Contact Heuristics
- MaxRects Heuristics Package
- Beam Search (generic) & MaxRects Beam Docs
- MaxRects Core Algorithm (find/place)
- Backlog Register & Status
- Solver Architecture Docs & DT-0002
- Workspace Blueprint ADRs
- Technical Debt: Packaging Fix (DT-0005)
- MaxRects Runner
- Layout Bounds
- Technical Debt Registry Cross-References
- Technical Debt: Dead Modules Removed (DT-0004)
- MaxRects Generator & Tests
- Free Space Generator & Tests
- MaxRects Engine
- SVG Exporter
- Workbench App
- Packing Benchmarks Tests
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
2. `Board` - 73 edges
3. `AssemblySolution` - 71 edges
4. `MaxRects` - 47 edges
5. `BoardPlacement` - 43 edges
6. `ProjectConstraints` - 37 edges
7. `BoardPieceItem` - 31 edges
8. `BoardWorkspace` - 29 edges
9. `MaxRectsPlacement` - 28 edges
10. `MainWindow` - 27 edges

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
- **Entradas del backlog inicial** — masterplan_doc_004_backlog_document, masterplan_doc_004_backlog_ide_0001, masterplan_doc_004_backlog_ide_0002, masterplan_doc_004_backlog_ide_0003, masterplan_doc_004_backlog_ide_0004, masterplan_doc_004_backlog_ide_0005, masterplan_doc_004_backlog_ide_0006, masterplan_doc_004_backlog_ide_0007, masterplan_doc_004_backlog_ide_0008 [EXTRACTED 1.00]
- **Cobertura de documentación funcional de Studio (DT-0001)** — masterplan_doc_006_deudatecnica_dt_0001, docs_studio_studioservices, docs_studio_projectmanager, docs_studio_commandmanager, docs_studio_selectionmanager, docs_studio_placementvalidator, docs_studio_dragcontroller, docs_studio_layout_resolution_flow, docs_studio_eventbus [EXTRACTED 1.00]
- **Explicabilidad y confianza como eje transversal (Producto + UX)** — masterplan_doc_001_producto_propuesta_valor, masterplan_doc_001_producto_problema, masterplan_doc_007_ux_studio_objetivos_experiencia [INFERRED 0.85]
- **Command Pattern for Studio Workspace Actions** — masterplan_masterplan_commandmanager, masterplan_masterplan_movepiececommand, masterplan_masterplan_rotatepiececommand [INFERRED 0.85]
- **Arquitectura reactiva y trazable del Core** — adr_adr_003_event_bus_decision, adr_adr_005_timeline_decision, adr_adr_008_arquitectura_basada_en_commands_command_pattern_decision [INFERRED 0.85]
- **Consolidación arquitectónica del Workspace** — adr_adr_010_placementvalidator_decision, adr_adr_011_workspace_blueprint_decision, adr_adr_012_selectioncontroller_decision, adr_adr_013_geometry_engine_decision [INFERRED 0.85]
- **Flujo completo de usuario en BoardComposer Studio** — flows_flw_001_crear_proyecto_flow, flows_flw_002_importar_csv_flow, flows_flw_003_generar_soluciones_flow, flows_flw_004_comparar_flow, flows_flw_005_exportar_flow, flows_flw_006_editar_proyecto_flow [EXTRACTED 1.00]
- **BoardComposer Functional Requirements** — docs_requirements_rf001, docs_requirements_rf002, docs_requirements_rf003, docs_requirements_rf004, docs_requirements_rf005, docs_requirements_rf006 [EXTRACTED 1.00]
- **Implementacion de MaxRects Beam Search** — docs_algorithms_maxrects_beam_search, docs_solver_architecture_maxrects_beam_route, solver_generators_maxrects_beam_generator, solver_maxrects_search_generate_beam_maxrects_solution, solver_maxrects_beam_runner_iter_beam_maxrects_solutions, maxrects_beam_search_states [EXTRACTED 1.00]
- **SequentialSolver como implementacion de referencia (v0.1)** — docs_solver_architecture_sequential_solver, docs_solver_architecture_sequential_solver_rationale, solver_sequential_solver_sequentialsolver [INFERRED 0.85]
- **Patrón de comandos undo/redo** — docs_studio_commandmanager, docs_studio_command, docs_studio_movepiececommand, docs_studio_rotatepiececommand, docs_studio_deletepiececommand [EXTRACTED 1.00]
- **Sincronización de selección aplicación-workspace** — docs_studio_selectionmanager, docs_studio_selectioncontroller, docs_studio_boardworkspace [INFERRED 0.85]
- **Funcionalidad Inspector de piezas (IDE-0003)** — docs_studio_inspector_panel, masterplan_doc_004_backlog_ide_0003, docs_studio_scr_004, docs_studio_selectioncontroller [EXTRACTED 1.00]
- **Componentes principales de Exportación** — ui_scr_007_exportacion_seleccion_solucion, ui_scr_007_exportacion_formatos_disponibles, ui_scr_007_exportacion_opciones_exportacion, ui_scr_007_exportacion_vista_previa [EXTRACTED 1.00]
- **Relación de Exportación con otras pantallas** — ui_scr_007_exportacion_pantalla, ui_scr_002_workspace_pantalla, ui_scr_003_comparador_pantalla, ui_scr_005_proyecto_pantalla, ui_scr_006_preferencias_pantalla [EXTRACTED 1.00]

## Communities (68 total, 15 thin omitted)

### Community 0 - "Inspector Panel & Studio Commands"
Cohesion: 0.05
Nodes (45): Inspector contextual (studio/panels/inspector_panel.py), docs/masterplan/ui/SCR-004-Inspector.md, QMainWindow, DeletePieceCommand, MainWindow, Main window for BoardComposer Studio., Refresh inspector panel for the selected piece., Main application window. (+37 more)

### Community 1 - "Qt Workspace Canvas"
Cohesion: 0.05
Nodes (22): QGraphicsRectItem, QGraphicsScene, QGraphicsView, QMouseEvent, QPoint, QRectF, QWheelEvent, create_board_item() (+14 more)

### Community 2 - "Solver Hierarchy & Strategies"
Cohesion: 0.05
Nodes (50): ABC, ScoringWeights (scoring_weights.py), Estrategias de optimización (OptimizationStrategy), BaseSolver (ABC), GeometrySolver (solver de produccion), SequentialSolver, SequentialSolver es el Motor v0.1 original del proyecto; se mantiene como implementacion de referencia, no es codigo muerto, build_demo_project() (+42 more)

### Community 3 - "Manifesto & Algorithm Catalog"
Cohesion: 0.06
Nodes (49): BoardComposer Studio, DOC-000 — Manifiesto del Proyecto, Algoritmos Genéticos, Beam Search (algoritmo de optimización), Comparación de algoritmos — todo puede compararse, CP-SAT, Explicabilidad — la explicación forma parte del resultado, MaxRects (algoritmo de optimización) (+41 more)

### Community 4 - "Skyline Algorithm Core"
Cohesion: 0.07
Nodes (21): Algoritmo Skyline, SkylineNode, SkylinePlacement, Skyline, SkylineCandidate, test_skyline_prefers_leftmost_when_same_height(), test_skyline_prefers_lowest_node(), test_bottom_left_prefers_lowest_then_leftmost() (+13 more)

### Community 5 - "Core Architecture ADRs"
Cohesion: 0.07
Nodes (44): Core, Core como única fuente de verdad, Las soluciones son inmutables, CsvImported (evento), Arquitectura basada en Event Bus, Event Bus, ExportCompleted (evento), ProjectCreated (evento) (+36 more)

### Community 6 - "MaxRects Core Algorithm"
Cohesion: 0.08
Nodes (27): FreeRectangle, MaxRects, Heuristic, MaxRects bin packing over a set of free rectangles., Place rectangles using the MaxRects free-space algorithm., test_find_candidates_returns_all_candidates(), test_find_candidates_returns_multiple_candidates(), test_place_candidate_updates_free_rectangles() (+19 more)

### Community 7 - "Studio App Entry Point"
Cohesion: 0.07
Nodes (17): EventHandler, main(), Application entry point for BoardComposer Studio., Run BoardComposer Studio., EventBus, Event bus for BoardComposer Studio., Simple synchronous event bus., Event services for BoardComposer Studio. (+9 more)

### Community 8 - "Project Foundational Docs"
Cohesion: 0.07
Nodes (38): BoardComposer purpose: generate board compositions reusing existing material via optimization algorithms, AI context rules (preserve data model compatibility, document decisions, update changelog), CHANGELOG 0.0.1 entry (2026-06-26), Decision: start with 2D flat assembly of rectangular boards, Decision: core independent of PySide6/files/AI, Decision: explainable solutions (score + explanation), Masterplan documents (Manifiesto, Producto, Arquitectura, Roadmap, Backlog, Decisiones, DeudaTecnica, UX-Studio, API), Project structure doc: docs/masterplan layout (INDEX + DOC-000..DOC-008 + sprints/) (+30 more)

### Community 9 - "Rectangle Geometry"
Cohesion: 0.10
Nodes (16): Rectangle (primitiva geométrica), Rectangle, FreeSpace, FreeSpaceManager, place_board_in_first_space(), test_free_space_manager_finds_space(), test_free_space_manager_places_rectangle(), test_free_space_manager_rejects_rectangle_that_does_not_fit() (+8 more)

### Community 10 - "Masterplan Product & Manifesto Docs"
Cohesion: 0.06
Nodes (37): DOC-000 — Manifiesto, BoardComposer (Producto), DOC-001 — Especificación del Producto, Fuera del alcance (por ahora), Objetivos del producto, El problema: soluciones de corte opacas, Nuestra propuesta, Propuesta de valor (+29 more)

### Community 11 - "Generator Registry & Free Space"
Cohesion: 0.11
Nodes (26): Generador Free Space, Registro de generadores (GENERATOR_REGISTRY), Generador Horizontal (fuerza bruta), Generador Vertical (fuerza bruta), LayoutGenerator, Project, generators_by_name(), horizontal_generator() (+18 more)

### Community 12 - "Architecture Docs: Core Layers & CLI"
Cohesion: 0.06
Nodes (30): ADR-003 (EventBus), ADR-008 (patrón Command para undo/redo), CLI (cli.py), Core (src/boardcomposer/), DOC-008 (masterplan, capa API futura), Capa export/, Capa geometry/, Capa io/ (+22 more)

### Community 13 - "Studio Commands (Undo/Redo)"
Cohesion: 0.11
Nodes (9): Protocol, Command, CommandManager, Command manager for undo/redo., Stores undo and redo stacks., Base command protocol for Studio undo/redo., Studio command system., MovePieceCommand (+1 more)

### Community 14 - "MaxRects Beam vs Classic Route"
Cohesion: 0.16
Nodes (20): maxrects/beam.py no reutiliza beam_search.py; candidato a revisar si hace falta mantener ambas implementaciones, beam_search.py: implementacion generica de beam search, Ruta MaxRects con Beam Search (maxrects_beam, beam_width=4), Ruta clasica MaxRects (sin beam search), maxrects_engine.py: tercera via de comparacion (workbench/tools), Familia MaxRects (modulos maxrects_*), Por que hay tantos ficheros maxrects_*: crecimiento incremental con cada algoritmo anadido, search.py::search_best_solution(): criterio interno compartido (+12 more)

### Community 15 - "Architecture Docs: Studio Bridge & ADRs"
Cohesion: 0.14
Nodes (23): ADR-003 (Event Bus), ADR-010 (validación única fuente de verdad de colocación), BoardWorkspace, Calcular antes de aplicar (flujo de resolución de layout), Command (Protocol) (studio/commands/command.py), CommandManager (studio/commands/command_manager.py), DeletePieceCommand, DragController (studio/workspace/drag_controller.py) (+15 more)

### Community 16 - "Domain Package"
Cohesion: 0.14
Nodes (16): Capa domain/, Board (dataclass), Project (dataclass), ProjectConstraints (dataclass), ProjectConstraints, generate_skyline_solution(), Generate Skyline-based layout solutions., Generate the best Skyline layout solution for the given project. (+8 more)

### Community 17 - "Solver Objectives & Assembly Solution"
Cohesion: 0.17
Nodes (14): Métricas de puntuación (objectives.py), AssemblySolution, compactness(), material_utilization(), placed_board_ratio(), rotation_ratio(), test_solution_explanation_accepts_values(), test_solution_explanation_defaults() (+6 more)

### Community 18 - "Placement & Collision"
Cohesion: 0.16
Nodes (11): BoardPlacement, placement_to_rectangle(), placements_overlap(), has_overlaps(), test_placements_do_not_overlap_when_touching_edges(), test_placements_overlap(), test_has_overlaps_accepts_valid_layout(), test_has_overlaps_detects_collision() (+3 more)

### Community 19 - "MaxRects Beam Runner & Scoring"
Cohesion: 0.14
Nodes (12): _beam_candidate(), iter_beam_maxrects_solutions(), Heuristic, score_state(), _beam_candidate(), Heuristic, MaxRectsState, test_score_state_prefers_more_placements() (+4 more)

### Community 20 - "Candidate Pipeline & Dedup"
Cohesion: 0.14
Nodes (10): Pipeline de candidatos (CandidatePipeline), respects_constraints(), deduplicate_solutions(), solution_signature(), evaluate(), test_respects_constraints_accepts_valid_solution(), test_respects_constraints_rejects_excess_length(), test_deduplicate_solutions_removes_duplicates() (+2 more)

### Community 21 - "Domain Explanation & Data Model"
Cohesion: 0.21
Nodes (5): SolutionExplanation (dataclass), SolutionExplanation, SolutionScore, test_solution_score_rejects_negative_values(), test_solution_score_total()

### Community 22 - "Board Orderings (shared)"
Cohesion: 0.19
Nodes (12): board_ordering.py: ordenes de tablas compartidos, largest_area_first(), longest_edge_first(), original_order(), _candidate_orders(), _default_skyline_width(), _generate_for_order(), iter_skyline_solutions() (+4 more)

### Community 23 - "Board Domain & Sequential Solver"
Cohesion: 0.21
Nodes (11): Board, SequentialSolver, test_board_area(), test_board_requires_positive_dimensions(), test_project_total_area(), test_sequential_solver_places_boards_in_sequence(), test_sequential_solver_returns_one_solution(), test_solver_respects_max_width() (+3 more)

### Community 24 - "MaxRects Contact Heuristics"
Cohesion: 0.29
Nodes (13): contact_score(), _contact_with_edges(), _contact_with_placements(), _overlap(), _shared_edge(), MaxRectsPlacement, test_contact_score_accumulates_multiple_contacts(), test_contact_score_with_bottom_edge() (+5 more)

### Community 25 - "MaxRects Heuristics Package"
Cohesion: 0.25
Nodes (12): Paquete solver/maxrects/ (logica geometrica), best_area_fit(), best_bottom_left_fit(), best_long_side_fit(), best_short_side_fit(), test_best_area_fit_prefers_less_waste(), test_best_area_fit_returns_none_without_candidates(), test_best_long_side_fit_prefers_shorter_long_side() (+4 more)

### Community 26 - "Beam Search (generic) & MaxRects Beam Docs"
Cohesion: 0.20
Nodes (10): Trade-off de Beam Search: mas combinaciones heuristica/orden a cambio de mas coste computacional, Variante Beam Search de MaxRects (maxrects_beam, beam_width=4), Score, beam_search(), BeamSearchConfig, search_states(), State, test_beam_search_keeps_best_states() (+2 more)

### Community 27 - "MaxRects Core Algorithm (find/place)"
Cohesion: 0.22
Nodes (3): Algoritmo MaxRects, Place a rectangle and update the remaining free rectangles., Return the best placement candidate without mutating free space.

### Community 28 - "Backlog Register & Status"
Cohesion: 0.18
Nodes (14): DOC-004 — Backlog del Producto, Estado actual del documento (En revisión; pendiente Épicas/Roadmap/flujo Idea→Épica→Sprint), Estados de una entrada (⚪🔵🟡🟢🔴⚫), Formato de una entrada del backlog, IDE-0001 Workspace interactivo (🟢 Completada, P0), IDE-0002 Comparador de algoritmos (🔵 Planificada, P0), IDE-0003 Inspector de piezas (🟢 Completada, P0), IDE-0005 Exportación PDF/SVG (🔵 Planificada, P1) (+6 more)

### Community 29 - "Solver Architecture Docs & DT-0002"
Cohesion: 0.15
Nodes (13): Algoritmos (docs/algorithms.md), Arquitectura interna del Solver (docs/solver_architecture.md), Fase 1 — Core (Completada), BaseSolver, DT-0002 Arquitectura interna del Solver (Resuelto), GENERATOR_REGISTRY, GeometrySolver (en producción), maxrects_beam_runner.py (+5 more)

### Community 30 - "Workspace Blueprint ADRs"
Cohesion: 0.27
Nodes (12): PlacementValidator como fuente única de validación, PlacementValidator, BoardPieceItem, BoardWorkspace, Blueprint del Workspace, DragController, Factories, MainWindow (+4 more)

### Community 31 - "Technical Debt: Packaging Fix (DT-0005)"
Cohesion: 0.22
Nodes (9): docs/architecture.md, BoardComposer Studio — documentación funcional, DT-0001 (docs/masterplan/DOC-006-DeudaTecnica.md), docs/masterplan/DOC-007-UX-Studio.md, [build-system], DT-0005 pyproject.toml no empaquetaba studio/ correctamente (Resuelto), DT-A — Arquitectura, [tool.setuptools.packages.find] (where = ["src", "."]) (+1 more)

### Community 32 - "MaxRects Runner"
Cohesion: 0.39
Nodes (7): BoardOrdering, generate_maxrects_candidate(), iter_maxrects_solutions(), _maxrects_size(), _place_all_boards(), Heuristic, _to_board_placement()

### Community 33 - "Layout Bounds"
Cohesion: 0.29
Nodes (3): bounding_rectangle(), test_bounding_rectangle(), test_bounding_rectangle_empty()

### Community 34 - "Technical Debt Registry Cross-References"
Cohesion: 0.29
Nodes (7): ADR relacionados, Gestión de la Deuda Técnica (DOC-006), DOC-002 — Arquitectura, DOC-003 — Roadmap, DOC-005 — Registro de Decisiones, DT-0003 Cobertura de pruebas (Controlado), DT-T — Tests

### Community 35 - "Technical Debt: Dead Modules Removed (DT-0004)"
Cohesion: 0.29
Nodes (6): DT-0004 Módulos runner/adaptador sin uso eliminados (Resuelto), DT-C — Código, solver/generator_utils.py (eliminado), generators.py (envoltorio manual), solver/packing_runner.py (eliminado), single_solution_generator (adaptador)

### Community 36 - "MaxRects Generator & Tests"
Cohesion: 0.38
Nodes (5): maxrects_generator(), generate_maxrects_solution(), test_generate_maxrects_solution(), test_generate_maxrects_solution_records_selected_heuristic(), test_generate_maxrects_solution_records_selected_ordering()

### Community 37 - "Free Space Generator & Tests"
Cohesion: 0.40
Nodes (4): generate_free_space_solution(), free_space_generator(), test_generate_free_space_solution(), test_generate_free_space_solution_skips_boards_that_do_not_fit()

### Community 38 - "MaxRects Engine"
Cohesion: 0.53
Nodes (4): iter_maxrects_candidates(), _project(), test_iter_maxrects_candidates_can_use_beam(), test_iter_maxrects_candidates_uses_classic_candidates_by_default()

### Community 40 - "Workbench App"
Cohesion: 0.70
Nodes (4): demo_project(), index(), render_solution(), render_svg()

### Community 41 - "Packing Benchmarks Tests"
Cohesion: 0.83
Nodes (3): _run(), test_benchmark_long_strips(), test_benchmark_mixed_sizes()

### Community 42 - "CSV Data Requirements"
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
- **133 isolated node(s):** `boardcomposer`, `Ruff format check step`, `Ruff lint step`, `Run tests step (pytest)`, `Principle: the program proposes multiple solutions` (+128 more)
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
- **Why does `LayoutService` connect `Studio App Entry Point` to `Solver Hierarchy & Strategies`, `Architecture Docs: Core Layers & CLI`?**
  _High betweenness centrality (0.274) - this node is a cross-community bridge._
- **Why does `Board` connect `Board Domain & Sequential Solver` to `MaxRects Runner`, `Solver Hierarchy & Strategies`, `MaxRects Generator & Tests`, `Free Space Generator & Tests`, `MaxRects Engine`, `Studio App Entry Point`, `Workbench App`, `Rectangle Geometry`, `Packing Benchmarks Tests`, `Generator Registry & Free Space`, `Architecture Docs: Core Layers & CLI`, `MaxRects Beam vs Classic Route`, `Domain Package`, `MaxRects Beam Runner & Scoring`, `Domain Explanation & Data Model`, `Board Orderings (shared)`, `Beam Search (generic) & MaxRects Beam Docs`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `Project` connect `Generator Registry & Free Space` to `MaxRects Runner`, `Solver Hierarchy & Strategies`, `MaxRects Generator & Tests`, `Free Space Generator & Tests`, `MaxRects Engine`, `Studio App Entry Point`, `Workbench App`, `Packing Benchmarks Tests`, `Architecture Docs: Core Layers & CLI`, `MaxRects Beam vs Classic Route`, `Domain Package`, `MaxRects Beam Runner & Scoring`, `Domain Explanation & Data Model`, `Board Orderings (shared)`, `Board Domain & Sequential Solver`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Project` (e.g. with `Board` and `ProjectConstraints`) actually correct?**
  _`Project` has 38 INFERRED edges - model-reasoned connections that need verification._