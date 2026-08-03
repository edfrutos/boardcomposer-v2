# Aprovechar retales como tablero en Studio

BoardComposer no distingue entre un tablero nuevo y un resto de otra
construcción (un retal, un recorte de corte anterior) — para el dominio,
ambos son solo un rectángulo con largo/ancho/grosor. Esta guía explica cómo
modelar un retal existente en Studio hoy, sin ningún paso especial ni
código adicional.

Alcance y contexto de esta decisión: `DEC-0019`
(`docs/masterplan/DOC-005-Decisiones.md`), sobre la Candidata 1 de
`docs/masterplan/DOC-999-Ideas.md`.

## Por qué funciona sin cambios

- `Board` (`src/boardcomposer/domain/board.py`, Core) solo exige
  `length_mm`/`width_mm`/`thickness_mm` finitos y positivos — no sabe ni le
  importa si el tablero es nuevo o un resto.
- `StudioBoard` (`studio/models/board.py`) añade `material: str`, campo de
  texto libre — sirve tanto para el material real ("Contrachapado 18mm")
  como para anotar la procedencia ("Retal — contrachapado 18mm, sobrante
  mueble salón").
- El solver (`GeometrySolver`/generadores) coloca piezas dentro de
  cualquier tablero que reciba, sin distinguir su origen.

## Cómo hacerlo

1. Mide el retal real (largo × ancho × grosor) tal como quedó tras el
   corte anterior.
2. En Studio, "Nuevo tablero" (mismo diálogo de siempre) con esas medidas
   exactas — no las de un formato comercial estándar.
3. En "Material", anota algo que te permita reconocerlo luego como retal
   (por ejemplo `Retal — <material> <grosor>mm`). Es solo texto libre, sin
   validación ni efecto en el solver.
4. Añade piezas y resuelve como con cualquier otro tablero — si las piezas
   caben en las medidas del retal, el solver las coloca igual.

## Limitaciones conocidas (fuera de alcance de esta guía)

- **Solo formas rectangulares.** Si el retal tiene una forma irregular (una
  L, una esquina cortada), no hay forma de modelarlo tal cual — el dominio
  asume rectángulos (`Board`/`BoardPlacement`). Tendrías que acotar el
  retal a su mayor rectángulo aprovechable.
- **Sin inventario entre proyectos.** El retal vive solo dentro del
  proyecto donde lo das de alta — no hay un almacén de "retales
  disponibles" que se comparta entre proyectos distintos ni que se marque
  como "consumido" al usarlo.
- **Sin priorización automática.** El solver no prefiere agotar retales
  antes que tablero nuevo — la elección de qué tablero usar es siempre
  manual.

Ambas limitaciones quedan registradas como posible ampliación futura, sin
acotar todavía, en `docs/masterplan/DOC-999-Ideas.md`.
