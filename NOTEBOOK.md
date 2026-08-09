
# NOTEBOOK - BoardComposer

Cuaderno de ingeniería del proyecto.

## 2026-06-26 - Sesión inicial de arquitectura

BoardComposer no será un optimizador de corte tradicional. Será un motor para generar composiciones 2D a partir de tablas disponibles, puntuarlas y explicar sus ventajas e inconvenientes.

### Alcance inicial

- Composición plana 2D.

- Tablas rectangulares.

- Medidas internas en milímetros.

- Motor independiente de la interfaz.

- Salida inicial por consola.

### Queda fuera por ahora

- Modelado 3D.

- Muebles completos.

- Interfaz gráfica.

- IA integrada.

- Uniones complejas de carpintería.

## 2026-07-13 - Actualización de alcance

De lo que "quedaba fuera por ahora" en la sesión inicial, dos puntos ya están construidos:

- **Interfaz gráfica**: BoardComposer Studio (PySide6), completa — workspace, comparador, inspector, gestión de proyectos, exportación SVG/PDF.

- **IA integrada**: Asistente IA (IDE-0007, 6 fases) sobre un proveedor de IA pluggable — todavía sin conectar un proveedor real (usa `MockAIProvider`).

Modelado 3D, muebles completos y uniones complejas de carpintería siguen fuera de alcance. Ver `docs/masterplan/DOC-004-Backlog.md` para el estado vivo de cada funcionalidad.

## 2026-07-22 - Release v0.2.0

Publicada la versión 0.2.0 con todos los cambios acumulados desde 0.1.0. Incluye:

- **IDE-0013–0015**: guía de plugins, receta de despliegue Cloud y visibilidad de plugins instalados (CLI + API).
- **IDE-0016**: tema visual claro/oscuro con detección automática, iconos de línea, toolbar principal y `PromptTextEdit` multilínea en el Asistente.
- **IDE-0017**: despliegue privado en VPS propio (Plesk + Docker): API en `bc.efjdefrutos.com` y Studio accesible por navegador vía noVNC en `studio.efjdefrutos.com`. Autenticación HTTP Basic (nginx) sumada a `BOARDCOMPOSER_API_KEY` y `VNC_PASSWORD`. Cuatro bugs reales detectados y corregidos probando el Studio remoto contra el despliegue real.
- **IDE-0018**: importación de piezas desde CSV en Studio (`Archivo → Importar piezas (CSV)…`), deshacible pieza a pieza.
- Múltiples correcciones de usabilidad detectadas probando datos reales: nodo Soluciones vacío quitado del Explorer, `DeletePieceCommand` que no eliminaba la pieza del inventario, diálogos que cerraban con id vacío/repetido, fila "Orden de piezas" en el Comparador.
- CI: 489 tests en verde. Build del `.app` macOS generado y publicado como asset de la release `v0.2.0` en GitHub Actions (19 min).

Todos los IDEs planificados (IDE-0001–IDE-0018) en 🟢. Próximos pasos sin acotar en `docs/masterplan/DOC-999-Ideas.md`.

## 2026-07-14 - Cierre de las prioridades P0/P1

La IA integrada (2026-07-13) pasa de proveedor simulado a proveedor real: `AnthropicProvider` (SDK `anthropic`, modelo `claude-haiku-4-5`) conectado y verificado con una clave real (IDE-0007). Además:

- Endurecimiento para producción de la API: autenticación por clave (`BOARDCOMPOSER_API_KEY`), rate limiting (Flask-Limiter) y `gunicorn` como servidor WSGI (IDE-0009).
- Importación desde Excel, junto al CSV ya existente (IDE-0010).
- BoardComposer Studio empaquetado como `.app` de macOS con `pyside6-deploy` (IDE-0011).

Con esto no quedan prioridades P0/P1 pendientes en `docs/masterplan/DOC-003-Roadmap.md`; solo P2 (exportación DXF, marketplace/comunidad, cloud).

## 2026-07-26 - Release v0.3.0

Primera versión sin ninguna capacidad nueva: 16 commits de corrección y endurecimiento sobre lo ya entregado en `v0.2.0`, más la revisión completa de la documentación. 673 tests en verde.

