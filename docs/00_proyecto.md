# Proyecto: Cambio de cobertura del suelo en la provincia de Cusco

## Cliente
Gobierno Regional de Cusco.

## Contexto
La provincia de Cusco combina ceja de selva, valles interandinos y alta montaña. Se busca medir la pérdida de bosque y la expansión agrícola durante 15 años. La expansión de bosque también entra en el alcance, pero se incorpora cuando se defina la clase "bosque" (ver `01_alcance.md`).

## Pregunta principal
¿Cuánta cobertura cambió en la provincia de Cusco en 15 años, y con qué exactitud e incertidumbre se estima esa área?

## Preguntas secundarias
- ¿Dónde se concentran los cambios (zonas críticas)?
- ¿Qué factores (pendiente, altitud, distancia a vías) se asocian con los cambios?
- ¿Qué tan bien coinciden nuestros resultados con MapBiomas, ESA WorldCover y GEOBOSQUES?
- ¿Qué tan rápido ocurren los cambios, y cómo se mueve la tasa a lo largo de los 15 años?

## Entregables
1. Mapas de cobertura por año y mapa de cambio.
2. Tabla de áreas por clase y transición, con intervalos de confianza.
3. Reporte de exactitud.
4. Identificación de zonas críticas y factores asociados.
5. Tasas de cambio por periodo.
6. Visualización de la evolución en 15 años (carrusel o animación).

## Líneas de trabajo

El proyecto tiene dos líneas que producen los mismos indicadores, para poder compararlos. El detalle está en `01_alcance.md`.

**Línea 1: indicadores de referencia y serie de 15 años.**
- Serie 2010–2025 construida con las fuentes disponibles: Landsat (serie principal), MapBiomas (referencia principal), Sentinel-2 (complemento desde 2019), WorldCover, GEOBOSQUES, SRTM y OpenStreetMap.
- Los indicadores que publican los productos existentes se usan como métricas de referencia.

**Línea 2: indicadores propios con computer vision.**
- Modelo entrenado con muestras etiquetadas por nosotros.
- Entrada: solo imágenes satelitales. MapBiomas y WorldCover no entran al modelo, solo sirven para comparar.
- Calcula los mismos indicadores de la línea 1.

**Cierre común.**
- Comparación de métricas de ambas líneas: matriz de confusión, exactitud global, exactitud del productor y del usuario, e intervalos de confianza.
- Tasas de cambio por periodo.
- Página web con la evolución según nuestro modelo.

## Clases de cobertura
Bosque, pastos, agrícola, urbano, agua y otras. La correspondencia con MapBiomas y la definición de bosque están pendientes (ver `01_alcance.md`).

## Indicadores y transiciones de interés
- **Pérdida de bosque** (bosque → no bosque) y **expansión agrícola** (no agrícola → agrícola): prioritarios.
- **Expansión de bosque** (no bosque → bosque): dentro del alcance, pero su inclusión en el análisis queda pendiente de confirmar.
- **Degradación** (bosque que sigue siendo bosque pero pierde densidad): no es un indicador separado. Se evalúa al final, a partir de las tasas de cambio.
- Cualquier otra transición se registra en `tabla_transiciones.csv`.

## Fuera de alcance
- Cambios que no involucran bosque, pastos ni agricultura (por ejemplo, expansión urbana), salvo que aparezcan en la tabla de transiciones como reporte aparte.
- Territorios fuera de la provincia de Cusco, aunque pertenezcan al departamento.
