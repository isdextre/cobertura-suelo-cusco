# 01 · Datos y fuentes

**Versión:** 1.0 · **Fecha:** 2026-10-22
**Reemplaza:** `02_datos_fuentes.md` v0.x (asumía Landsat 8 + 9, Sentinel-2 y GEOBOSQUES).
**Base de verificación:** notebooks 01, 02 y 03 ejecutados.

---

## 1. Ámbito

- **Área de estudio:** provincia de Cusco (`ccdd = 08`, `ccpp = 01`) del límite INEI
  (`data/raw/Provincia/PROVINCIA.gpkg`, capa `PROVINCIA`, EPSG:4326).
- **Área:** 530.1 km² calculada en EPSG:32719, que es el valor de referencia. El cálculo en GEE
  da 531.2 km²; la diferencia de 0.2 % viene de la simplificación de geometría y de la proyección.
- **Columna `fuente` del archivo:** "V Censo Nacional Económico". Se documenta tal cual; el origen
  INEI sigue sin confirmar formalmente.

---

## 2. Fuentes vigentes

Solo dos. Cada una tiene un rol que la otra no puede cumplir.

| Fuente | Producto | Periodo | Resolución | Rol |
|---|---|---|---|---|
| **Landsat 8 C2 L2** (`LANDSAT/LC08/C02/T1_L2`) | Reflectancia de superficie | 2013-03-26 → presente | 30 m | **Serie temporal principal.** Alimenta LandTrendr: dice *cuándo* cambió cada píxel |
| **MapBiomas Perú C4** (`projects/mapbiomas-public/assets/peru/collection4/mapbiomas_peru_collection4_coverage_v1`) | Cobertura y uso del suelo, una banda por año | 1985 → 2025 | 30 m | **Referencia temática.** Define la máscara de pastizal (clase 12) y aporta los indicadores de comparación |

### 2.1 Por qué solo Landsat 8

LandTrendr lee la *forma* de la trayectoria temporal de cada píxel, lo que lo hace sensible a
cualquier cambio en el régimen de muestreo que ocurra a mitad de la serie.

**Landsat 9 queda fuera** aunque sea técnicamente compatible (OLI-2 es un gemelo de OLI y se mezcla
sin transformación). El problema es *cuándo empieza*: con escenas sobre la provincia desde noviembre
de 2021, añadirlo duplicaría las observaciones solo en los últimos cuatro años. El compuesto medoide
de 2024 se elegiría entre el doble de candidatos que el de 2015, así que su calidad mejoraría
sistemáticamente a partir de 2022 por razones de muestreo y no de terreno. Para un segmentador, ese
escalón en 2021–2022 es indistinguible de un disturbio real.

**Landsat 7 queda fuera** porque ETM+ no mide igual que OLI: Roy et al. (2016, RSE 185:57–70)
documentaron que el NDVI de OLI es sistemáticamente mayor sobre superficies vegetadas y publicaron
coeficientes de armonización. A eso se suma el bandeado SLC-off (le falta ~22 % de cada escena desde
2003) y la deriva orbital de sus últimos años, que cambia la hora de paso.

**Sentinel-2 queda fuera de la serie** por el mismo problema de densidad no estacionaria, agravado:
empieza en 2015 y recién es denso desde 2019. Se reserva para **validación visual**, donde su
resolución de 10 m ayuda a interpretar un píxel a ojo.

### 2.2 Qué aporta MapBiomas y qué no

**Aporta:** la máscara de la clase objetivo (formación herbácea, clase 12), la composición de la
provincia por año, y los indicadores de referencia contra los que se compara el resultado propio.
Cubre todo el periodo, está a la misma resolución que Landsat (se cruza píxel a píxel sin
remuestreo) y es un asset abierto de GEE, lo que mantiene el flujo reproducible.

**No aporta:** verdad de campo. Es una clasificación Random Forest que en la región Andes se
entrenó con pocas muestras estables por clase. Y por construcción no puede ver degradación
intraclase: asigna una clase por año, así que un pajonal que pierde densidad sigue siendo
"formación herbácea" hasta cruzar a otra clase. Esa es justamente la brecha que llena este trabajo.

**No se usa para validar.** La validación va con muestreo estratificado e interpretación visual
(paso 6 de la metodología), no contra MapBiomas, porque validar un mapa contra otro mapa mide
concordancia, no exactitud.

### 2.3 Composición de la provincia (MapBiomas C4, notebook 02)

Superficie en km² por clase. Confirma el cambio de enfoque documentado en `00_proyecto.md` §2.

| Clase | 2013 | 2019 | 2025 | Tendencia |
|---|---|---|---|---|
| 12 · Formación herbácea | 258.3 | 260.2 | 260.5 | estable |
| 21 · Mosaico agropecuario | 148.4 | 145.3 | ~143 | en descenso |
| 24 · Infraestructura urbana | 28.3 | 32.1 | >33.7 | en aumento |
| 9 · Plantación forestal | 9.9 | 9.3 | 8.9 | en leve descenso |
| 3 · Bosque | 2.01 | 1.86 | 1.82 | estable, muy pequeño |
| 15 · Pasto (beta) | 1.7 | 2.7 | 3.6 | ruidoso, clase beta |

