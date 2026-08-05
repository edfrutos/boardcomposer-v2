# Checklist de verificación manual — v0.3.7

Cubre las tres funcionalidades nuevas de esta release (`IDE-0029`,
`IDE-0030`, `IDE-0031`) más una comprobación mínima de que no hay
regresiones en lo ya existente. Marca cada casilla al probarla.

**Entorno:** `.dmg` de v0.3.7 (https://github.com/edfrutos/boardcomposer-v2/releases/tag/v0.3.7) o Studio remoto (`studio.efjdefrutos.com`, si ya está reconstruido con el código nuevo).

---

## 0. Arranque

- [ ] La app abre sin errores, ventana principal con Explorer/lienzo/toolbar visibles.
- [ ] "Nuevo proyecto" crea un proyecto vacío sin errores.

## 1. IDE-0029 — Importar tableros (CSV)

- [ ] Con un proyecto abierto (sin tablero activo necesariamente), **Archivo → Importar tableros (CSV)…** abre el diálogo.
- [ ] Prepara un CSV con columnas `id,length_mm,width_mm,thickness_mm[,material]` y 2-3 filas.
- [ ] La vista previa muestra las filas correctas antes de confirmar.
- [ ] Al aceptar, los tableros aparecen en el Explorer; el primero importado queda activo.
- [ ] **Ctrl+Z** deshace la importación tablero a tablero (no todo de golpe).
- [ ] CSV con una fila inválida (dimensión negativa o vacía) → falla todo-o-nada, ningún tablero se añade, mensaje de error claro.

## 2. IDE-0030 — Reparto por mejor ajuste entre tableros

- [ ] Proyecto con **varios tableros** (al menos uno pequeño y uno grande) y piezas sin colocar que quepan en el pequeño.
- [ ] **Herramientas → Repartir piezas entre tableros (mejor ajuste)** (o `Ctrl+Alt+M`) — no exige tablero activo.
- [ ] Verifica que prioriza el tablero **más pequeño que sea suficiente**, no el primero de la lista.
- [ ] Prueba también con un tablero **parcialmente usado** (no vacío del todo) — debe considerarse como candidato, a diferencia del reparto antiguo tablero-por-tablero.
- [ ] Mensaje final informa cuántas piezas se colocaron / cuántas quedaron sin colocar.
- [ ] No rompe el flujo existente: "Calcular layout"/"Aplicar layout" tablero por tablero sigue funcionando igual que antes.

## 3. IDE-0031 — Cajón sin rieles en el generador de contenedores

- [ ] Con un tablero activo, **Herramientas → Generar piezas de contenedor…** abre el diálogo.
- [ ] El combo "Tipo de contenedor" ofrece **dos** opciones: "Caja simple" y "Cajón sin rieles (por hueco de mueble + holgura)".
- [ ] Al elegir **Caja simple**: campos Largo/Ancho/Alto exterior visibles; campos de hueco/holgura/profundidad ocultos. Prefijo por defecto `caja`.
- [ ] Al elegir **Cajón sin rieles**: campos Ancho del hueco / Alto del hueco / Profundidad del cajón / Holgura por lado visibles; Largo/Ancho/Alto exterior ocultos. Prefijo por defecto cambia a `cajon`.
- [ ] Prueba con hueco 300×100 mm, holgura 1.5 mm, profundidad 200 mm, grosor 18 mm → vista previa con 5 piezas, dimensiones exteriores = hueco − 2×holgura.
- [ ] Holgura demasiado grande para el hueco (p. ej. hueco 10 mm, holgura 10 mm) → mensaje de error claro, no añade piezas.
- [ ] Al confirmar, las 5 piezas se añaden al tablero activo; **Ctrl+Z** las deshace una a una.
- [ ] Si personalizas el prefijo de id a mano y cambias de tipo en el combo, el prefijo personalizado **no** se pisa.

## 4. Regresión rápida

- [ ] Añadir/editar/borrar una pieza a mano sigue funcionando.
- [ ] Guardar proyecto (`.bcstudio.json`) y volver a abrirlo conserva tableros/piezas/layout.
- [ ] Exportar DXF/JSON sigue funcionando sobre un tablero con piezas colocadas.
- [ ] El generador de **caja simple** (`IDE-0028`, ya existente) sigue funcionando igual que antes de este cambio.

---

Cualquier fallo: anota pasos exactos para reproducir + captura si es visual, y lo llevamos al Backlog como incidencia.
