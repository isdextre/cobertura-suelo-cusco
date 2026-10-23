# 02 · Metodología

**Versión:** 1.0 · **Fecha:** 2026-10-22 · **Cliente:** Gobierno Regional de Cusco
**Reemplaza:** `metodologia_general.md` v0.3 (construida sobre pérdida de bosque, umbral de
GEOBOSQUES y serie Landsat 8 + 9).
**Documentos relacionados:** `00_proyecto.md` (objetivo e indicadores), `01_datos_fuentes.md`
(fuentes y disponibilidad verificada), `03_decisiones.md` (decisiones con respaldo bibliográfico).

---

## Cómo leer esta guía

Cada paso tiene el mismo formato:

- **Objetivo** · qué resuelve
- **Entradas** · lo que necesita
- **Hacer** · acciones, en orden
- **Salida** · lo que deja
- **Criterio para avanzar** · la condición antes del paso siguiente
- **Por definir** · lo que aún no está decidido

Lo marcado **Decidido** no se reabre sin acuerdo explícito. Las decisiones con respaldo
bibliográfico están en `03_decisiones.md` con sus citas.

## Decisiones vigentes

- **Objeto:** degradación de pastizal altoandino (MapBiomas clase 12). Bosque como indicador
  secundario de referencia. Decidido 2026-10-22.
- **Periodo:** 2013–2025, 13 compuestos anuales. Decidido.
- **Serie principal:** Landsat 8 únicamente. Decidido.
- **Referencia temática:** MapBiomas Perú Colección 4. Decidido.
- **Método:** LandTrendr sobre un índice primario, con índices acompañantes en la misma corrida.
  Decidido.
- **Índice primario:** −TCW (Tasseled Cap Wetness invertido). Decidido, con verificación pendiente
  contra puntos interpretados (paso 4).
- **Ventana:** 1 jun – 31 ago. Decidido.
- **Compuesto:** medoide. Decidido.
- **Resolución:** 30 m. Unidad mínima de mapeo: 1 ha. Decidido.
- **Validación:** muestreo estratificado con interpretación visual, no holdout temporal. Decidido.

## Mapa de notebooks

| Paso | Notebook | Estado |
|---|---|---|
| 1 | `01_limite_provincial.ipynb` | Ejecutado |
| 2 | `02_mapbiomas_referencia.ipynb` | Ejecutado (su agrupación de clases pide revisión: ver paso 2) |
| 3 | `03_landsat8_compuestos_anuales.ipynb` | **Ejecutado 2026-10-22.** Es el notebook de referencia de estilo y documentación |
| 4 | `04_landtrendr.ipynb` | Por crear |
| 5 | `05_tipo_de_cambio.ipynb` | Por crear |
| 6 | `06_validacion.ipynb` | Por crear |
| 7 | `07_atribucion_climatica.ipynb` | Por crear |
| 8 | `08_indicadores_entregables.ipynb` | Por crear |

---

## Paso 1 · Ámbito y límite provincial

- **Objetivo:** fijar el área de estudio.
- **Entradas:** `data/raw/Provincia/PROVINCIA.gpkg` (INEI).
- **Hacer:**
  1. Filtrar por `ccdd = 08` y `ccpp = 01`; verificar que devuelve un solo polígono válido.
  2. Simplificar a 0.0001° (≈11 m, menos de medio píxel) para que la geometría no encarezca cada
     consulta a GEE.
  3. Calcular el área en EPSG:32719.
  4. Comprobar si el polígono cruza el meridiano −72°, frontera entre UTM 18S y 19S.
- **Salida:** geometría de la provincia, 530.1 km².
- **Criterio para avanzar:** un registro, geometría válida, área en UTM 19S.
- **Por definir:** nada.

## Paso 2 · Referencia MapBiomas y máscara de pastizal

- **Objetivo:** delimitar la clase objetivo y obtener los indicadores de referencia.
- **Entradas:** asset de MapBiomas Perú C4, límite provincial (paso 1).
- **Hacer:**
  1. Calcular la superficie por clase y año, 2013–2025 (ya hecho; ver `01_datos_fuentes.md` §2.3).
  2. Construir la **máscara de pastizal**: píxeles de clase 12 (formación herbácea). Decidir si se
     usa la máscara de un año base, la unión de todos los años, o los píxeles clase 12 en todo el
     periodo. Cada opción responde a una pregunta distinta y hay que elegir explícitamente.
  3. Separar los **bofedales y cuerpos de agua** como estrato aparte: su dinámica depende de agua y
     nieve, no del pajonal, y CFMask los marca de forma inconsistente.
  4. Extraer la matriz de transiciones de MapBiomas para los periodos del análisis, que es la
     referencia de comparación del paso 8.
  5. Reportar las clases 3 (bosque) y 21 (agropecuario) como contexto, sin convertirlas en
     indicador propio.