Pérdida de bosque según MapBiomas: 0.02 a 0.11 km²/año. Expansión agrícola: 0.20 a 0.93 km²/año.

---

## 3. Disponibilidad real de la serie Landsat 8

Medida en el notebook 03 sobre la ventana vigente (1 jun – 31 ago), con la máscara de calidad
completa aplicada. `obs/píxel` es la media de observaciones limpias por píxel sobre la provincia.

| Año | Escenas en ventana | Útiles (<65 % nubes) | obs/píxel media | p10 | % prov. con ≥3 obs | Calidad |
|---|---|---|---|---|---|---|
| 2013 | 8 | 8 | 3.21 | 2.0 | 85.2 | buena |
| 2014 | 8 | 8 | 3.21 | 3.0 | 90.4 | buena |
| 2015 | 12 | 11 | 3.56 | 3.0 | 92.3 | buena |
| 2016 | 10 | 9 | 3.18 | 3.0 | 90.1 | buena |
| 2017 | 12 | 11 | 4.27 | 3.0 | 97.5 | buena |
| 2018 | 12 | 11 | 3.07 | 2.0 | 71.0 | buena (la más débil) |
| 2019 | 12 | 11 | 4.73 | 4.0 | 97.7 | buena |
| 2020 | 10 | 10 | 4.11 | 3.0 | 98.5 | buena |
| 2021 | 12 | 12 | 3.59 | 3.0 | 92.2 | buena |
| 2022 | 11 | 10 | 3.24 | 3.0 | 97.5 | buena |
| 2023 | 12 | 12 | 5.14 | 4.0 | 98.8 | buena |
| 2024 | 12 | 11 | 4.60 | 3.0 | 96.9 | buena |
| **2025** | 12 | 11 | **2.94** | **2.0** | **63.1** | **baja** |

Media del periodo: 3.76 observaciones por píxel y año.

### Lo que hay que tener en cuenta

- **12 de 13 años en calidad buena**, por encima de los 6 años válidos que exige
  `minObservationsNeeded` de LandTrendr.
- **2025 es el año débil y además es el terminal.** Con 2.94 observaciones de media y solo el
  63.1 % de la provincia alcanzando el mínimo, el medoide de 2025 se apoya a menudo en una sola
  escena. Al ser el extremo de la serie tiene palanca sobre la pendiente del último segmento, así
  que puede generar una falsa señal de degradación reciente. **Control acordado:** correr LandTrendr
  dos veces, 2013–2024 y 2013–2025, y verificar que los vértices de 2013–2022 no se muevan. Si
  coinciden, 2025 se conserva; si no, la serie cierra en 2024.
- **2018 es la más débil de las "buenas"**: solo el 71 % de la provincia llega a 3 observaciones.
  Tratarla con la misma cautela al interpretar quiebres en ese año.
- **`obs_min = 0` en todos los años.** Siempre hay píxeles sin ninguna observación limpia, por
  nubosidad persistente. Es esperable en montaña y por eso la banda `n_obs` se arrastra hasta el
  análisis final: esos píxeles no son interpretables y deben excluirse, no rellenarse.
- **2013 y 2014 tienen 8 escenas** frente a 10–12 en los años siguientes. Consistente con la entrada
  en operación de Landsat 8, pero la media de observaciones (3.21) sigue sobre el umbral.

---

## 4. Fuentes descartadas

| Fuente | Motivo |
|---|---|
| Landsat 9 | Densidad no estacionaria: solo cubre 2021→, crea un escalón de muestreo a mitad de la serie (§2.1) |
| Landsat 7 | Calibración distinta a OLI, bandeado SLC-off, deriva orbital (§2.1) |
| Sentinel-2 | Empieza en 2015, denso desde 2019. Mismo problema de densidad. Se reserva para validación visual |
| GEOBOSQUES (MINAM) | Era la autoridad para definir bosque. Con el bosque como indicador secundario pierde su función. Además los 9 PNG locales comparten el mismo MD5 (`ac33384d…`), así que no sirven como serie anual |
| ESA WorldCover | Solo 2020 y 2021. No permite construir serie |
| SRTM | Modelo fijo del año 2000. No es serie temporal |
| OpenStreetMap | Foto de 2026-10-08 sin historial consistente |

### Consecuencia sobre los factores asociados

Con SRTM y OSM fuera, el análisis de factores pierde altitud, pendiente y distancia a vías. Dos
opciones, a decidir en el paso 7:

1. **Reincorporar SRTM y OSM como covariables fijas**, no como series. Para explicar *dónde* se
   concentra la degradación, una variable fija es perfectamente válida: la altitud de 2000 sigue
   siendo la altitud. La razón original para descartarlas (no miden cambio) no aplica a un análisis
   de patrón espacial.
2. **Sustituirlos** por las covariables climáticas del paso 7 (precipitación CHIRPS o PISCO,
   temperatura mínima ERA5-Land), que sí son series y además son las que la literatura exige para
   separar degradación antrópica de respuesta a sequía.

Recomendación: las dos. Son complementarias y responden preguntas distintas.
