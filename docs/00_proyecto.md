# Proyecto: Cambio de cobertura del suelo en la provincia de Cusco

## Cliente
Gobierno Regional de Cusco.

## Contexto
La provincia de Cusco combina ceja de selva, valles interandinos y alta montaña. Se busca medir la pérdida de bosque y, si la definición lo permite, la expansión agrícola entre 2013 y 2025 (12 periodos anuales).

## Pregunta principal
¿Cuánta cobertura cambió en la provincia de Cusco entre 2013 y 2025, y con qué exactitud e incertidumbre se estima ese cambio?

## Preguntas secundarias
- ¿Dónde se concentran los cambios (zonas críticas)?
- ¿Qué factores se asocian con los cambios? (variables por definir, ver `01_alcance.md`)
- ¿Qué tan bien coinciden nuestros resultados con MapBiomas y GEOBOSQUES?
- ¿Qué tan rápido ocurren los cambios, y cómo se mueve la tasa a lo largo del periodo?

## Entregables
1. Mapas de bosque por año y mapa de cambio.
2. Tabla de áreas de pérdida y ganancia de bosque, con intervalos de confianza.
3. Reporte de exactitud.
4. Identificación de zonas críticas y factores asociados.
5. Tasas de cambio por periodo.
6. Visualización de la evolución (carrusel o animación) y página web con la evolución según Línea 2.

## Líneas de trabajo
El proyecto tiene dos líneas que producen indicadores comparables. El detalle está en `01_alcance.md`.

**Línea 1: indicadores de referencia.** Lo que publican MapBiomas Colección 4 y GEOBOSQUES (MINAM). Se usan como métricas de comparación.

**Línea 2: indicadores propios con LandTrendr.** Serie anual de Landsat 8 y 9 (2013–2025). LandTrendr ajusta la trayectoria de cada píxel y detecta sus cambios. El bosque se identifica con un umbral sobre el índice ajustado. No se entrena ningún clasificador. MapBiomas y GEOBOSQUES no entran al cálculo: sirven para calibrar el umbral y para comparar.

**Cierre común.** Comparación de métricas de ambas líneas (concordancia espacial y exactitud), tasas de cambio por periodo y página web con la evolución según la Línea 2.

## Clases e indicadores
- **Clases propias:** bosque y no bosque. Las demás clases de MapBiomas (pastos, agrícola, urbano, agua) solo se usan como referencia.
- **Pérdida de bosque** (bosque → no bosque): prioritaria.
- **Expansión agrícola** (no agrícola → agrícola): prioritaria en el planteamiento original, pero por definir (ver `01_alcance.md`).
- **Expansión de bosque** (no bosque → bosque): dentro del alcance; su inclusión en el análisis está por confirmar.
- **Degradación** (bosque que sigue siendo bosque pero pierde vigor): no es un indicador separado. Se evalúa al final, a partir de las tasas y de los segmentos de LandTrendr con pendiente negativa.

## Fuera de alcance
- Cambios que no involucran bosque ni agricultura (por ejemplo, expansión urbana), salvo que se reporten aparte.
- Territorios fuera de la provincia de Cusco, aunque pertenezcan al departamento.
