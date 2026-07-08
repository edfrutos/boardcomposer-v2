# BoardComposer

## Documento 2 — Arquitectura del Sistema

**Código:** DOC-002
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 01/07/2026

---

## Objetivo

Definir la arquitectura de BoardComposer, estableciendo la organización de sus componentes, las dependencias permitidas y los principios que deberán respetarse durante toda la vida del proyecto.

---

## Principio fundamental

La arquitectura de BoardComposer se basa en una única premisa:

> **El Core es el corazón del sistema y nunca dependerá de ninguna interfaz de usuario.**

Toda aplicación, servicio o integración deberá construirse alrededor del Core, nunca dentro de él.

---

## Arquitectura general

```text
                 BoardComposer
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
      Studio          CLI            API
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
               BoardComposer Core
                       │
     ┌─────────────────┼──────────────────┐
     ▼                 ▼                  ▼
  Domain            Solver           Exporters
     │                 │                  │
     └─────────────────┼──────────────────┘
                       ▼
                  Geometry Engine
```

---

## Componentes

### Core

Contiene toda la lógica de negocio y optimización. No conocerá ningún detalle de la interfaz gráfica, servicios web o tecnologías externas.

### Studio

Aplicación visual para explorar proyectos, comparar soluciones y gestionar el flujo de trabajo del usuario.

### CLI

Interfaz de línea de comandos destinada a automatización, integración y pruebas.

### API

Capa de servicios para futuras integraciones con aplicaciones externas o despliegues remotos.

---

## Reglas arquitectónicas

1. El Core nunca importará módulos de interfaz.
2. Las interfaces consumirán el Core mediante APIs públicas.
3. Toda nueva funcionalidad deberá implementarse primero en el Core.
4. Ningún algoritmo dependerá de una tecnología concreta de presentación.
5. La arquitectura favorecerá la extensibilidad antes que la duplicación de código.

---

## Evolución prevista

La arquitectura está diseñada para admitir, sin cambios estructurales importantes:

- nuevos algoritmos de optimización;
- nuevas interfaces de usuario;
- nuevos formatos de importación y exportación;
- ejecución local o remota;
- integración con servicios de inteligencia artificial.

---

## Relación con otros documentos

- DOC-000 — Manifiesto.
- DOC-001 — Producto.
- DOC-003 — Studio.
- ADR (Architecture Decision Records).

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- validar la estructura definitiva del Core;
- documentar los módulos internos;
- incorporar diagramas de dependencias;
- aprobar la arquitectura como referencia oficial del proyecto.
