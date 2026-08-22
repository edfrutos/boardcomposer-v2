# BoardComposer

## Documento 3 — Roadmap del Producto

**Código:** DOC-003
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 22/08/2026

---

## Objetivo

Definir la evolución prevista de BoardComposer mediante fases, hitos y prioridades, proporcionando una visión clara del desarrollo del producto a corto, medio y largo plazo.

---

## Principios

El Roadmap representa la dirección del proyecto, no una planificación cerrada. Podrá evolucionar conforme aparezcan nuevas necesidades, siempre respetando el Manifiesto y la Arquitectura.

---

## Fase 1 — Core (Completada)

**Estado:** 🟢

Objetivos alcanzados:

- Motor de optimización desacoplado.
- Algoritmos Skyline y MaxRects.
- Beam Search.
- Sistema de evaluación.
- Exportadores básicos.
- Cobertura amplia mediante pruebas automatizadas.

---

## Fase 2 — BoardComposer Studio (Completada)

**Estado:** 🟢

Objetivo:

Construir la aplicación visual profesional para explorar, comparar y comprender soluciones de corte.

Entregables principales:

- Workspace. 🟢 (IDE-0001)
- Comparador de algoritmos. 🟢 (IDE-0002)
- Inspector de piezas. 🟢 (IDE-0003)
- Panel de propiedades. 🟢 (cubierto por el Inspector, IDE-0003)
- Gestión de proyectos. 🟢 (IDE-0004)
- Exportación visual. 🟢 (SVG/PDF, IDE-0005)
- Alta/edición de tableros y piezas, y soporte multi-tablero. 🟢 (`DT-0013`, `docs/masterplan/DOC-006-DeudaTecnica.md`)
- Tema visual, iconos y toolbar. 🟢 (`IDE-0016`)
- Importación de piezas desde CSV. 🟢 (`IDE-0018`)
- Buscar actualizaciones / "Acerca de". 🟢 (`IDE-0032`, `IDE-0033`)
- Separar "quitar del tablero" de "eliminar del proyecto". 🟢 (`IDE-0035`)
- Import CSV con `quantity`/`material` en español y sin distinguir mayúsculas, en los tres formatos (Core, piezas y tableros de Studio). 🟢 (`IDE-0037`, `IDE-0038`, `DT-0026`)
- Menú contextual en el lienzo (pieza/tablero) + "Eliminar tablero". 🟢 (`IDE-0040`)
- Auto-actualización: descargar y abrir el `.dmg`, y sustituir el `.app` en marcha + relanzar. 🟢 (`IDE-0043`, `IDE-0045`) — el relanzado (`DT-0029`) está mitigado pero pendiente de reconfirmar contra un ciclo real (`v0.3.36`).

---

## Fase 3 — Plataforma

**Estado:** 🟢 Completada

Incluye:

- API pública. 🟢 (IDE-0006: `/health`, `/strategies`, `/solve`; ver `docs/architecture.md`)
- Automatización. 🟢 (DEC-0009: cubierta por el mecanismo de plugins de `IDE-0008` — generadores, estrategias, importadores/exportadores instalables vía entry points; sin entrega nueva propia)
- Integraciones. 🟢 (DEC-0010: cubierta por los importadores/exportadores registrables de `IDE-0008` Fase D; sin entrega nueva propia)
- Servicios remotos. 🟢 (IDE-0009: autenticación por clave de API vía `BOARDCOMPOSER_API_KEY`, rate limiting con Flask-Limiter, `gunicorn` como servidor WSGI de producción; ver `docs/architecture.md`)
- Despliegue Cloud. 🟢 (IDE-0014: Dockerfile + receta Fly.io/VPS+Caddy; IDE-0017: tercera opción VPS+Plesk verificada con un despliegue privado real y en marcha — `docs/deploy.md` — y Studio accesible por navegador vía escritorio remoto VNC/noVNC — `docs/deploy-studio-remote.md`)

---

## Fase 4 — Inteligencia

**Estado:** 🟢 Completada (Fases A–F de IDE-0007)

Objetivos:

