# ROADMAP - BoardComposer

> **Superado.** Este fichero es el andamiaje del primer día del proyecto
> (26/06/2026). El roadmap vivo y mantenido está en
> `docs/masterplan/DOC-003-Roadmap.md`; el backlog funcionalidad por
> funcionalidad, en `docs/masterplan/DOC-004-Backlog.md`. Se conserva aquí
> como registro histórico, sin actualizar checkbox a checkbox.

## Fase 0 - Fundamentos

- [x] Directorio raíz.
- [x] Documentación fundacional.
- [x] Estructura inicial.
- [x] Documentación técnica v0.1.
- [x] Inicializar Git.
- [x] Primer commit.

## Fase 1 - Motor mínimo 2D

- [x] Modelo Board.
- [x] Modelo Project.
- [x] Modelo AssemblySolution.
- [x] Restricciones básicas.
- [x] Motor de puntuación.
- [x] Generador de soluciones simples.
- [x] Salida por consola.
- [x] Tests unitarios.

## Fase 2 - Datos

- [x] CSV.
- [x] Excel.
- [x] JSON.
- [x] Formato .bcstudio.json (equivalente al `.bcproj` previsto).

## Fase 3 - Visualización

- [x] Dibujo 2D (workspace de BoardComposer Studio).
- [x] Comparación de soluciones.
- [x] Exportación de imagen/PDF.

## Fase 4 - Aplicación macOS

- [x] Interfaz PySide6.
- [x] Editor visual.
- [x] Panel de criterios (Inspector).

## Fases no previstas originalmente, añadidas después

- [x] API HTTP pública.
- [x] Asistente IA (proveedor pluggable; `AnthropicProvider` conectado como proveedor real).
- [x] Sistema de plugins (generadores, estrategias, importadores/exportadores, paneles de Studio).
- [x] Endurecimiento para producción (autenticación por clave, rate limiting, servidor WSGI).
- [x] Empaquetado de Studio como `.app` de macOS.
