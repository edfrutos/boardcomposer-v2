
# BoardComposer

## Documento 8 — API y Extensibilidad

**Código:** DOC-008
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 31/07/2026

---

## Objetivo

Definir la arquitectura de integración de BoardComposer mediante una API pública, estable y desacoplada del Core, permitiendo que aplicaciones, automatizaciones y servicios externos puedan utilizar el motor de optimización sin depender de una interfaz concreta.

---

## Principios

- El Core será la única fuente de lógica de negocio.
- La API expondrá capacidades, nunca implementaciones internas.
- La compatibilidad hacia atrás será un objetivo prioritario.
- Toda operación deberá ser reproducible y trazable.
- La API deberá ser válida para aplicaciones de escritorio, web, móviles y servicios.

---

## Objetivos funcionales

La API deberá permitir:

- crear y gestionar proyectos;
- importar piezas y tableros;
- ejecutar algoritmos de optimización;
- comparar soluciones;
- consultar métricas y explicaciones;
- exportar resultados;
- administrar configuraciones y perfiles.

---

## Arquitectura

```text
Cliente
    │
    ▼
BoardComposer API
    │
    ▼
BoardComposer Core
    │
    ├── Domain
    ├── Solver
    ├── Evaluation
    └── Exporters
```

La API actuará como una capa de adaptación entre los clientes y el Core, evitando que estos dependan de detalles internos.

---

## Versionado

Se adoptará versionado semántico para la API.

Ejemplos:

- /api/v1/
- /api/v2/

Los cambios incompatibles requerirán una nueva versión mayor.

---

## Extensibilidad

La arquitectura deberá facilitar:

- nuevos algoritmos;
- nuevos importadores y exportadores;
- proveedores de autenticación;
- asistentes basados en IA;
- plugins desarrollados por terceros.

---

## Seguridad

La especificación definitiva contemplará:

- autenticación;
- autorización;
- validación de entradas;
- limitación de uso cuando proceda;
- trazabilidad de operaciones.

Nota: ya existe una primera versión mínima de autenticación (clave de API por cabecera, opcional) y limitación de uso (rate limiting por IP) — `IDE-0009`, ver `docs/architecture.md`. `IDE-0020` añade una primera forma de autorización real: claves por cliente ligadas a un plan (`free`/`basico`/`pro`) con cuota mensual (`src/boardcomposer/billing.py`), más allá de la clave única compartida original. No sustituye la especificación definitiva de este documento (sin roles, sin trazabilidad de operaciones más allá del conteo de cuota).

---

## Relación con otros documentos

- DOC-001 — Producto.
- DOC-002 — Arquitectura.
- DOC-005 — Registro de Decisiones.
- ADR relacionados.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- definir los contratos públicos de la API;
- especificar los recursos principales;
- documentar los formatos de intercambio;
- elaborar una guía para desarrolladores e integradores.
