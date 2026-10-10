# 01 · Alcance

## Ámbito
- **Espacial:** provincia de Cusco (`ccdd=08`, `ccpp=01`), unos 530 km², en UTM 19S (EPSG:32719). Quedan fuera las demás provincias y el departamento.
- **Temporal:** 15 periodos anuales, de 2010 a 2025 (2010→2011, …, 2024→2025). 2026 es año parcial: solo se usa para inventario y no entra en el análisis.

## Dos líneas de trabajo

**Línea 1: indicadores de referencia y serie de 15 años**
- Usar todas las fuentes disponibles para construir la serie 2010–2025, delimitada a la provincia de Cusco.
- Leer los indicadores que publican los productos existentes (MapBiomas, GEOBOSQUES, WorldCover) y usarlos como métricas de referencia.

**Línea 2: indicadores propios con computer vision**
- Entrenar un modelo con imágenes satelitales y muestras etiquetadas por nosotros.
- El modelo usa solo imágenes satelitales como entrada. MapBiomas y WorldCover no entran al modelo, solo sirven para comparar.
- Calcular con el modelo los mismos indicadores de la línea 1.

**Cierre común**
- Comparar las métricas de ambas líneas.
- Calcular tasas de cambio por periodo.
- Publicar todo en una página web que muestre la evolución según nuestro modelo.

## Indicadores
- **Pérdida de bosque:** prioritario.
- **Expansión agrícola:** prioritario.
- **Expansión de bosque:** dentro del alcance. La definición de la clase "bosque" queda pendiente hasta revisar la data.
- **Degradación:** no es un indicador separado en esta etapa. Se evalúa al final, a partir de las tasas de cambio.
- **Otras transiciones:** se registran en `tabla_transiciones.csv`.

## Clases de cobertura
Bosque, pastos, agrícola, urbano, agua y otras. Pendiente: definir qué clases de MapBiomas corresponden a cada una, y la definición de bosque, después de revisar la data.

## Unidad mínima de mapeo
- **Propuesta:** 1 ha (unos 11 píxeles de 30 m).
- Sensibilidad a 0.5 ha: se evalúa en la etapa de exactitud. Si la exactitud se sostiene, se usa 0.5 ha.
- Los cambios menores a la unidad mínima se reportan como "no reportable".

## Resolución de análisis
- **30 m.** La serie 2010–2018 depende de Landsat, que tiene esa resolución. Sentinel-2 (10 m) se usa desde 2019 y se remuestrea a 30 m para que la serie sea consistente.

## Referencias
- **MapBiomas Perú Colección 4** (1985–2025, 30 m): comparación principal.
- **GEOBOSQUES 2025** (MINAM): comparación solo en la zona que cubre su producto. Pendiente conseguir valores por píxel (descarga o WCS).
- **ESA WorldCover 2020 y 2021**: comparación puntual. La diferencia de suelo desnudo entre ambas versiones debe revisarse antes de usarlas.

## Fuera de alcance
- Expansión urbana y otros cambios que no involucren bosque, pastos ni agricultura, salvo que aparezcan en la tabla de transiciones.
- La red vial de OSM como variable temporal. Es una foto de 2026 sin historial, así que solo serviría como variable fija (distancia a vías).
- Territorios fuera de la provincia de Cusco.

## Índices y bandas
- Se eligen después de revisar las imágenes y su información: bandas disponibles en cada satélite, consistencia entre Landsat y Sentinel-2, y calidad de nubes.
- No se fija ningún índice (NDVI, EVI, NBR) en esta etapa.
- El método de reglas con umbrales (si se mantiene) depende de esa elección.

## Pendiente
- Revisar las imágenes y su información antes de elegir índices o bandas.
- Decidir si el método de reglas se mantiene, después de elegir el índice.
- Definición de bosque, después de revisar la data.
- Mapeo de clases de MapBiomas a las clases del proyecto.
- Confirmar que hay escenas disponibles para 2010 (el inventario actual empieza en 2011).
