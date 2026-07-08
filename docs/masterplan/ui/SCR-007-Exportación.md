# SCR-007 — Exportación

**Módulo:** BoardComposer Studio

**Código:** SCR-007
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

La pantalla de Exportación permite generar la documentación final del proyecto en distintos formatos, garantizando que la información técnica, gráfica y de producción sea consistente, reproducible y adecuada para cada destinatario.

---

## Filosofía

Exportar no consiste únicamente en guardar un archivo. Significa transformar una solución en un resultado útil para fabricación, documentación, archivo o intercambio con otros sistemas.

La exportación debe ser sencilla para el usuario y extremadamente flexible en sus posibilidades.

---

## Distribución conceptual

```text
┌────────────────────────────────────────────────────────────────────┐
│ Exportación                                                       │
├────────────────────────────────────────────────────────────────────┤
│ Solución seleccionada                                              │
├────────────────────┬───────────────────────────────────────────────┤
│ Formato            │ PDF │ SVG │ DXF │ JSON │ CSV │ Imagen         │
├────────────────────┼───────────────────────────────────────────────┤
│ Opciones           │ Escala │ Márgenes │ Calidad │ Plantilla       │
├────────────────────┼───────────────────────────────────────────────┤
│ Contenido          │ Planos │ Métricas │ Explicaciones │ Listados   │
├────────────────────┴───────────────────────────────────────────────┤
│ Vista previa                                                   │
├────────────────────────────────────────────────────────────────────┤
│ Exportar │ Guardar plantilla │ Compartir │ Cancelar               │
└────────────────────────────────────────────────────────────────────┘
```

---

## Componentes principales

### Selección de solución

- Solución activa.
- Algoritmo.
- Fecha de generación.
- Resumen de métricas.

### Formatos disponibles

- PDF.
- SVG.
- DXF.
- JSON.
- CSV.
- PNG y JPEG.

La arquitectura permitirá incorporar nuevos formatos mediante extensiones.

### Opciones de exportación

- Escala.
- Orientación.
- Tamaño de papel.
- Márgenes.
- Calidad gráfica.
- Inclusión de cotas.
- Inclusión de desperdicio.
- Inclusión de explicaciones.
- Inclusión de métricas.

### Vista previa

Representación aproximada del resultado final antes de exportar.

---

## Flujo principal

1. Seleccionar una solución.
2. Elegir el formato.
3. Configurar las opciones.
4. Revisar la vista previa.
5. Exportar.
6. Registrar la operación en el historial del proyecto.

---

## Principios de interacción

- Vista previa inmediata.
- Configuración organizada por categorías.
- Plantillas reutilizables.
- Validación antes de exportar.
- Recordar las últimas opciones utilizadas.

---

## Criterios de aceptación

- Exportación en un único paso para configuraciones habituales.
- Resultados reproducibles.
- Integridad de la información exportada.
- Compatibilidad con futuras extensiones.

---

## Relación con otras pantallas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-005 — Proyecto.
- SCR-006 — Preferencias.

---

## Evolución prevista

Versiones futuras podrán incorporar:

- exportación por lotes;
- publicación directa en servicios en la nube;
- generación automática de documentación técnica;
- integración con sistemas ERP y CAD/CAM;
- firma digital de documentos;
- perfiles de exportación específicos por cliente.

---

## Nota de diseño

Toda exportación deberá conservar la trazabilidad de la solución de origen, incluyendo el identificador del proyecto, la versión de BoardComposer, el algoritmo utilizado y la fecha de generación cuando el formato lo permita.