- **Salida:** máscara de pastizal, tabla de áreas por clase y año, matriz de transiciones de
  referencia.
- **Criterio para avanzar:** la máscara de pastizal tiene suficientes píxeles para análisis
  estadístico (258 km² ≈ 287 000 píxeles: sobra) y los bofedales están separados.
- **Por definir:**
  - Qué definición de máscara se usa (año base, unión, o estabilidad en todo el periodo).
  - Si la clase 15 (pasto, beta) se integra o se analiza aparte. Es pequeña y MapBiomas la marca
    como preliminar.
  - El notebook heredado agrupa clases con el bosque al centro (`bosque: [3,4,5,6]`). Hay que
    reorientar la agrupación al pastizal cuando se vuelva a ejecutar.

## Paso 3 · Serie anual de Landsat 8 — EJECUTADO

- **Objetivo:** una imagen por año con los índices espectrales, lista para LandTrendr.
- **Entradas:** `LANDSAT/LC08/C02/T1_L2`, límite provincial.
- **Hacer:**
  1. Filtrar la ventana 1 jun – 31 ago y descartar escenas con `CLOUD_COVER_LAND ≥ 65 %`.
  2. Escalar la reflectancia: `SR = DN × 0.0000275 − 0.2`, y recortar al rango físico [0, 1].
     Obligatorio antes de cualquier índice.
  3. Enmascarar: `QA_PIXEL` bits 0–5 (relleno, nube dilatada, cirrus, nube, sombra, nieve),
     confianza de nube ≥ media, confianza alta de sombra y cirrus, `QA_RADSAT ≠ 0`, aerosol alto.
  4. Componer por **medoide**: la observación real más cercana a la mediana multibanda, que
     preserva la coherencia entre bandas de la que dependen las componentes Tasseled Cap.
  5. Calcular 7 índices: `negTCW` (primario), NDVI, MSAVI, TCG, TCB, BSI, NDMI.
  6. Guardar el conteo de observaciones limpias por píxel y año (`n_obs`).
- **Salida:** 13 imágenes anuales de 8 bandas (7 índices + `n_obs`). Tabla de disponibilidad en
  `outputs/landsat_compuestos_anuales/disponibilidad_anual.csv`.
- **Criterio para avanzar:** cumplido. 12 de 13 años en calidad buena, media de 3.76 observaciones
  por píxel y año. Detalle en `01_datos_fuentes.md` §3.
- **Por definir:**
  - Qué se hace con 2025 (2.94 obs/píxel, 63.1 % de la provincia bajo el mínimo). Control acordado:
    correr LandTrendr con y sin 2025 y comparar la estabilidad de los vértices de 2013–2022.

## Paso 4 · LandTrendr

- **Objetivo:** detectar, por píxel, cuándo cambia la trayectoria y con qué magnitud.
- **Entradas:** serie anual de `negTCW` (paso 3) y los 6 índices acompañantes.
- **Hacer:**
  1. **Una sola corrida.** Segmentar con `negTCW` y pasar NDVI, MSAVI, TCG, TCB, BSI y NDMI como
     `ftvList`. Los vértices los define solo el índice primario; los demás se ajustan en esos
     mismos vértices. No correr LandTrendr una vez por índice.
  2. Verificar la orientación del índice: la pérdida de vegetación debe ser un **delta positivo**.
     `negTCW` ya está invertido para eso. Equivocarse aquí invierte degradaciones y recuperaciones.
  3. Calibrar parámetros con una grilla contra puntos interpretados, eligiendo por F1 de detección
     de vértices y concordancia del año (±1), **no por RMSE**. Valores de partida:

     | Parámetro | Valor inicial | Motivo |
     |---|---|---|
     | `maxSegments` | 4 (probar 3–5) | El default 6 permite 7 vértices y sobresegmenta con solo 13 años |
     | `spikeThreshold` | 0.9 (probar 0.85) | |
     | `vertexCountOvershoot` | 3 | Default original |
     | `preventOneYearRecovery` | `True` | En pastizal un rebote de un año es lluvia, no recuperación |
     | `recoveryThreshold` | 0.25 (probar 0.5) | En herbáceas la recuperación real es más rápida que en bosque |
     | `pvalThreshold` | 0.05 | |
     | `bestModelProportion` | 0.75 | |
     | `minObservationsNeeded` | 6 | No bajar: con 13 años quedan pocos grados de libertad |

  4. Correr dos veces, 2013–2024 y 2013–2025, y comparar la estabilidad de los vértices de
     2013–2022 (control del paso 3).
  5. Extraer por píxel: año de quiebre, magnitud, duración, pendiente del segmento, valores
     pre/post de los 7 índices, y el RMSE del ajuste.
