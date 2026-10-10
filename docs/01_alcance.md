# 01 · Alcance

## Ámbito
- **Espacial:** provincia de Cusco (`ccdd = 08`, `ccpp = 01`), 530.1 km² en UTM 19S (EPSG:32719), según el límite INEI. Quedan fuera las demás provincias y el departamento.
- **Temporal:** 12 periodos anuales, de 2013→2014 a 2024→2025. 2013 es el primer año con Landsat 8 sobre la provincia. Decidido.
- **2026:** año parcial y fuera del periodo validado. Ver sección "Extensión 2026".

## Dos líneas de trabajo

**Línea 1: indicadores de referencia.**
- Lo que publican MapBiomas Colección 4 y GEOBOSQUES (MINAM), leído tal cual.
- Se usa solo para comparar y para calibrar el umbral de bosque (ver metodología, pasos 4 y 5).

**Línea 2: indicadores propios con LandTrendr.**
- Entrada: serie anual de Landsat 8 y 9 por píxel. Solo imágenes satelitales.
- LandTrendr sustituye a la clasificación supervisada con computer vision. Decidido. No se entrena ningún clasificador.
- MapBiomas y GEOBOSQUES no entran al cálculo.

**Cierre común.** Comparación de métricas de ambas líneas, tasas de cambio por periodo y página web con la evolución según la Línea 2.

## Fuentes
Decidido: cuatro fuentes.
- **Landsat 8 y 9** (C2 L2 SR): serie principal de la Línea 2.
- **MapBiomas Colección 4:** referencia principal (Línea 1).
- **GEOBOSQUES (MINAM):** referencia y autoridad para definir bosque.
- **Sentinel-2:** no entra en LandTrendr. Su rol queda como revisión visual o comparación. Por confirmar.

Descartadas: ESA WorldCover (solo 2020 y 2021), SRTM (modelo fijo de 2000) y OpenStreetMap (foto de 2026 sin historial). Los motivos están en `02_datos_fuentes.md`.

## Indicadores
- **Pérdida de bosque:** prioritaria. Decidido.
- **Expansión agrícola:** por definir. LandTrendr detecta cambios de trayectoria, pero no asigna clases de uso. Sin una clase agrícola propia, este indicador no se puede calcular con la Línea 2. Opciones: (a) reportarlo solo como referencia de MapBiomas, (b) sacarlo del alcance, (c) definir una regla adicional con otra fuente.
- **Expansión de bosque:** dentro del alcance. Por confirmar si entra en el análisis.
- **Degradación:** no es indicador separado. Se evalúa al final, a partir de las tasas y de los segmentos de LandTrendr con pendiente negativa que no llegan a pérdida. Decidido.

## Clases
Bosque y no bosque para la Línea 2. Decidido. Las demás clases de MapBiomas solo se usan como referencia. Si se define expansión agrícola con una regla propia, habrá que revisar esta sección.

## Unidad mínima de mapeo
- **1 ha** (unos 11 píxeles de 30 m). Decidido.
- Los cambios menores a la unidad mínima se reportan como "no reportable".
- Sensibilidad a 0.5 ha, que menciona el planteamiento original: por confirmar.

## Resolución de análisis
- **Análisis a 30 m.** Decidido. La serie depende de Landsat, que tiene esa resolución.
- **Sentinel-2:** si se usa como revisión o comparación, se remuestrea a 30 m en la integración. Por confirmar.

## Índice espectral
- **Por definir y urgente.** LandTrendr necesita un único índice para ajustar la serie.
- Candidatos: NBR, NDVI y EVI. NBR es habitual para pérdida de bosque, pero la elección se confirma revisando imágenes en el notebook 05.

## Extensión 2026
- 2026 queda fuera del ajuste de LandTrendr y del periodo validado. Decidido.
- **Por definir:** si se presenta una lectura preliminar (umbral aplicado a la composición parcial de 2026, marcada como parcial) o se omite.
