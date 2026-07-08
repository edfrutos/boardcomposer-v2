# ADR-001 — El Core es la única fuente de verdad

**Estado:** Aceptado

**Fecha:** 01/07/2026

**Responsable:** Arquitectura de BoardComposer

---

## Contexto

BoardComposer estará formado por múltiples capas: Core, Studio, CLI, API, exportadores, automatizaciones, plugins y futuras integraciones.

Todas ellas necesitarán acceder a la lógica del sistema sin duplicarla ni reinterpretarla.

Existe el riesgo de que cada interfaz implemente parte de la lógica de negocio, provocando inconsistencias, errores y dificultades de mantenimiento.

---

## Problema

¿Dónde debe residir la lógica funcional de BoardComposer?

Las alternativas consideradas fueron:

1. Repartir la lógica entre las distintas interfaces.
2. Duplicar determinadas reglas para simplificar cada cliente.
3. Centralizar toda la lógica de negocio en un único núcleo.

---

## Decisión

Se adopta la tercera alternativa.

El **Core de BoardComposer** será la única fuente de verdad del sistema.

Toda regla de negocio deberá implementarse exclusivamente en el Core.

Las capas superiores (Studio, CLI, API, plugins o automatizaciones) actuarán únicamente como consumidores del Core, limitándose a presentar información, recoger entradas del usuario o adaptar formatos.

---

## Consecuencias

### Ventajas

- Un único comportamiento para todas las interfaces.
- Eliminación de duplicidades.
- Mayor facilidad para realizar pruebas.
- Evolución independiente de la interfaz y del motor.
- Mejor soporte para automatización y scripting.
- Base sólida para una API pública y un sistema de plugins.

### Inconvenientes

- El Core deberá diseñarse con especial cuidado.
- Algunas interfaces requerirán adaptadores adicionales.
- La disciplina arquitectónica será esencial para evitar que la lógica migre hacia capas superiores.

---

## Principios derivados

- Ninguna interfaz implementará reglas de optimización.
- Ninguna interfaz modificará directamente el estado interno del Core.
- Las decisiones funcionales pertenecerán exclusivamente al dominio.
- Toda funcionalidad nueva deberá evaluarse primero desde la perspectiva del Core.

---

## Impacto

Esta decisión afecta a:

- BoardComposer Studio.
- CLI.
- API pública.
- Plugins.
- Exportadores.
- Importadores.
- Automatizaciones.
- Integraciones futuras.

---

## Relación con otros documentos

- DOC-002 — Arquitectura.
- DOC-008 — API y Extensibilidad.
- SCR-002 — Workspace.
- FLW-003 — Generar Soluciones.

---

## Revisión futura

Esta decisión solo podrá modificarse mediante un nuevo ADR que justifique de forma explícita los beneficios y riesgos del cambio, preservando la coherencia arquitectónica del proyecto.
