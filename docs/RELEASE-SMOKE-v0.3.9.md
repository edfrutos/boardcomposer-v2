# Checklist de verificación visual manual — v0.3.9

Esta checklist es para ojo humano: todo lo que un chequeo automatizado
(pytest, CLI, API, captura headless) no puede juzgar por sí solo —
contraste real, legibilidad, que un icono no "desaparezca", que un menú
diga lo que tiene que decir. El chequeo operativo automatizado (875 tests,
CLI, API, arranque headless de Studio) ya se hizo aparte y está en verde;
esto lo complementa, no lo repite.

**Entorno:** `.dmg` de v0.3.9
(https://github.com/edfrutos/boardcomposer-v2/releases/tag/v0.3.9) o
Studio remoto (`studio.efjdefrutos.com`, si ya está reconstruido con el
código actual). Prueba en **claro y oscuro** salvo que se indique lo
contrario — varios de los bugs de esta lista solo se veían en una de las
dos paletas.

**Nota:** el punto 2 (botones flotar/cerrar de los docks) se detectó
durante la primera pasada de este checklist (06/08/2026) y ya está
corregido en `main` — pendiente de entrar en la siguiente release para
verificarse contra un `.dmg` real; hasta entonces solo es verificable
en Studio remoto si ya está reconstruido con el código actual.

---

## 0. Arranque

- [ ] La app abre sin errores: ventana principal con Explorer, lienzo,
      toolbar y docks visibles.
- [ ] **Ver → Tema** (o **Editar → Preferencias… / Ctrl+,**) permite
      cambiar entre claro / oscuro / automático sin reiniciar.
- [ ] La barra de menú superior de macOS (negrita, arriba del todo)
      muestra **"BoardComposer Studio"**, no "app" ni el bundle id
      (`com.efjdefrutos.boardcomposer.studio`). *(Solo aplica al `.app`
      real de macOS — no se puede comprobar en Studio remoto/web.)*
- [ ] "Nuevo proyecto" crea un proyecto vacío sin errores.

## 1. Contraste de iconos deshabilitados (fix v0.3.8)

Guía concreta para identificarlo — compara el **mismo icono** en su
estado activo vs. deshabilitado, no solo "si se ve bien" en general:

- [ ] Abre **"Nuevo proyecto"**: el toolbar queda con casi todo
      deshabilitado (deshacer/rehacer — flechas curvas, 2º y 3er icono
      — y también "Eliminar pieza", "Calcular layout", etc.). Esos
      iconos deben verse **atenuados pero con el trazo reconocible**
      (gris translúcido sobre el degradado de color de la barra), no
      completamente borrados/invisibles.
- [ ] Añade una pieza y selecciónala: los iconos que dependen de esa
      selección (p. ej. "Eliminar pieza", "Rotar") pasan de atenuados a
      color completo — la diferencia entre los dos estados debe ser
      obvia a simple vista.
- [ ] Repite el mismo contraste atenuado/activo en modo oscuro.

## 2. Contraste de los botones de flotar/cerrar en la cabecera de los docks

**Este es el bug real encontrado en UAT — no las pestañas (ver punto
3, que si funciona bien).** Cada dock (Explorer, Asistente, Inspector,
Timeline, Comparador…) tiene dos botones pequeños arriba a la derecha
de su cabecera: uno para **flotar/anclar** la ventana (cuadrado) y otro
para **cerrarla** (aspa). `theme.py` nunca les puso una regla propia,
así que quedan con el icono gris nativo de Qt/Fusion — apenas
distinguible contra la cabecera oscura del dock en tema oscuro.

- [ ] En **tema oscuro**, mira la cabecera de "Explorer" o "Asistente":
      los dos botones (flotar / cerrar) arriba a la derecha son casi
      del mismo color que el fondo de la cabecera — confirma que
      cuesta verlos, casi hay que saber que están ahí.
- [ ] En **tema claro**, los mismos botones sí se distinguen con
      claridad — el problema es específico del tema oscuro.
- [ ] Pendiente de arreglo (aún no corregido, a diferencia de las
      pestañas de dock tabificado).

## 3. Contraste de pestañas de dock tabificado (fix v0.3.9 — ya corregido)

Los docks **Timeline/Comparador** están tabificados entre sí, igual que
**Inspector/Asistente**. Este punto es solo regresión — ya se arregló.

- [ ] En el dock inferior, las pestañas "Timeline" y "Comparador" son
      **legibles las dos**, seleccionada y sin seleccionar, en claro y
      en oscuro.
- [ ] Al hacer clic en la pestaña no seleccionada, cambia de panel y
      pasa a resaltarse con el color de acento (no el gris plano).
- [ ] Pasar el ratón por encima de una pestaña sin seleccionar la
      resalta (hover) antes de hacer clic.
- [ ] Repite los tres puntos anteriores con **Inspector/Asistente**.

## 3. Recorrido visual por pantallas

### Workspace (lienzo)

- [ ] Cuadrícula, reglas y piezas se distinguen con claridad en ambos
      temas.
- [ ] Seleccionar una pieza la resalta visualmente (borde/color de
      selección) sin ambigüedad.
- [ ] Arrastrar una pieza dentro del tablero se ve fluido, sin
      parpadeos ni piezas "fantasma" residuales.

### Explorer (panel izquierdo)

- [ ] Árbol Proyecto → Tableros / Piezas con iconos y texto legibles.
- [ ] Seleccionar un tablero en el árbol cambia el tablero activo del
      lienzo.

### Inspector

- [ ] Con una pieza seleccionada, el Inspector muestra sus propiedades
      (dimensiones, posición, rotación) de forma legible.
- [ ] Sin nada seleccionado, el estado vacío es un mensaje real, no un
      panel en blanco.

### Comparador

- [ ] **Comparar → Generar comparación** produce una tabla con
      miniaturas de cada solución — miniaturas nítidas, no borrosas ni
      en negro.
- [ ] La solución favorita (si se marca una) se distingue visualmente
      de las demás.
- [ ] Sin soluciones generadas, el estado vacío es un mensaje real
      ("No hay soluciones para comparar…"), no un panel en blanco.

### Timeline / Actividad

- [ ] El dock muestra un resumen de tableros (piezas, % de uso) y un
      log de actividad en vivo — ambos legibles, no solo texto plano
      sin tratamiento.
- [ ] Realizar una acción (añadir pieza, generar comparación) añade una
      entrada nueva visible en el log sin recargar manualmente.

### Asistente

- [ ] El placeholder inicial ("Escribe una pregunta…") es legible en
      ambos temas.
- [ ] Escribir una pregunta y pulsar Intro (o el botón de envío)
      produce una respuesta visible en el panel, sin que el layout se
      rompa con texto largo.

### Preferencias (Editar → Preferencias…, Ctrl+,)

- [ ] El diálogo abre centrado, con el selector de tema (claro/oscuro/
      automático) legible y usable.
- [ ] Cambiar el tema desde aquí se aplica de inmediato a toda la
      ventana principal, docks incluidos.
- [ ] Cerrar y reabrir Studio conserva el tema elegido (persistencia).

### Exportación (menú Exportar)

- [ ] **Exportar SVG…** / **Exportar PDF…** / **Exportar DXF…** /
      **Exportar JSON…** abren cada uno un `QFileDialog` nativo sin
      errores.
- [ ] El archivo exportado de cada formato se abre correctamente fuera
      de Studio (visor de SVG/PDF, editor de texto para JSON, CAD o
      visor DXF) y el layout coincide visualmente con el lienzo.

## 4. Flujos con piezas/tableros

- [ ] **Archivo → Importar tableros (CSV)…** y **Archivo → Importar
      piezas (CSV)…** muestran vista previa antes de confirmar,
      legible y con las columnas esperadas.
- [ ] **Herramientas → Generar piezas de contenedor…** — probar las dos
      opciones del combo (Caja simple / Cajón sin rieles): los campos
      que se muestran/ocultan cambian según el tipo elegido, sin
      parpadeos ni campos huérfanos.
- [ ] **Herramientas → Repartir piezas entre tableros (mejor ajuste)**
      informa al final cuántas piezas se colocaron, en un mensaje
      legible (no un diálogo cortado o desbordado).
- [ ] Añadir/editar/borrar una pieza a mano sigue funcionando y se
      refleja de inmediato en Explorer + lienzo.
- [ ] **Ctrl+Z / Ctrl+Y** deshacen/rehacen cada acción anterior una a
      una, con el estado del lienzo consistente en cada paso.

## 5. Regresión rápida

- [ ] Guardar proyecto (`.bcstudio.json`) y volver a abrirlo conserva
      tableros/piezas/layout/tema.
- [ ] Redimensionar la ventana principal no rompe el layout de los
      docks (paneles no se solapan ni desaparecen).
- [ ] Ningún texto se ve cortado, desbordado o superpuesto en ninguna
      de las pantallas anteriores, en ninguno de los dos temas.

---

Cualquier fallo: anota pasos exactos para reproducir + captura de
pantalla, y se lleva a `DOC-004-Backlog.md` como incidencia.
