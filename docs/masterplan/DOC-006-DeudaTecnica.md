

# BoardComposer

## Documento 6 — Gestión de la Deuda Técnica

**Código:** DOC-006
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 01/07/2026

---

## Objetivo

Registrar, clasificar y gestionar toda la deuda técnica del proyecto BoardComposer para asegurar que el crecimiento del producto no comprometa su calidad, mantenibilidad ni capacidad de evolución.

La deuda técnica es un elemento normal del desarrollo. El objetivo no es eliminarla por completo, sino hacerla visible, controlarla y decidir conscientemente cuándo asumirla o resolverla.

---

## Principios

- Toda deuda técnica conocida debe registrarse.
- La deuda nunca debe depender de la memoria del equipo.
- Cada elemento tendrá una prioridad y un impacto estimado.
- La deuda técnica forma parte de la planificación del producto.
- Ninguna deuda crítica podrá permanecer indefinidamente sin revisión.

---

## Clasificación

### DT-A — Arquitectura
Problemas de diseño estructural.

### DT-C — Código
Duplicación, complejidad o refactorizaciones pendientes.

### DT-T — Tests
Cobertura insuficiente o pruebas mejorables.

### DT-D — Documentación
Documentación incompleta o desactualizada.

### DT-P — Rendimiento
Aspectos relacionados con optimización y escalabilidad.

### DT-UX — Experiencia de usuario
Limitaciones conocidas en la interfaz o flujo de trabajo.

---

## Formato de un registro

```text
DT-0001

Título

Categoría

Prioridad

Descripción

Impacto

Riesgo

Propuesta de resolución

Documentos relacionados

Estado
```

---

## Registro inicial

| ID | Categoría | Descripción | Estado |

|----|-----------|-------------|--------|
| DT-0001 | DT-D | Completar la documentación funcional de BoardComposer Studio. | 🟡 Pendiente |
| DT-0002 | DT-A | Revisar y documentar la arquitectura interna del Solver tras la incorporación de nuevos algoritmos. | 🟡 Pendiente |
| DT-0003 | DT-T | Mantener la cobertura de pruebas por encima del objetivo definido. | 🟢 Controlado |

---

## Política de gestión

- La deuda técnica deberá revisarse al cierre de cada Sprint.
- Ninguna versión mayor del producto se publicará sin revisar este documento.
- Las deudas resueltas permanecerán registradas como histórico.
- La prioridad podrá modificarse, pero nunca desaparecerá el registro.

---

## Relación con otros documentos

- DOC-002 — Arquitectura.
- DOC-003 — Roadmap.
- DOC-004 — Backlog.
- DOC-005 — Registro de Decisiones.
- ADR relacionados.

---

## Estado

**Estado actual:** 🟡 En revisión

Pendiente de:

- definir métricas de deuda técnica;
- establecer umbrales de aceptación por versión;
- integrar este documento en el proceso de cierre de Sprint.