- **Números no finitos**: `json.loads()` interpreta `"NaN"`/`"Infinity"` como flotantes, y toda comparación contra `NaN` es falsa — las guardas `< 0`/`<= 0` los dejaban pasar hasta el solver, la puntuación o la exportación. Ahora se exige `math.isfinite()` en cada ruta de entrada externa (API, CSV/Excel, modelos del Core y de Studio, pesos devueltos por la IA). La lección: validar por el signo no basta si el tipo admite valores fuera del orden total.
- **Errores recuperables**: un proyecto con colocaciones colgantes se repara descartándolas y avisando, en vez de rechazar el fichero entero; un CSV malformado da número de fila y código de salida 1, no un traceback. Ambos casos venían de asumir que un fichero propio siempre está bien formado.
- **Multi-tablero**: siete correcciones de Studio con la misma raíz — `LayoutService` seguía razonando como si el proyecto tuviera un solo tablero, meses después de que `DT-0013` introdujera varios. Nació `studio/workspace/placement_fit.py`, el equivalente sin Qt de `PlacementValidator`, para validar lo que ocurre fuera de la escena gráfica.
- **Documentación**: auditada de arriba abajo. Faltaba lo más básico para quien usa la herramienta desde la terminal — ni `--strategy`, ni `--top`, ni `boardcomposer plugins` aparecían en ningún sitio orientado al usuario; ahora en `docs/cli.md`. `INDEX.md` del masterplan estaba vacío desde el primer día. `docs/studio.md` afirmaba todavía que "Studio solo soporta un tablero activo por proyecto".
- **Hallazgo de la auditoría** (`DT-0020`, abierto): el ancho de sierra se configura, se persiste y es deshacible, pero solo lo aplica el arrastre interactivo. Ni el solver ni la exportación lo tienen en cuenta, así que un plano exportado asume corte de anchura cero y el material real no cuadrará. Documentar sirvió para encontrarlo.

## 2026-08-07 - Release v0.3.13

Trece releases de parche desde `v0.3.0` (27/07 a 07/08), todos los IDEs planificados hasta `IDE-0035` en 🟢, sin prioridades P0/P1/P2 pendientes en `DOC-003-Roadmap.md`. 926 tests en verde. Resumen por hilos, no cronológico — el detalle release a release está en `CHANGELOG.md`, el estado vivo de cada funcionalidad en `DOC-004-Backlog.md`.

- **Cierre del hallazgo `DT-0020`** (`v0.3.1`): el kerf pasa de ser solo una ayuda visual del arrastre interactivo a aplicarlo también el solver (`LayoutService.to_core_project()`) y `piece_fits_on_board()`, ensanchando cada pieza un corte a la derecha/abajo y el tablero igual para que se cancele — N piezas en fila exigen N-1 cortes, no N. El Core sigue sin saber qué es un kerf (`DEC-0016`); con `kerf_mm=0` nada cambia. Misma release: primera firma y notarización real del `.app` de macOS (`DEC-0017`), condicionada a que existan las credenciales — sin ellas, build sin firmar como hasta ahora.
- **El `EventBus` de `ADR-003` se usa por primera vez de verdad** (`v0.3.2`, `IDE-0019`): el dock "Timeline" llevaba desde su creación con el texto literal "Timeline / Consola / Eventos", ninguna de las tres cosas construida. Al cablearlo salió a la luz un `AttributeError` dormido (6 de 9 clases de `Command` sin `name`, nunca disparado hasta que el log de actividad lo leyó) y una duplicación entre Inspector y Timeline (extraída a `board_metrics.py`). Primer certificado real contra Apple Developer (`v0.3.3`) encontró y corrigió tres fallos que ningún build sin firmar podía revelar (datos sueltos de Nuitka fuera de `Resources/`, `notarytool --wait` que no comprobaba el estado, binarios de Qt sin extensión saltándose la firma).
- **Deuda de proceso repetida y registrada, no corregida a posteriori** (`DT-0021`/`DT-0022`): `IDE-0019` y `IDE-0020` (claves de API con cuota mensual + Stripe para overage, `v0.3.3`) se construyeron y comitieron antes de pasar por el Backlog, incumpliendo la norma 1 de `MASTERPLAN.md`. Sin impacto en usuario ni código — impacto en trazabilidad, registrado como tal en vez de fabricar un bloque previo ficticio. `IDE-0021` en adelante sí se dio de alta antes de construirse.
- **Barrido de gaps de Studio identificados en la auditoría de documentación del 01/08** (`v0.3.4`-`v0.3.7`): exportar DXF/JSON (`IDE-0022`), miniaturas/favorita/fragmentación/nº de cortes en el Comparador (`IDE-0023`), vista previa de import CSV (`IDE-0024`), diálogo de Preferencias con tema persistente (`IDE-0025`), categorías y filtro en el Timeline (`IDE-0026`), ids legibles de solución A/B/C+hash (`IDE-0027`), generador de piezas de contenedor — caja simple y luego cajón sin rieles (`IDE-0028`/`IDE-0031`), importar tableros CSV (`IDE-0029`) y reparto por mejor ajuste entre tableros (`IDE-0030`).
- **Pulido visual encontrado usando la app de verdad, no en revisión de código** (`v0.3.6`-`v0.3.11`): asset de macOS de `.zip` a `.dmg`; nombre del menú de macOS mostrando "app" en vez de "BoardComposer Studio"; iconos deshabilitados casi invisibles sobre el gradiente del toolbar; pestaña sin seleccionar de un dock tabificado ilegible en tema oscuro; botones flotar/cerrar de la cabecera de los docks casi invisibles en tema oscuro; etiqueta de pieza desbordando el rectángulo en piezas estrechas. Mismo patrón en los cuatro últimos: color explícito en vez de confiar en el pintado nativo de Qt, que ignora la paleta de la app.
- **Última tanda pedida directamente por el usuario en sesiones de UAT sobre releases reales** (`v0.3.9`/`v0.3.12`): buscar actualizaciones desde el menú Ayuda (`IDE-0032`, consulta la API de GitHub bajo demanda, nunca descarga ni instala nada), nombres largos indistinguibles en el selector "Mover a tablero" y en la vista previa de import CSV. Y en `v0.3.13`, en la misma pasada: "Acerca de" en el menú Ayuda (`IDE-0033`), clave de API de Anthropic configurable en Preferencias (`IDE-0034` — un `.app` abierto con doble clic no hereda variables de entorno de una Terminal, así que el Asistente caía en `MockAIProvider` sin ninguna pista de por qué) y separar "quitar del tablero" de "eliminar del proyecto" (`IDE-0035` — Backspace hacía las dos cosas a la vez, sin forma de recuperar la pieza salvo deshacer).

