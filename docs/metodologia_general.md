# Metodología general · Cambio de cobertura del suelo, provincia de Cusco

**Versión:** 0.3
**Fecha:** 2026-10-10
**Cliente:** Gobierno Regional de Cusco
**Documentos relacionados:** `00_proyecto.md` (objetivos y líneas), `01_alcance.md` (alcance y decisiones de alcance), `02_datos_fuentes.md` (fuentes verificadas).

## Cómo usar esta guía

Cada paso tiene el mismo formato:

- **Objetivo:** qué resuelve.
- **Entradas:** lo que necesita.
- **Hacer:** acciones, en orden.
- **Salida:** lo que deja.
- **Criterio para avanzar:** la condición antes del siguiente paso.
- **Por definir:** lo que aún no está decidido y bloquea el paso.

Lo marcado como **Decidido** no se reabre sin acuerdo explícito.

## Decisiones vigentes

- Periodo: 2013 a 2025, 12 periodos anuales. Serie principal: Landsat 8 y 9.
- Fuentes: Landsat, MapBiomas Colección 4, GEOBOSQUES y Sentinel-2. Sin WorldCover, SRTM ni OSM.
- Método principal: LandTrendr. Sustituye a la clasificación supervisada. No se entrena ningún clasificador.
- Bosque: definición de GEOBOSQUES (MINAM). Sus umbrales se confirman en el paso 4.
- Unidad mínima de mapeo: 1 ha (unos 11 píxeles de 30 m).
- Resolución de análisis: 30 m.

## Mapa de notebooks

| Paso | Notebook | Estado |
|---|---|---|
| 1 y 2 | 01 y 02 | Ejecutados |
| 2 y 3 | 03 | Ejecutado |
| 8 (referencia MapBiomas) | 04 | Ejecutado (la propuesta de bosque no es definitiva) |
| 3 y 6 (revisión de imágenes e índice) | 05 | Sin ejecutar |
| Descarga de compuestos | 06 | Sin ejecutar. Exporta WorldCover y SRTM: quitarlas antes de activar `EXPORTAR` |
| 7 (LandTrendr) y 10 (validación) | Por crear | — |

---

## Paso 1. Ámbito y límite provincial

- **Objetivo:** fijar el área de estudio.
- **Entradas:** `data/raw/Provincia/PROVINCIA.gpkg` (INEI).
- **Hacer:**
  1. Filtrar por `ccdd = 08` y `ccpp = 01`.
  2. Verificar que sale un solo polígono válido.
  3. Calcular el área en EPSG:32719.
- **Salida:** geometría de la provincia de Cusco, 530.1 km².
- **Criterio para avanzar:** un registro, geometría válida, área en UTM 19S.
- **Por definir:** nada.

## Paso 2. Fuentes de datos

- **Objetivo:** confirmar fuentes, periodos y roles.
- **Entradas:** catálogos de GEE y archivos locales de GEOBOSQUES.
- **Hacer:**
  1. Verificar rango de fechas y bandas de cada fuente.
  2. Revisar disponibilidad de escenas por año.
  3. Documentar fuentes descartadas y motivos.
- **Salida:** `02_datos_fuentes.md`.
- **Criterio para avanzar:** cada fuente tiene periodo verificado y rol.
- **Por definir:** rol final de Sentinel-2 (revisión visual o comparación). No entra en LandTrendr.

## Paso 3. Preprocesamiento de Landsat

- **Objetivo:** una serie anual de compuestos limpios, uno por año y píxel, comparable entre sensores.
- **Entradas:** colecciones Landsat 8 y 9 C2 L2 sobre la provincia.
- **Hacer:**
  1. Escalar bandas SR con `× 0.0000275 − 0.2`.
  2. Enmascarar con `QA_PIXEL`, bits 0 a 4 (relleno, nube dilatada, cirrus, nube y sombra).
  3. Calcular el compuesto anual como mediana de enero a diciembre. Este valor por año es lo que recibe LandTrendr.
  4. Guardar el conteo de observaciones limpias por píxel y año.
  5. Comparar L8 y L9 en el traslape de 2021 y 2022.
- **Salida:** compuesto anual por año de 2013 a 2025, con conteo de observaciones.
- **Criterio para avanzar:** L8 y L9 coinciden en el traslape; no hay saltos de color que parezcan cambio de cobertura; los años tienen conteo de observaciones suficiente.
- **Por definir:**
  - Mínimo de observaciones limpias por año.
  - Revisión visual de saltos de color (notebook 05).

## Paso 4. Definición de bosque y umbral