- **Salida:** capa de segmentos por píxel con los atributos de arriba, y serie ajustada (FTV) de
  cada índice.
- **Criterio para avanzar:** los vértices de 2013–2022 coinciden entre las dos corridas; una muestra
  de quiebres revisada visualmente corresponde a cambios reales.
- **Por definir:**
  - Verificación del índice primario: correr 3–4 candidatos (−TCW, NDVI, MSAVI, fracción de suelo)
    sobre los puntos de calibración y confirmar −TCW por F1 antes de fijarlo.
  - Número de puntos de calibración (la literatura sugiere 150–300, estratificados por cobertura y
    altitud).

## Paso 5 · Tipo de cambio

- **Objetivo:** decir *qué* fue cada cambio, no solo cuándo ocurrió.
- **Entradas:** segmentos de LandTrendr (paso 4), máscara de pastizal (paso 2).
- **Hacer:**
  1. Para cada segmento de pérdida, leer la dirección simultánea de los índices acompañantes en el
     vértice. Firma esperada de degradación de pastizal:
     `negTCW ↑` · `NDVI ↓` · `MSAVI ↓` · `BSI ↑` · `TCB ↑` · `NDMI ↓`
  2. Exigir **evidencia cruzada**: al menos 4 de 6 índices en la dirección esperada. Un solo índice
     moviéndose es casi siempre ruido o nube mal enmascarada.
  3. Separar por patrón temporal:
     - **degradación gradual**: pérdida de ≥3 años, sostenida, con BSI y TCB en aumento
     - **quema**: pérdida de 1 año con recuperación rápida
     - **conversión agrícola**: patrón geométrico, alta variabilidad interanual, y transición
       confirmada en MapBiomas
     - **expansión urbana**: transición a clase 24 en MapBiomas, con TCB alto y persistente
  4. Formalizar con un random forest sobre los atributos de los segmentos, entrenado con los puntos
     interpretados del paso 6.
- **Salida:** mapa de tipo de cambio por píxel, con nivel de confianza.
- **Criterio para avanzar:** la regla multi-índice y el clasificador coinciden en la mayoría de los
  píxeles; las discrepancias se revisan a mano.
- **Por definir:** umbral exacto de la regla (4 de 6 es el punto de partida) y número de clases del
  clasificador.

## Paso 6 · Validación

- **Objetivo:** medir la exactitud del mapa y estimar el área con incertidumbre.
- **Entradas:** mapa de degradación (pasos 4 y 5).
- **Hacer:**
  1. **Muestreo aleatorio estratificado**, con las clases de cambio del mapa como estratos
     (degradación gradual, pérdida abrupta, ganancia, estable), ≥50–100 puntos por estrato de
     cambio y mayor asignación al estrato estable, que ocupa casi todo el paisaje.
  2. **Interpretación visual ciega al mapa:** para cada punto, revisar la trayectoria Landsat
     2013–2025 más imágenes de alta resolución (Sentinel-2, Google Earth histórico), siguiendo la
     lógica de TimeSync. Registrar ocurrencia, año (±1) y tipo.
  3. **Matriz de error en proporción de área**, exactitud de usuario y de productor por clase, y
     **estimación de área con IC 95 %** según Olofsson et al. (2014). No usar kappa.
  4. Mantener **separación espacial** entre los puntos de calibración del paso 4 y los de validación.
- **Salida:** reporte de exactitud y tabla de superficie degradada con intervalos de confianza.
- **Criterio para avanzar:** cada área reportada tiene su intervalo.
- **Por definir:** número final de puntos por estrato y protocolo de control de sesgo del
  intérprete.

### Lo que NO se hace, y por qué

- **No se valida con holdout temporal.** Retener 2023–2025 para "probar" el modelo no tiene sentido
  metodológico: LandTrendr es una segmentación no supervisada, ajustada independientemente a la
  serie completa de cada píxel. No aprende parámetros en un periodo para aplicarlos a otro, y no
  extrapola. Comparar una "predicción" con los años retenidos mide la persistencia de la última
  pendiente, no la detección de degradación. Además acorta la serie, que ya es corta.
- **El RMSE del ajuste no es validación.** LT-GEE lo entrega como banda y sirve de diagnóstico de
  calidad por píxel, pero solo mide cuánto se pega la polilínea a la serie de entrada. Un modelo
  sobresegmentado baja el RMSE y empeora la detección de cambio real.
