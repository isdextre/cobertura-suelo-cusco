# 02 · Datos y fuentes

**Actualizado:** 2026-10-10
**Base de verificación:** notebooks 01 a 04 ejecutados (salidas guardadas). Notebooks 05 y 06 sin ejecutar.

## 1. Ámbito

- **Área de estudio:** provincia de Cusco (`ccdd = 08`, `ccpp = 01`), del límite INEI (`data/raw/Provincia/PROVINCIA.gpkg`, capa `PROVINCIA`, EPSG:4326).
- **Área:** 530.1 km² calculada en UTM 19S (EPSG:32719), que es el método de referencia. El notebook 04 da 531.2 km² calculando el área en GEE. Los documentos usan 530.1 km².
- **Columna `fuente` del límite:** "V Censo Nacional Económico". Se documenta tal cual; el origen INEI sigue por confirmar.

## 2. Fuentes incluidas

Las fechas de Landsat, Sentinel-2 y MapBiomas vienen de consultas a Google Earth Engine (notebook 02). Las de GEOBOSQUES vienen de su servicio WMS y de las imágenes locales (notebooks 02 y 03).

| Fuente | Producto | Periodo verificado | Resolución | Indicadores | Rol |
|---|---|---|---|---|---|
| Landsat 8 C2 L2 | Reflectancia superficial (SR) | 2013-03-26 a 2026-09-19 | 30 m | Serie anual del índice para LandTrendr | **Serie principal (Línea 2)** |
| Landsat 9 C2 L2 | Reflectancia superficial (SR) | 2021-11-05 a 2026-09-27 | 30 m | Igual que L8 | **Serie principal (Línea 2)**, desde 2021 |
| Sentinel-2 SR Harmonized | Reflectancia superficial (SR) | 2016-04-30 a 2026-10-07 (denso desde 2019) | 10 m (B2, B3, B4, B8); 20 m (B11, B12) | Revisión visual | **Revisión o comparación**, por confirmar. No entra en LandTrendr |
| MapBiomas Perú Colección 4 | Cobertura y uso del suelo | 1985 a 2025, una banda por año | 30 m | Clases de referencia; pérdida de bosque, expansión agrícola y otras transiciones | **Referencia principal (Línea 1)** |
| GEOBOSQUES (MINAM) | Bosque y pérdida de bosque | Capas WMS: "No bosque al 2000", "Pérdida 2001 - 2024", "Bosque al 2025", "Pérdida natural 2025", "Pérdida antrópica (Deforestación) 2025" | Según WMS | Pérdida de bosque, deforestación anual y acumulada, bosque remanente 2025 | **Referencia (Línea 1)** y **autoridad para definir bosque** |

### 2.1 Disponibilidad de escenas (notebook 03)

**Landsat 8 (serie principal):** escenas sobre la provincia por año.

| Año | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 |
|---|---|---|---|---|---|---|---|---|---|---|
| Escenas | 19 | 36 | 42 | 41 | 45 | 39 | 36 | 41 | 40 | 43 |

- **Landsat 9:** 5 escenas en 2021 y 46 en 2022. Desde 2023 la tabla del notebook 03 no se revisó completa.
- **Landsat 5 y 7 (fuera de la serie decidida):** L5 tiene escenas de 1984 a 2011 (solo 2010 y 2011 caen en la ventana original). L7 tiene escenas de 1999 a 2023 y cubre 2010 a 2022 en la ventana original.
- **Sentinel-2:** 11 escenas en 2016, 18 en 2017, 29 en 2018, y entre 284 y 295 por año de 2019 a 2024. En 2025 hay 412.
- **MapBiomas:** tiene banda para todos los años de 2010 a 2025.
- **GEOBOSQUES (imágenes locales):** hay PNG de 2016 a 2025, con 2021 faltante. Las **9 imágenes tienen el mismo MD5** (`ac33384d5a7810e958d0db6d47875efa`) y el mismo tamaño (10,301 bytes). Por lo tanto, **los PNG locales no sirven como serie anual**. Hay que descargar cada año desde el servicio WMS.

### 2.2 Notas por fuente

- **Landsat:** Collection 2 Level 2 (SR). La máscara de calidad usa `QA_PIXEL` con los bits 0 a 4 (relleno, nube dilatada, cirrus, nube y sombra). La escala es `reflectancia × 0.0000275 − 0.2`.
- **Sentinel-2:** la banda 1 de la colección tiene 60 m. Por eso la escala 60 m que aparece en el notebook 02 no es la resolución de análisis. Las bandas usadas serían B2, B3, B4 y B8 a 10 m, y B11 y B12 a 20 m. La máscara usa la capa SCL.
- **MapBiomas:** el asset es `projects/mapbiomas-public/assets/peru/collection4/mapbiomas_peru_collection4_coverage_v1`. El rango 1985–2025 viene de GEE. El valor 1985–2021 de la tabla de referencia previa estaba desactualizado.
- **GEOBOSQUES:** el producto `bosque_humedo_2025` (WMS) tiene capas de 2000 a 2025. El periodo de pérdida es **2001–2024**, no 2001–2020 como decía la tabla previa. Se usa como referencia en 2013–2020 para comparación, y para pérdida con el periodo 2013–2024 cuando haga falta.

## 3. Fuentes descartadas

| Fuente | Motivo |
|---|---|
| ESA WorldCover (2020 y 2021) | Solo tiene dos años. No permite construir una serie. |
| SRTM (`USGS/SRTMGL1_003`) | Es un modelo fijo (año 2000). Sale del análisis. |
| OpenStreetMap (red vial) | Es una foto de 2026-10-08 sin historial. No hay imágenes para calcular métricas. |

**Consecuencia:** el análisis de factores asociados (pendiente, altitud, distancia a vías) pierde sus variables. Por definir.

## 4. Decisiones de fuentes vigentes

- Serie principal: **Landsat 8 y 9, de 2013 a 2025** (12 periodos anuales). Landsat 5 y 7 quedan fuera.
- Método principal: **LandTrendr** sobre la serie Landsat. Sustituye a la clasificación supervisada. No se entrena clasificador.
- Unidad mínima de mapeo: **1 ha** (unos 11 píxeles de 30 m).
- Análisis a **30 m**.
- Bosque: definición de **GEOBOSQUES (MINAM)**. Los umbrales se confirman en el paso 4 de la metodología.
- Se usan solo las cuatro fuentes de esta sección.

## 5. Pendientes relacionados

- Umbrales de GEOBOSQUES para bosque (cobertura de copa, altura, área mínima).
- Índice espectral que alimenta LandTrendr (NBR, NDVI o EVI).
- Parámetros de LandTrendr.
- Rol final de Sentinel-2 (revisión o comparación).
- Descarga de GEOBOSQUES por año, porque los PNG locales están repetidos.
- Variables de factores asociados, ya que SRTM y OSM salieron del análisis.