- **Objetivo:** fijar una definición de bosque y traducirla a un umbral sobre el índice que usa LandTrendr.
- **Entradas:** definición de GEOBOSQUES (MINAM), índice ajustado (paso 7), píxeles estables de calibración (paso 5).
- **Hacer:**
  1. Tomar los umbrales de GEOBOSQUES (cobertura de copa mínima, altura mínima, área mínima) de su documentación oficial, y citar la fuente exacta.
  2. Calibrar el umbral sobre el índice con los píxeles de calibración: píxeles donde MapBiomas y GEOBOSQUES coinciden como bosque o como no bosque, sin cambio en 2013–2025.
  3. Fijar el umbral y documentarlo.
- **Salida:** definición citada y valor de umbral sobre el índice.
- **Criterio para avanzar:** el umbral separa bosque de no bosque en los píxeles de calibración con exactitud aceptable (valor por definir).
- **Por definir:**
  - Umbrales de GEOBOSQUES. No están verificados. Están en el PDF de 2016 de Cusco o en la ficha técnica del producto.
  - Cómo pasar de cobertura de copa a un valor de índice. El código 3 de MapBiomas no sirve como definición: es etiqueta de un clasificador. En esta provincia tiene 1.8 km².
  - Exactitud mínima de calibración.

## Paso 5. Muestras de calibración y validación

- **Objetivo:** tener datos para calibrar el umbral (paso 4) y para validar (paso 10). No hay entrenamiento.
- **Entradas:** definición de bosque (paso 4), MapBiomas y GEOBOSQUES.
- **Hacer:**
  1. **Calibración:** píxeles estables donde MapBiomas y GEOBOSQUES coinciden, sin cambio en el periodo.
  2. **Validación:** puntos aleatorios y estratificados por clase (bosque, no bosque, cambio), etiquetados por interpretación sobre imágenes y referencias.
  3. Verificar que ningún punto de validación esté en el conjunto de calibración.
- **Salida:** dos conjuntos separados.
- **Criterio para avanzar:** conjuntos sin solapamiento, con suficientes píxeles de bosque por clase. Hay unos 2,000 píxeles de bosque en toda la provincia, lo que limita el tamaño de la muestra.
- **Por definir:**
  - Número de muestras por clase.
  - Criterio de interpretación manual y control de sesgo.

## Paso 6. Índice espectral

- **Objetivo:** elegir el índice que LandTrendr usa para ajustar la serie.
- **Entradas:** compuestos anuales (paso 3).
- **Hacer:**
  1. Comparar NBR, NDVI y EVI sobre imágenes de referencia (notebook 05).
  2. Elegir uno y documentar la razón.
- **Salida:** serie anual del índice elegido por píxel.
- **Criterio para avanzar:** el índice separa visualmente bosque de no bosque y los cambios de pérdida se ven claros.
- **Por definir:** índice. NBR es habitual para pérdida de bosque, pero la elección se confirma con las imágenes.

## Paso 7. LandTrendr

- **Objetivo:** ajustar la trayectoria de cada píxel y detectar sus cambios.
- **Entradas:** serie anual del índice (paso 6).
- **Hacer:**
  1. Ajustar LandTrendr con los parámetros fijados.
  2. Extraer por píxel: segmentos, año de cada quiebre, magnitud, duración y tipo (pérdida o recuperación).
  3. Generar el índice ajustado para cada año de 2013 a 2025.
- **Salida:** capa de segmentos por píxel e índice ajustado por año.
- **Criterio para avanzar:** una muestra de cambios detectados se revisa en imágenes y coincide.
- **Por definir:**
  - Parámetros: máximo de segmentos, umbral de pico, umbral de recuperación y p-valor. Se calibran con los datos de calibración del paso 5.
  - Con 12 años la serie es corta para LandTrendr. Hay que documentarlo como limitación.

## Paso 8. Mapa de bosque por año e indicadores

- **Objetivo:** pasar del índice ajustado a bosque y no bosque por año, y calcular los indicadores.
- **Entradas:** índice ajustado (paso 7), umbral (paso 4).
- **Hacer:**
  1. Aplicar el umbral al índice ajustado de cada año: bosque o no bosque.
  2. **% de bosque** = píxeles de bosque / píxeles totales × 100, por año.
  3. **Pérdida bruta** = píxeles de bosque en t−1 y no bosque en t. Es la cifra principal.
  4. **Pérdida neta** = diferencia de área de bosque entre años. Es referencia.
  5. **Ganancia** = píxeles de no bosque en t−1 y bosque en t.
  6. Control de consistencia: la pérdida por año del mapa debe coincidir con los cambios de LandTrendr que caen en ese año.
- **Salida:** mapas de bosque por año, tabla anual de indicadores, mapa de cambio.
- **Criterio para avanzar:** el control de consistencia cumple. Si no cumple, se revisa el umbral o los parámetros de LandTrendr antes de seguir.
- **Por definir:**
  - Expansión agrícola (ver `01_alcance.md`): no se puede calcular solo con LandTrendr.
  - Expansión de bosque: dentro o fuera del análisis.