- Asistencia mediante IA. 🟢 (`AssistantService`/chat en Studio, Fase E)
- Explicaciones inteligentes. 🟢 (`explain_solution()`, Fase C)
- Recomendación automática de estrategias. 🟢 (`suggest_strategy()`, Fase D)
- Análisis avanzado de soluciones. 🟢 (generación de proyecto desde texto, Fase B; expuesto vía API, Fase F)

Soporte multi-proveedor. 🟢 (`IDE-0036`): además de Anthropic (Claude), el usuario puede elegir OpenAI (GPT), Google Gemini u Ollama (local, sin clave) desde Preferencias — clave de Anthropic también configurable ahí (`IDE-0034`), sin depender de variables de entorno heredadas de una Terminal. `AssistantService._resolve_provider()` cae a respuestas de ejemplo con el motivo visible si el proveedor elegido no tiene credenciales, en vez de tumbar el arranque de Studio. Verificado con claves reales de Anthropic y OpenAI; Gemini/Ollama sin verificar contra credenciales/servidor reales.

---

## Fase 5 — Ecosistema

**Estado:** 🟡 En curso

Objetivos:

- Plugins. 🟢 (IDE-0008, Fases A–E completas: generadores, estrategias, importadores/exportadores y paneles de Studio registrables vía entry points de Python)
- Marketplace. 🟡 (guía para desarrolladores de plugins completada — `IDE-0013`, `DEC-0011`, `docs/plugins.md`; visibilidad de plugins instalados completada — `IDE-0015`, `DEC-0013`, CLI `boardcomposer plugins` + API `GET /plugins`; marketplace público sigue sin acotar, `DOC-999-Ideas.md`)
- Biblioteca de materiales. 🟢 Completado (`IDE-0041`, `DEC-0020`, catálogo del taller exportable/importable como CSV, `v0.3.23`).
- Inventario de retales. 🟢 Completado (`IDE-0039`, persistente en SQLite, `v0.3.18`), enlazado a la biblioteca de materiales como consulta (`IDE-0042`, `v0.3.24`) y priorizable al añadir un tablero (`IDE-0044`, `v0.3.26`) — deliberadamente sin afectar al solver en ningún punto (`DEC-0019`, `DEC-0022`).
- Comunidad. ⚪ Sin empezar.

---

## Prioridades actuales

Studio, API, IA, Plugins y Plataforma (antes P0–P2) ya están completos — ver arriba. El endurecimiento para producción (`IDE-0009`) y el empaquetado de Studio (`IDE-0011`, `pyside6-deploy`, `.app` de macOS) también están completos (`docs/masterplan/DOC-004-Backlog.md`). No quedan prioridades P0/P1 pendientes; las prioridades reales hoy son:

### Prioridad P2

- Exportación DXF. 🟢 Completado (`IDE-0012`, `solution_to_dxf()`, SDK `ezdxf`).
- Guía para desarrolladores de plugins. 🟢 Completado (`IDE-0013`, `DEC-0011`, `docs/plugins.md`) — primer paso concreto de Marketplace/Comunidad (Fase 5); biblioteca de materiales y marketplace público siguen sin acotar (`DOC-999-Ideas.md`).
- Receta de despliegue Cloud. 🟢 Completado (`IDE-0014`, `DEC-0012`, `Dockerfile` + `docs/deploy.md`, Fly.io o VPS+Caddy); instancia demo pública y SaaS completo (cuentas, persistencia por usuario) siguen sin acotar. Modelo híbrido Studio gratis + API de pago decidido y construido sin esperar al SaaS completo (`DEC-0018`, `IDE-0020`/`IDE-0021`, `DOC-999-Ideas.md`).
- Visibilidad de plugins instalados. 🟢 Completado (`IDE-0015`, `DEC-0013`, CLI `boardcomposer plugins` + API `GET /plugins`) — segundo paso de Marketplace/Comunidad (Fase 5); biblioteca de materiales y marketplace público siguen sin acotar (`DOC-999-Ideas.md`).

---

## Criterios para modificar el Roadmap

Toda modificación deberá:

- aportar valor al usuario;
- mantener la coherencia con el Manifiesto;
- respetar la arquitectura definida;
- quedar registrada en el historial de decisiones.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- descomponer las fases en épicas (EP);
- vincular los futuros sprints;
- incorporar estimaciones y dependencias;
- aprobar como hoja de ruta oficial del proyecto.
