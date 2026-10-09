# Proyecto: Cambio de cobertura del suelo en la provincia de Cusco

## Cliente
Gobierno Regional de Cusco.

## Contexto
La provincia de Cusco combina ceja de selva, valles interandinos y alta montaña. Se busca medir la pérdida de bosque, la regeneración y la expansión agrícola durante 15 años.

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

## Trabajos del proyecto

El proyecto tiene dos trabajos que producen los mismos indicadores, para poder compararlos.

**Trabajo 1: indicadores propios con reglas (método clásico).**
- Se calculan índices a partir de las bandas satelitales (NDVI, EVI, NBR).
- Se definen umbrales propios que asignan cada píxel a una clase (bosque, pasto, agrícola, urbano, agua).
- Se comparan los mapas de años distintos para detectar pérdida, regeneración y expansión agrícola.
- Entrada: índices y bandas. Salida: mapas y áreas por año.

**Trabajo 2: modelo de computer vision propio (aprendizaje automático).**
- Se entrena un modelo (por ejemplo, una red convolucional) con muestras etiquetadas por nosotros.
- El modelo aprende a clasificar cada píxel directamente a partir de las imágenes satelitales.
- Entrada: solo imágenes satelitales (no MapBiomas ni WorldCover, para que la comparación no quede sesgada). Salida: mapas y áreas por año.

**Comparación entre trabajos.**
- Ambos se evalúan con las mismas métricas (matriz de confusión, exactitud global, exactitud del productor y del usuario, intervalos de confianza).
- Ambos se validan con los mismos datos de verificación independientes.
- Ambos se comparan contra MapBiomas, ESA WorldCover y GEOBOSQUES.

## Clases de cobertura
Bosque, pastos, agrícola, urbano, agua y otras (se definen en `01_alcance.md`).

## Transiciones de interés
- Bosque → agrícola o pastos (pérdida de bosque y expansión agrícola).
- Pastos o agrícola → bosque (regeneración).
- Degradación (bosque que sigue siendo bosque pero pierde densidad) se analiza dentro del alcance, usando un indicador adicional.
- Cualquier otra transición se registra en `tabla_transiciones.csv`.

## Fuera de alcance
- Cambios que no involucran bosque, pastos ni agricultura (por ejemplo, expansión urbana), salvo que aparezcan en la tabla de transiciones como reporte aparte.
- Territorios fuera de la provincia de Cusco, aunque pertenezcan al departamento.