## Paso 9. Unidad mínima de mapeo y áreas corregidas

- **Objetivo:** áreas finales con intervalos de confianza.
- **Entradas:** cambios por año (paso 8), matriz de exactitud (paso 10).
- **Hacer:**
  1. Aplicar la unidad mínima de 1 ha a los parches de cambio. Los cambios menores se reportan como "no reportable".
  2. Aplicar el ajuste por exactitud de Olofsson et al. con la matriz del paso 10.
  3. Presentar la pérdida bruta como cifra principal y la neta como referencia.
- **Salida:** tabla de áreas de pérdida y ganancia con intervalos de confianza.
- **Criterio para avanzar:** cada área tiene intervalo de confianza.
- **Por definir:** sensibilidad a 0.5 ha, que menciona el planteamiento original.

## Paso 10. Validación y exactitud

- **Objetivo:** medir la exactitud del mapa de bosque.
- **Entradas:** mapas de bosque por año (paso 8), muestras de validación (paso 5).
- **Hacer:**
  1. Comparar el mapa de cada año de prueba con las muestras de validación.
  2. Calcular matriz de confusión, exactitud global, exactitud del productor y del usuario, por clase.
  3. Validación por bloques espaciales.
  4. Calcular intervalos de confianza.
- **Salida:** reporte de exactitud por clase.
- **Criterio para avanzar:** exactitud por clase con intervalos de confianza.
- **Por definir:**
  - Años de prueba: solo 2025, o también 2024.
  - Tipo de validación: puntual o rodante (calibrar hasta t y probar en t+1).
  - Independencia: las muestras de calibración no se reutilizan en validación.

## Paso 11. Tasas de cambio y degradación

- **Objetivo:** cuantificar la velocidad del cambio y señalar la degradación.
- **Entradas:** áreas corregidas (paso 9), segmentos de LandTrendr (paso 7).
- **Hacer:**
  1. Calcular la tasa de cambio por periodo a partir de las áreas corregidas.
  2. Identificar degradación candidata: segmentos con pendiente negativa en el índice que no llegan al umbral de pérdida.
- **Salida:** tabla de tasas por periodo y mapa de degradación candidata.
- **Criterio para avanzar:** las tasas tienen intervalo de confianza.
- **Por definir:** criterio de pendiente mínima para considerar degradación.

## Paso 12. Comparación con referencias

- **Objetivo:** medir la concordancia con MapBiomas y GEOBOSQUES.
- **Entradas:** mapas de bosque (paso 8), MapBiomas (2013–2021), GEOBOSQUES (2013–2020).
- **Hacer:**
  1. Comparar % de bosque y pérdida bruta con cada referencia en su periodo común.
  2. Calcular concordancia espacial.
  3. Construir la matriz de transición propia contra MapBiomas.
- **Salida:** tabla de comparación por periodo.
- **Criterio para avanzar:** cada comparación usa el periodo común.
- **Por definir:** métricas de concordancia espacial.

## Paso 13. Factores asociados

- **Objetivo:** asociar los cambios con factores del entorno.
- **Entradas:** cambios detectados (paso 8).
- **Hacer:** según la decisión que se tome.
- **Salida:** tabla de factores asociados.
- **Por definir:** variables de reemplazo para pendiente, altitud y distancia a vías (SRTM y OSM salieron del análisis), o eliminar este análisis.

## Paso 14. Extensión preliminar 2026

- **Objetivo:** dar una primera lectura de 2026, fuera del periodo validado.
- **Entradas:** imágenes disponibles de 2026, mismo preprocesamiento del paso 3.
- **Hacer:** si se decide, aplicar el umbral (paso 4) a la composición parcial, sin pasar por LandTrendr.
- **Salida:** lectura preliminar marcada como parcial.
- **Criterio para avanzar:** la advertencia de parcialidad aparece en todo entregable que lo use.
- **Por definir:** si se presenta o se omite.

## Paso 15. Entregables

- **Objetivo:** cumplir `00_proyecto.md`.
- **Hacer:**
  1. Mapas de bosque por año y mapa de cambio (paso 8).
  2. Tabla de áreas de pérdida y ganancia con intervalos (paso 9).
  3. Reporte de exactitud (paso 10).
  4. Zonas críticas (paso 8) y factores asociados (paso 13).
  5. Tasas de cambio por periodo (paso 11).
  6. Visualización de la evolución y página web (pasos 8 y 11).
- **Criterio para avanzar:** cada entregable tiene su fuente en un paso documentado.
- **Por definir:** si el entregable 2 incluye expansión agrícola.