- **No se valida contra MapBiomas.** Comparar un mapa con otro mapa mide concordancia, no exactitud.
  La comparación con MapBiomas va en el paso 8, como contraste, no como validación.

## Paso 7 · Atribución climática

- **Objetivo:** separar la degradación antrópica de la respuesta a variabilidad de lluvia.
- **Entradas:** segmentos de pérdida (paso 4), series climáticas.
- **Hacer:**
  1. Reunir precipitación de la estación húmeda previa (oct–abr) y acumulada de dos años, con
     CHIRPS (~5 km) o PISCO de SENAMHI, más temperatura mínima de ERA5-Land.
  2. Para cada píxel con segmento de pérdida, ajustar índice ~ precipitación sobre los años
     estables y evaluar si la pérdida persiste en los residuos (RESTREND).
  3. Clasificar como **degradación probable antrópica** solo las pérdidas con residuo negativo
     significativo; como **respuesta climática** las que coinciden con sequías regionales y se
     recuperan.
- **Salida:** capa de atribución y tabla de superficie degradada separada por causa probable.
- **Criterio para avanzar:** la separación es reproducible y sus limitaciones quedan escritas.
- **Por definir:** CHIRPS o PISCO; si se usa RESTREND simple o TSS-RESTREND.

### Por qué este paso no es opcional

En pastizal semiárido y de altura la variabilidad interanual de lluvia domina el verdor. Mazzarino
y Finn (2016, *Wetlands Ecology and Management*) encontraron en el sur de Perú que el NDVI de
estación seca se correlaciona con la precipitación de la estación húmeda (R² = 0.56). Sin este
control, una sequía se lee como degradación — y en un informe a un gobierno regional esa confusión
tiene consecuencias de política pública.

### Limitaciones que hay que declarar

- Wessels, van den Bergh y Scholes (2012, RSE 125:10–22): con degradación simulada ≥20 %, la
  relación NDVI–lluvia se rompe y RESTREND deja de ser confiable. Además la degradación >20 % solo
  era detectable si no ocurría al inicio o al final del periodo.
- Con 13 años la regresión tiene poca potencia estadística.
- La precipitación a ~5 km frente a píxeles de 30 m limita la atribución local.
- La literatura de RESTREND es sobre todo MODIS/AVHRR en drylands de Australia, África y China, no
  en los Andes.

## Paso 8 · Indicadores finales y entregables

- **Objetivo:** producir los entregables de `00_proyecto.md` §4.
- **Entradas:** salidas de los pasos 4 a 7.
- **Hacer:**
  1. Aplicar la unidad mínima de 1 ha a los parches de degradación; los menores se marcan
     "no reportable".
  2. Excluir los píxeles no interpretables: `n_obs` insuficiente en demasiados años, fuera de la
     máscara de pastizal, bordes entre coberturas, bofedales.
  3. Calcular superficie degradada por periodo con IC 95 %, y tasas de cambio.
  4. Identificar zonas críticas y cruzar con factores asociados.
  5. Comparar contra los indicadores de referencia de MapBiomas, declarando que la comparación es
     un contraste y no una validación.
  6. Reportar el bosque **como referencia de MapBiomas**, con la limitación de `00_proyecto.md` §2
     escrita en el mismo lugar donde aparece la cifra.
  7. Construir la visualización de la evolución 2013–2025.
- **Salida:** los 7 entregables.
- **Criterio para avanzar:** cada entregable tiene su fuente en un paso documentado.
- **Por definir:** formato final de la visualización.

---

## Limitaciones generales del diseño

Van en todo entregable, no solo aquí.

- **13 años es una serie corta para LandTrendr**, diseñado para 25–35 años. Limita el número de
  segmentos detectables, la potencia de RESTREND y la confirmación de los cambios recientes.
- **No existe literatura revisada por pares que aplique LandTrendr a degradación de pastizal en
  puna, altiplano o páramo.** Las decisiones de este diseño extrapolan desde estepas de Asia
  Central, drylands mediterráneos y rangelands de EE. UU. Es una limitación y a la vez una
  oportunidad de aporte original.
- **El efecto de las heladas de época seca sobre el verdor Landsat en puna no está cuantificado en
  la literatura.** Las mitigaciones adoptadas (ventana estrecha y fija, medoide, índice menos
  dependiente de la clorofila, covariable de temperatura mínima) son razonadas, no validadas.
- **MapBiomas no es verdad de campo.** Es un Random Forest entrenado con pocas muestras estables en
  la región Andes.
- **2025 es el año más débil de la serie y además el terminal.** Ver paso 3.
