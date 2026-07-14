# CHANGELOG - BoardComposer

## Sin publicar

### Añadido

- Proveedor de IA real para el Asistente IA (`IDE-0007`): `AnthropicProvider` sobre el SDK `anthropic`, modelo `claude-haiku-4-5`, API key vía la variable de entorno `ANTHROPIC_API_KEY`. `default_provider()` lo activa automáticamente cuando esa variable está definida, con `MockAIProvider` como fallback; usado por defecto en la API (`create_app()`) y en el chat de Studio (`AssistantService`).
- Endurecimiento para producción de la API (`IDE-0009`): autenticación opcional por clave (`BOARDCOMPOSER_API_KEY` vía cabecera `X-API-Key`), rate limiting con Flask-Limiter (60 peticiones/minuto por IP, `/health` exenta) y `gunicorn` como servidor WSGI de producción (dependencia opcional `pip install -e ".[prod]"`, `make serve`).
- Importación desde Excel (`IDE-0010`, cierra RF-002): `load_project_from_excel()` (SDK `openpyxl`), mismas columnas que el CSV existente; registrada en `IMPORTER_REGISTRY` como `"xlsx"` y expuesta en la CLI con `--excel` (mutuamente excluyente con `--csv`).
- Empaquetado de BoardComposer Studio como `.app` de macOS (`IDE-0011`): `pyside6-deploy` (`make package`, dependencia opcional `pip install -e ".[package]"`), nuevo punto de entrada `boardcomposer-studio`, y publicación automática como asset de release de GitHub al crear un tag `v*` (`.github/workflows/package-studio.yml`).

### Corregido

- `project_from_text()`/`suggest_strategy()` fallaban con un proveedor de IA real: Claude envuelve el JSON en un bloque ` ```json ... ``` ` pese a que el prompt pide lo contrario, y devuelve `thickness_mm: null` explícito en vez de omitir la clave. Corregido con `strip_json_fence()` y tratando el `null` explícito igual que una clave ausente.

## 0.1.0 - 2026-07-13

### Añadido

- Motor: generadores skyline, MaxRects y beam search; estrategias `balanced`/`material`/`compact`.
- CLI: entrada CSV, salida texto/JSON, selección de estrategia (IDE-0004).
- BoardComposer Studio (PySide6): workspace interactivo (IDE-0001), comparador de algoritmos (IDE-0002), inspector de piezas (IDE-0003), gestión de proyectos `.bcstudio.json` (IDE-0004), exportación SVG/PDF (IDE-0005), aviso de cambios sin guardar al cerrar.
- API HTTP pública (IDE-0006): `/health`, `/strategies`, `/solve`.
- Asistente IA (IDE-0007, Fases A–F): puerto `AIProvider` pluggable, generación de proyecto desde texto libre, explicación de soluciones en lenguaje natural, sugerencia de estrategia, chat contextual en Studio, y las tres capacidades anteriores expuestas vía `/assist/*` — todo sobre `MockAIProvider`, sin proveedor real conectado todavía.
- Sistema de plugins (IDE-0008, Fases A–E): descubrimiento vía *entry points* de Python; generadores, estrategias, importadores/exportadores y paneles de Studio registrables por terceros.
- Límite de tamaño de proyecto en la API (`MAX_BOARDS = 100`) para evitar peticiones lentas con proyectos grandes.

### Decisiones

- Los plugins se registran vía *entry points* estándar de Python (`importlib.metadata`), no un cargador propio.
- La IA nunca genera geometría directamente: solo ajusta parámetros del solver determinista existente (pesos de puntuación, generadores a usar).
- Los nombres integrados (generadores, estrategias, importadores, exportadores) siempre tienen prioridad sobre un plugin que repita el nombre.

## 0.0.1 - 2026-06-26

### Añadido

- Documentación fundacional.
- Estructura base del proyecto.
- Backlog inicial.
- Documentación técnica v0.1.

### Decisiones

- Inicio con ensamblaje 2D.
- Núcleo independiente de la interfaz.
- Soluciones explicables.
