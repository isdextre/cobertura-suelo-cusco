# Notebooks

Flujo de análisis, en orden de ejecución. **Una pregunta por notebook**, y el nombre dice el
resultado, no la herramienta.

Cada notebook consume lo que produjo el anterior y produce lo que necesita el siguiente. Nada se
calcula dos veces en dos lugares que puedan divergir.

| # | Notebook | Pregunta que responde | Estado |
|---|---|---|---|
| 01 | `01_area_de_estudio.ipynb` | ¿Dónde medimos? | Ejecutado |
| 02 | `02_referencia_cobertura.ipynb` | ¿De qué está hecho el territorio y dónde está el pajonal? | Ejecutado |
| 03 | `03_referencia_fuego.ipynb` | ¿Dónde y cuándo se quemó? | Por ejecutar |
| 04 | `04_serie_anual_landsat.ipynb` | ¿Cómo se ve cada año? | Ejecutado |
| 05 | `05_deteccion_cambio.ipynb` | ¿Dónde y cuándo cambió la trayectoria? | Por ejecutar |
| 06 | `06_control_deteccion.ipynb` | ¿Podemos creerle a esa detección? | Por ejecutar |
| 07 | `07_tipo_de_cambio.ipynb` | ¿Qué fue cada cambio? | Por crear |
| 08 | `08_atribucion_climatica.ipynb` | ¿Cuánto es sequía y cuánto no? | Por crear |
| 09 | `09_validacion.ipynb` | ¿Qué tan exacto es? | Por crear |
| 10 | `10_indicadores_entregables.ipynb` | Las cifras finales | Por crear |

## La cadena de insumos

Cada flecha es un asset de Earth Engine o un archivo. Si falta uno, el notebook que lo necesita lo
dice y nombra dónde generarlo: **ninguno reconstruye por su cuenta lo que debería leer**, porque eso
es justo lo que crea definiciones divergentes.

```
01  →  cusco_01_aoi                    área de estudio
02  →  cusco_02_mascara                pajonal + máscara de análisis
03  →  cusco_03_quema_aparicion        quema por año de APARICIÓN (desfase resuelto)
04  →  cusco_04_serie_anual            13 imágenes, 7 índices + n_obs
05  →  cusco_05_resultado              segmentos, pre/post, rmse, confianza
06  →  (solo CSV de control)
```

### Por qué tantos assets

Earth Engine **no guarda resultados intermedios**: una colección construida en un notebook es una
*receta*, no un conjunto de imágenes. Cada vez que se pide un número, la receta se ejecuta entera
desde las escenas crudas. Con el medoide de 13 años y LandTrendr encima, el cómputo por tesela
desborda la memoria (`Computed image is too large`).

Exportar a un asset convierte la receta en imágenes de verdad. A partir de ahí leer un píxel es leer
un píxel. Por eso cada notebook termina con una celda de exportación marcada con un flag
(`EXPORTAR_* = False` por defecto): hay que ponerla en `True` **una sola vez**.

## Carpetas de salida

Llevan el número del notebook que las genera, para que cualquier archivo se trace a su origen sin
preguntar:

```
outputs/
├── 01_area_de_estudio/        area_estudio.geojson
├── 02_referencia_cobertura/   areas_por_clase.csv · matrices_transicion.csv · indicadores_referencia.csv
├── 03_referencia_fuego/       area_quemada_mensual.csv · area_quemada_anual.csv · quema_en_pajonal_por_anio.csv
├── 04_serie_anual_landsat/    disponibilidad_anual.csv · indices_anual_YYYY.tif
├── 05_deteccion_cambio/       degradacion_segmentos.tif · negTCW_ajustado.tif · parametros_corrida.csv
└── 06_control_deteccion/      sensibilidad_maxsegments.csv · estabilidad_2025.csv · distribucion_rmse.csv
```

## El estándar de estilo

El notebook **04** es la referencia: constantes parametrizadas al inicio, una celda markdown que
explica el *porqué* antes de cada bloque de código, diagnóstico de la calidad de los datos, control
visual y celda de resumen al final. Los demás siguen ese formato.

Cada notebook arranca con una tabla de **qué consume** y **qué produce**, nombrando archivos y assets
concretos.

## Trampas conocidas

Errores que ya se cometieron y se corrigieron. Si vuelven a aparecer, el código falla o —peor— da
resultados silenciosamente equivocados:

- **`copyProperties()` devuelve un `ee.Element`, no un `ee.Image`.** Hay que volver a castear con
  `ee.Image(...)` o el siguiente `.updateMask()` falla.
- **Las capas apiladas necesitan `.rename()` con un nombre común.** Las bandas se llaman
  `classification_YYYY` y los reductores de `ImageCollection` exigen nombres consistentes.
- **El índice primario (`negTCW`) NO tiene banda `_fit`.** Solo los acompañantes la tienen. Sus
  valores ajustados salen de la fila 2 del array `LandTrendr`.
- **Todo `reduceRegion` y todo `sample()` lleva `tileScale`.** Sin eso aparece
  `Computed image is too large`.
- **Nunca evaluar varias reducciones con `ee.List([...]).getInfo()`.** Earth Engine las lanza en
  paralelo y responde `Too many concurrent aggregations`. Usar `evaluar_serie()`.
- **La banda 0 de cada imagen es la que LandTrendr usa para segmentar.** Hay que pasar
  `.select(INDICES)` explícito, y `n_obs` nunca entra a LandTrendr.
- **`negTCW` está invertido a propósito:** LT-GEE exige que la pérdida de vegetación sea un delta
  positivo. No "corregir" el signo.
- **El escalado `SR = DN × 0.0000275 − 0.2` va antes de cualquier índice.** El offset no se cancela
  ni siquiera en el NDVI, que es un cociente.

## Historial

- **2026-10-23 · renumeración.** El flujo pasó a diez notebooks con una pregunta cada uno. El antiguo
  `04_landtrendr` se partió en `05_deteccion_cambio` (produce) y `06_control_deteccion` (escruta),
  lo que además eliminó las funciones de compuesto duplicadas y los errores de memoria. Se añadió
  `03_referencia_fuego`. Los notebooks 01, 02 y 04 ganaron su celda de exportación.
- **2026-10-22 · limpieza.** Se archivaron 14 notebooks del enfoque anterior (pérdida de bosque) y
  se reescribió la documentación. Ver `_archivo/MOTIVOS.txt`.

Los notebooks archivados están en `_archivo/`, con el motivo de cada uno. Si el repositorio los tenía
commiteados, siguen recuperables con `git log` y `git checkout`.