Todos los frentes P0-P2 de `DOC-003-Roadmap.md` completos. El único frente abierto es la Fase 5 (Ecosistema, 🟡 En curso): biblioteca de materiales y comunidad siguen sin empezar; marketplace público sigue sin acotar más allá de la guía de plugins (`IDE-0013`) y la visibilidad de plugins instalados (`IDE-0015`) ya construidas.

## 2026-08-08 - Release v0.3.16

Tres releases desde `v0.3.13` (07/08 a 08/08):

- **Soporte multi-proveedor en el Asistente IA** (`v0.3.14`, `IDE-0036`): además de Anthropic, ahora se puede elegir OpenAI, Google Gemini u Ollama (local, sin clave) desde Preferencias. Verificado con una clave real de OpenAI — SDK, resolución de proveedor y una pregunta con contexto de proyecto real respondidas correctamente. Elegir un proveedor sin clave configurada podía tumbar el arranque de Studio (OpenAI/Gemini lanzan de inmediato si falta la clave, a diferencia de Anthropic); `AssistantService` ahora cae a respuestas de ejemplo con el motivo visible.
- **El `.app` de `v0.3.14` no arrancaba en absoluto** (`v0.3.15`, `DT-0023`): `google-genai` resuelve buena parte de su subsistema interno con `importlib.import_module()` sobre un nombre calculado en tiempo de ejecución en vez de imports literales — invisible para el análisis estático de Nuitka. CI en verde no lo detectó porque notarizar solo valida la firma, nunca ejecuta el binario; el primer arranque real fue el del usuario tras descargar la release, diagnosticado pidiéndole que lo abriera desde Terminal para ver el traceback que Finder se traga en silencio. `studio/pysidedeploy.spec` fuerza ahora el empaquetado completo de `google.genai` y `openai`.
- **Columna `quantity` opcional en el import CSV** (`v0.3.16`, `IDE-0037`): pedido por el usuario porque el diálogo "Pieza"/"Tablero" ya tenía un campo "Cantidad" que nunca llegó al CSV — una fila con `quantity` > 1 se expande a N piezas/tableros idénticos con ids derivados por sufijo, determinista en vez de probar el siguiente sufijo libre en silencio como hace el diálogo: cualquier colisión aborta toda la importación.

## 2026-08-09 - Release v0.3.17

`IDE-0038`, pedido por el usuario para ampliar `IDE-0037` a los tres formatos de CSV (Core, piezas y tableros de Studio) con `quantity` y `material`, en ese orden. Investigar el alcance real sacó a la luz que el Core y Studio no son simétricos:

- **El Core nunca ha tenido `material`** — el único "material" que existía era `material_usage_score`, una métrica del solver (% de aprovechamiento), sin relación con un tipo de madera. Se añadió como campo pasivo en `Board` (se guarda, se expone, no afecta al solver) porque el Core solo empaqueta piezas sobre **una única lámina implícita** (`ProjectConstraints`) — no hay varias tablas entre las que el solver pueda elegir por material. Intentar que "afectara al solver" ahí, como se pidió al principio, no tenía nada que emparejar: hacerlo de verdad exigiría convertir el Core a multi-lámina con material, un cambio de arquitectura mucho mayor que quedó fuera de alcance, a registrar aparte si hace falta.
- **En Studio sí hay varias `StudioBoard` reales**, así que ahí `material` sí pasa de etiqueta a **restricción dura** — mismo patrón exacto que ya existía para `thickness_mm` desde hace varias releases (una pieza de un grosor no encaja en un tablero de otro): mismo `!=` sin comodín, en los mismos puntos de llamada (`LayoutService.to_core_project()`/`apply_best_fit_distribution()`, `MainWindow._edit_board()`/`_edit_piece()`/`_move_piece_to_board()`), nunca dentro de `piece_fits_on_board()` (geometría pura, tampoco comprueba grosor).
- **Lección de proceso**: la primera respuesta a "¿qué alcance debe tener material?" fue "con efecto en el solver" sin que existiera, en el Core, ningún mecanismo con el que ese efecto pudiera engancharse — el diseño se corrigió a mitad de camino, con el usuario, en cuanto se investigó el dominio real en vez de asumir que Core y Studio comparten arquitectura de colocación. 993 tests en verde (15 nuevos sobre `v0.3.16`).
