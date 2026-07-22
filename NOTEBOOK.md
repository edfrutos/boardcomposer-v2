
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
