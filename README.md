# Degradación de pastizal altoandino en la provincia de Cusco (2013–2025)

Análisis geoespacial de cambio de cobertura del suelo para el **Gobierno Regional de Cusco**.
Detecta la degradación gradual de pastizal altoandino aplicando **LandTrendr** a una serie anual de
**Landsat 8**, con **MapBiomas Perú Colección 4** como referencia temática.

- **Área:** provincia de Cusco, 530.1 km² (límite INEI)
- **Periodo:** 2013–2025, 13 compuestos anuales de estación seca
- **Resolución:** 30 m · **Unidad mínima de mapeo:** 1 ha
- **Plataforma:** Google Earth Engine (proyecto `viirs-peru`)

## El problema

La formación herbácea ocupa el **48.6 %** de la provincia y MapBiomas la reporta **estable**
(258.3 → 260.5 km² en 13 años). Pero MapBiomas asigna una clase por año: informa si el píxel
*sigue siendo* pastizal, no en qué *condición* está. Un pajonal que pierde densidad y expone suelo
se sigue clasificando igual hasta cruzar a otra clase.

Este trabajo detecta esa degradación intraclase, que un clasificador anual no puede ver, leyendo la
trayectoria temporal de cada píxel con un índice sensible a humedad y suelo expuesto.

> El planteamiento original de este proyecto medía **pérdida de bosque**. Se cambió el 2026-10-22
> porque el bosque ocupa el 0.38 % de la provincia (2.0 km²) y su cambio anual está en el orden de
> decenas de píxeles, lo que no soporta una estimación de área con intervalos de confianza. El
> bosque pasó a indicador secundario de referencia. Detalle en `docs/00_proyecto.md` §2 y §6.

## Documentación

Leer en este orden:

| Documento | Contenido |
|---|---|
| [`docs/00_proyecto.md`](docs/00_proyecto.md) | Objetivo, indicadores, entregables y alcance |
| [`docs/01_datos_fuentes.md`](docs/01_datos_fuentes.md) | Fuentes vigentes y descartadas, disponibilidad real de la serie |
| [`docs/02_metodologia.md`](docs/02_metodologia.md) | Los 8 pasos del flujo, con entradas, salidas y criterios |
| [`docs/03_decisiones.md`](docs/03_decisiones.md) | Cada decisión de diseño con su respaldo bibliográfico |
| [`notebooks/README.md`](notebooks/README.md) | Mapa de notebooks y orden de ejecución |

## Método, en resumen

1. **Serie anual.** Compuesto **medoide** de las escenas de Landsat 8 de **1 jun – 31 ago**
   (estación seca plena), con escalado de reflectancia y máscara de calidad estricta.
2. **Siete índices.** `negTCW` como primario, más NDVI, MSAVI, TCG, TCB, BSI y NDMI.
3. **LandTrendr**, una sola corrida: segmenta con `negTCW` y ajusta los otros seis en los mismos
   vértices.
4. **Caracterización** del tipo de cambio por evidencia cruzada entre índices.
5. **Validación** con muestreo estratificado e interpretación visual, con estimación de área e
   intervalos de confianza.
6. **Atribución climática** con RESTREND, para separar degradación antrópica de respuesta a sequía.

Las tres decisiones menos obvias, y por qué:

- **Solo Landsat 8.** Añadir Landsat 9 (que empieza en 2021) duplicaría las observaciones solo en
  los últimos años, mejorando la calidad del compuesto por razones de muestreo y no de terreno. Ese
  escalón a mitad de serie es indistinguible de un disturbio para un segmentador.
- **−TCW en vez de NDVI.** En pajonal senescente de época seca no hay clorofila activa, así que el
  NDVI no separa vegetación seca de suelo desnudo. TCW mide contenido de agua y funciona esté verde
  o seco. Va invertido porque LT-GEE exige que la pérdida sea un delta positivo.
- **Medoide en vez de mediana.** La mediana por banda puede combinar bandas de fechas distintas y
  crear un píxel que nunca existió, lo que rompe las relaciones entre bandas de las que dependen las
  componentes Tasseled Cap.

## Estado

| Paso | Notebook | Estado |
|---|---|---|
| 1 · Límite provincial | `01_limite_provincial.ipynb` | Ejecutado |
| 2 · Referencia MapBiomas | `02_mapbiomas_referencia.ipynb` | Ejecutado, pide revisión |
| 3 · Serie anual Landsat 8 | `03_landsat8_compuestos_anuales.ipynb` | **Ejecutado 2026-10-22** |
| 4 · LandTrendr | `04_landtrendr.ipynb` | Por crear |
| 5 · Tipo de cambio | `05_tipo_de_cambio.ipynb` | Por crear |
| 6 · Validación | `06_validacion.ipynb` | Por crear |
| 7 · Atribución climática | `07_atribucion_climatica.ipynb` | Por crear |
| 8 · Indicadores y entregables | `08_indicadores_entregables.ipynb` | Por crear |

**Resultado del paso 3:** 12 de 13 años en calidad buena, con una media de 3.76 observaciones
limpias por píxel y año. 2025 queda en calidad baja (2.94 obs/píxel, 63.1 % de la provincia bajo el
mínimo) y además es el año terminal, así que el paso 4 se corre con y sin 2025 para verificar que
los vértices no se muevan. Tabla completa en `outputs/landsat_compuestos_anuales/`.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
python -m pip install -r requirements.txt
```

Earth Engine necesita autenticación una vez:

```python
import ee
ee.Authenticate()
ee.Initialize(project="viirs-peru")
```

## Estructura

```
data/raw/Provincia/PROVINCIA.gpkg     límite provincial del INEI (no versionado)
docs/                                 documentación del proyecto
notebooks/                            flujo de análisis, en orden
outputs/                              resultados: compuestos, tablas, mapas
src/                                  módulos reutilizables (sin usar todavía)
reorganizar_notebooks.py              utilidad de mantenimiento del repo
```

## Limitaciones

Van declaradas en todo entregable:

- **13 años es una serie corta** para LandTrendr, diseñado para 25–35 años.
- **No existe literatura revisada por pares** que aplique LandTrendr a degradación de pastizal en
  puna, altiplano o páramo. El diseño extrapola desde estepas de Asia Central, drylands
  mediterráneos y rangelands de EE. UU. Es limitación y oportunidad de aporte original.
- **El efecto de las heladas de época seca** sobre el verdor Landsat en puna no está cuantificado en
  la literatura; las mitigaciones adoptadas son razonadas, no validadas.
- **MapBiomas no es verdad de campo**, sino un Random Forest entrenado con pocas muestras estables
  en la región Andes. Se usa como referencia, nunca como validación.
