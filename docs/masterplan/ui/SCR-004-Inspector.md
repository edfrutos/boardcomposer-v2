# SCR-004 — Inspector Contextual

**Módulo:** BoardComposer Studio

**Código:** SCR-004
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

El Inspector es el panel contextual inteligente de BoardComposer Studio. Su misión es mostrar únicamente la información relevante del elemento actualmente seleccionado, evitando paneles sobrecargados y reduciendo el cambio de contexto.

---

## Filosofía

El Inspector no es un panel de propiedades tradicional.

Debe responder siempre a una única pregunta:

> **¿Qué necesita saber el usuario sobre lo que tiene seleccionado en este momento?**

Su contenido cambiará dinámicamente según el contexto, manteniendo siempre la misma estructura visual.

---

## Contextos soportados

### Proyecto

- Nombre.
- Descripción.
- Materiales.
- Número de tableros.
- Número de piezas.
- Restricciones activas.
- Fecha de modificación.

### Tablero

- Dimensiones.
- Material.
- Espesor.
- Superficie utilizada.
- Desperdicio.
- Número de piezas colocadas.

### Pieza

- Referencia.
- Dimensiones.
- Rotación.
- Material.
- Canto.
- Posición.
- Coordenadas.
- Observaciones.

### Solución

- Algoritmo.
- Estrategia.
- Aprovechamiento.
- Tiempo de cálculo.
- Puntuación.
- Explicación resumida.

### Algoritmo

- Nombre.
- Descripción.
- Parámetros.
- Ventajas.
- Limitaciones.
- Casos recomendados.

---

## Distribución conceptual

```text
┌───────────────────────────────┐
│ Inspector                     │
├───────────────────────────────┤
│ Icono + Título                │
├───────────────────────────────┤
│ Propiedades principales       │
├───────────────────────────────┤
│ Métricas                      │
├───────────────────────────────┤
│ Explicación                   │
├───────────────────────────────┤
│ Acciones relacionadas         │
└───────────────────────────────┘
```

---

## Principios de interacción

- Actualización inmediata al cambiar la selección.
- Misma estructura para todos los contextos.
- Información priorizada de mayor a menor relevancia.
- Acceso directo a acciones relacionadas.
- Nunca mostrar información irrelevante para el contexto actual.

---

## Criterios de aceptación

- Cambio de contexto sin parpadeos.
- Actualización en tiempo real.
- Información comprensible sin abrir ventanas adicionales.
- Integración completa con Workspace y Comparador.

---

## Relación con otras pantallas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-005 — Proyecto.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- gráficos dinámicos;
- historial del elemento seleccionado;
- recomendaciones mediante IA;
- edición directa de determinadas propiedades;
- enlaces a documentación técnica y decisiones relacionadas.
