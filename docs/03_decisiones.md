# 03 · Registro de decisiones con respaldo bibliográfico

**Versión:** 1.0 · **Fecha:** 2026-10-22

Cada decisión de diseño con su motivo y su fuente. Sirve para defender el método ante revisión y
para no reabrir discusiones ya cerradas.

**Advertencia de verificación:** las autorías de Dara et al. (2020), Sonnenschein et al. (2011),
Wessels, van den Bergh y Scholes (2012) y Gelabert et al. (2021) están confirmadas. Varios
benchmarks recientes se citan por revista y volumen sin la lista completa de autores; **hay que
verificarlos antes de citarlos formalmente** en el paper.

---

## 1 · Objeto de estudio: pastizal, no bosque

**Decisión:** degradación de formación herbácea (MapBiomas clase 12) como indicador principal.
Bosque como referencia secundaria.

**Motivo:** el bosque ocupa 2.0 km² de los 530.1 km² de la provincia (0.38 %) y su cambio anual
según MapBiomas es de 0.02 a 0.11 km², unos 89 píxeles a 30 m. Una estimación de área con
intervalos de confianza sobre esa población da intervalos más anchos que la estimación. La
formación herbácea es el 48.6 % del territorio.

**Aporte científico:** MapBiomas reporta la formación herbácea como estable (258.3 → 260.5 km² en
13 años) porque asigna una clase por año y no puede ver degradación *dentro* de la clase. Un pajonal
que pierde densidad sigue clasificado como formación herbácea hasta cruzar a otra clase. La
segmentación temporal sobre un índice sensible a humedad y suelo expuesto sí detecta ese proceso.

---

## 2 · Sensor: solo Landsat 8

**Decisión:** `LANDSAT/LC08/C02/T1_L2`, Tier 1. Sin Landsat 9, 7 ni Sentinel-2.

**Motivo:** LandTrendr lee la forma de la trayectoria temporal, así que es sensible a cualquier
cambio del régimen de muestreo a mitad de serie. Landsat 9 cubre solo 2021→, lo que duplicaría las
observaciones en los últimos cuatro años: el medoide de 2024 se elegiría entre el doble de
candidatos que el de 2015, mejorando sistemáticamente la calidad del compuesto por razones de
muestreo y no de terreno. Ese escalón en 2021–2022 es indistinguible de un disturbio.

Landsat 7 exigiría armonización — Roy et al. (2016), *RSE* 185:57–70, mostraron que el NDVI de OLI
es sistemáticamente mayor que el de ETM+ sobre vegetación — y arrastra el bandeado SLC-off y la
deriva orbital. Sentinel-2 reproduce el problema de densidad, agravado.

**Costo aceptado:** ~3.76 observaciones limpias por píxel y año, apenas sobre el mínimo práctico
de 3. Verificado en el notebook 03.

---

## 3 · Ventana temporal: 1 jun – 31 ago

**Decisión:** estación seca plena. Respaldo 15 may – 15 sep solo si falta cobertura.

**Motivo:** incluir marzo y abril (fin de lluvias) mezcla estados fenológicos, y como la proporción
de escenas claras de esos meses varía entre años, **la fecha efectiva del compuesto se desplaza de
año en año**. Para un algoritmo que lee trayectorias, eso es ruido estructurado que imita cambio
real.

**Respaldo:** la guía de LT-GEE recomienda probar varias ventanas y advierte que el hemisferio sur
debe adaptarlas. Pasquarella et al. (2022), *International Journal of Applied Earth Observation and
Geoinformation*, muestran que las fechas de inicio y fin afectan el ajuste y los vértices.
Precedente regional: Cano, Pizarro, Cacciuttolo, Peñaloza, Yaranga y Gandini (2023),
*Sustainability* 15(21):15472, usaron abril–octubre en la puna de Junín, sin analizar el efecto
fenológico de esa amplitud.

**Tensión sin resolver:** la ventana seca tiene menos nubes pero captura pajonal senescente, donde
los índices basados en clorofila pierden rango dinámico. Es un argumento adicional a favor de TCW.

---

## 4 · Compuesto: medoide

**Decisión:** medoide, no mediana por banda.

**Motivo:** la mediana por banda toma el valor central de cada banda independientemente, así que
puede combinar el azul de junio con el NIR de agosto y el SWIR de julio. El píxel resultante nunca
se observó. Eso rompe las relaciones entre bandas de las que dependen las componentes Tasseled Cap,
cuyos coeficientes fueron derivados asumiendo seis bandas de la misma medición. El medoide elige la
**observación completa** más cercana al vector mediano: siempre un píxel real, con sus seis bandas
coherentes.

**Respaldo:** la guía de LT-GEE declara preferir el medoide. Flood (2013), *Remote Sensing*
5(12):6481, mostró que representa la serie mejor que el compuesto de máximo NDVI, con residuos hasta
un orden de magnitud menores.

**Sin consenso:** un estudio de 2023 en *International Journal of Digital Earth* encontró mejor
clasificación con la mediana y señaló que el medoide puede dar discontinuidad espacial. Para
alimentar un segmentador, la coherencia radiométrica pesa más que la continuidad espacial.

---

## 5 · Índice primario: −TCW

**Decisión:** Tasseled Cap Wetness invertido para la segmentación. NDVI, MSAVI, TCG, TCB, BSI y
NDMI como acompañantes (`ftvList`).

**Motivo físico:** en pajonal senescente de época seca (*Festuca*, *Stipa ichu*, *Calamagrostis*)
no hay clorofila activa, así que el contraste rojo/NIR del que vive el NDVI se desploma y un
pastizal sano-pero-seco se parece a uno degradado. TCW no mide actividad fotosintética sino
**contenido de agua** (pesos fuertemente negativos en SWIR1 y SWIR2), y un pastizal degradado
retiene menos agua independientemente de su estado fenológico.

**Respaldo empírico:**

- Dara, Baumann, Freitag, Hölzel, Hostert, Kamp, Müller, Prishchepov y Kuemmerle (2020),
  *RSE* 239:111667 — en estepa post-soviética con gradiente de pastoreo, la mediana de TCW superó a
  las demás métricas individuales con 78 % de exactitud global.
- Gelabert, Rodrigues, de la Riva, Ameztegui, Sebastià y Vega-Garcia (2021), *RSE* 262:112521 — en
  pérdida de pastizal por arbustización, la mejor estrategia usó series de TCB y TCW ajustadas por
  LandTrendr (F1 = 0.85).
- Sonnenschein, Kuemmerle, Udelhoven, Stellmes y Hostert (2011), *RSE* 115:1408–1420 — tomando las
  fracciones de unmixing como referencia física, la similitud decrece de TCG a SAVI y por último
  NDVI.

**La inversión de signo es obligatoria:** LT-GEE exige que la pérdida de vegetación sea un delta
**positivo**. Como la degradación hace bajar TCW, se multiplica por −1. Omitir este paso invierte
degradaciones y recuperaciones; es el error más común al usar la herramienta.

**Alternativa superior, si hay tiempo:** fracción de suelo o NPV de unmixing espectral lineal, o
NDFI estilo Souza/MapBiomas. Davidson et al. (2008), *JGR Biogeosciences*, en pasturas amazónicas:
NPV y suelo aumentan con la edad de la pastura, y concluyen que NPV es un escalar objetivo del grado
de degradación. Requiere calibrar endmembers locales de puna; sin esa calibración, separar NPV de
suelo con bandas Landsat es difícil y depende del color del suelo.

**Pendiente:** verificar −TCW contra 3–4 candidatos sobre los puntos de calibración, eligiendo por
F1. No existe ningún paper que compare índices dentro de LandTrendr para pastizal andino.

---

## 6 · Coeficientes Tasseled Cap: Baig et al. (2014)

**Decisión:** Baig et al. (2014), *Remote Sensing Letters* 5(5):423–431, derivados para Landsat 8
OLI. Crist (1985) queda disponible como alternativa en el código.

**Salvedad declarada:** Baig se derivó para reflectancia *at-satellite* y aquí se aplica a
reflectancia de superficie. Es práctica común y no afecta a LandTrendr, que trabaja sobre el cambio
relativo de la trayectoria y no sobre el valor absoluto, siempre que el juego de coeficientes sea el
mismo en todos los años — que es el caso.

---

## 7 · Escalado y máscara de calidad

**Escalado:** `SR = DN × 0.0000275 − 0.2` antes de cualquier índice, con recorte a [0, 1]. Fuente:
USGS, *Landsat 8-9 Collection 2 Level 2 Science Product Guide* (LSDS-1619), y la FAQN del USGS sobre
factores de escala.

Crítico porque Tasseled Cap, MSAVI y BSI tienen términos aditivos. **Y también importa para el
NDVI**: el factor multiplicativo se cancela en el cociente, pero el offset −0.2 no. Saltarse el
escalado da un NDVI que parece razonable y está sesgado — el peor tipo de error, porque no falla.

**Máscara:** `QA_PIXEL` bits 0–5 (relleno, nube dilatada, cirrus, nube, sombra de nube, nieve),
confianza de nube ≥ media, confianza alta de sombra y cirrus, `QA_RADSAT ≠ 0`, y `SR_QA_AEROSOL`
con aerosol alto.

**Por qué desde confianza media y no solo alta:** el default del USGS y de LT-GEE es alta
confianza. Enmascarar desde media es una decisión conservadora propia: en montaña la nube delgada es
frecuente y su sesgo apunta siempre en la misma dirección — baja TCW y NDVI, o sea **falsa
degradación**. Preferimos perder píxeles a ganar señal falsa.

**Contrapeso:** en puna los suelos claros y la nieve hacen que CFMask marque de más. El notebook 03
incluye verificación visual; si se pierde demasiado terreno real, `CONF_NUBE_MIN = 3` lo relaja.

*Juicio experto, no óptimo publicado:* el umbral de confianza media, el mínimo de 3 observaciones
claras por año y `CLOUD_COVER_LAND < 65 %` son decisiones razonadas sin respaldo numérico directo.

---

## 8 · Parámetros de LandTrendr

**Decisión:** valores de partida en `02_metodologia.md` paso 4, a calibrar contra puntos
interpretados.

**Motivo del cambio respecto al default:** los valores por defecto de LT-GEE se calibraron para
**bosque** (NBR, Oregón y Washington) y series de 25–35 años. Con 13 observaciones anuales,
`maxSegments = 6` permite hasta 7 vértices, lo que con ruido climático interanual lleva a
sobresegmentación: vértices que siguen años secos y húmedos, no degradación.

**Respaldo:**

- Kennedy, Yang y Cohen (2010), *RSE* 114:2897–2910 — algoritmo original; calibraron contra 388
  parcelas interpretadas en TimeSync, no contra RMSE.
- Kennedy et al. (2018), *Remote Sensing* 10(5):691 — implementación en GEE y valores de los
  ejemplos.
- *Remote Sensing* 2025, 17(4):680 — análisis de sensibilidad sobre China: óptimos
  `recoveryThreshold = 0.5` y `spikeThreshold = 0.85`. Bosque.
- *Remote Sensing* 2025, 17(14):2402 — benchmark urbano global: mejores F1 con `maxSegments` 4 o 5;
  con 3 bajan los falsos positivos pero suben las omisiones.

**Sin consenso:** no existe ningún estudio de sensibilidad específico para pastizal. Todos los
óptimos publicados vienen de bosque o de cambio urbano.

---

## 9 · Índices acompañantes y atribución del tipo de cambio

**Decisión:** una sola corrida de LandTrendr, con `ftvList`. Los vértices los define el índice
primario y los acompañantes se ajustan en ellos.

**Respaldo:** la función `ee.Algorithms.TemporalSegmentation.LandTrendr` define que la primera banda
encuentra los quiebres y las siguientes se ajustan con esos quiebres; LT-GEE está construido para
eso. Kennedy et al. (2018) describen FTV como medio para caracterizar el cambio en múltiples
dimensiones espectrales.

**Limitación:** un cambio visible en BSI pero no en el índice de segmentación no generará vértice.

**Clasificadores sobre las salidas:** Cohen et al. (2018), *RSE* 205:131–140 — random forest sobre
salidas de LandTrendr de 6 bandas y 7 índices; el ensamble multiespectral mejora la detección frente
a cualquier índice individual. Healey et al. (2018), *RSE*, y el sistema LCMS del USDA Forest
Service usan el mismo enfoque. Dara et al. (2020): combinar métricas en random forest superó
claramente a cualquier métrica individual.

---

## 10 · Validación: muestreo estratificado, no holdout temporal

**Decisión:** muestreo aleatorio estratificado con interpretación visual ciega y estimación de área
con IC 95 %.

**Respaldo:** Olofsson, Foody, Herold, Stehman, Woodcock y Wulder (2014), *RSE* 148:42–57 — diseño
probabilístico con las clases de cambio del mapa como estratos, matriz de error en proporción de
área, exactitudes de usuario y productor, estimación de área con intervalos, y recomendación
explícita de no usar kappa. Cohen, Yang y Kennedy (2010), *RSE* — TimeSync, el estándar del propio
ecosistema LandTrendr; Cohen et al. (2018) validaron con 2360 puntos TimeSync en 22 escenas.

**Por qué se descarta el holdout temporal:** LandTrendr es una segmentación **no supervisada**,
ajustada independientemente a la serie completa de cada píxel. No aprende parámetros en un periodo
para aplicarlos a otro y no extrapola. Retener 2023–2025 no prueba nada sobre la exactitud de los
vértices de 2013–2022, acorta una serie ya corta, y comparar una "predicción" con los años
retenidos mide la persistencia de la última pendiente, no la detección de degradación. No se
encontró ningún paper que proponga holdout temporal para LandTrendr.

**Por qué el RMSE no es validación:** LT-GEE lo entrega como banda, pero solo mide cuánto se pega la
polilínea a la serie de entrada. Un modelo sobresegmentado baja el RMSE y empeora la detección real.
Sirve como diagnóstico de calidad por píxel, nada más.

**Lo que sí es válido:** separación **espacial** entre calibración y validación, y un análisis de
estabilidad (correr 2013–2022 y 2013–2025 y verificar que los vértices comunes no se muevan).

---

## 11 · Atribución climática

**Decisión:** añadir una capa de atribución con RESTREND sobre CHIRPS o PISCO más ERA5-Land.

**Motivo:** en pastizal semiárido y de altura la variabilidad interanual de lluvia domina el verdor.
Mazzarino y Finn (2016), *Wetlands Ecology and Management*, encontraron en una cuenca semiárida del
sur de Perú que el NDVI de estación seca se correlaciona con la precipitación de la estación húmeda
(R² = 0.56). Sin este control, una sequía se lee como degradación.

**Método:** Evans y Geerken (2004) — regresión vegetación–precipitación por píxel y tendencia de los
residuos; residuos negativos = degradación no explicada por el clima. Burrell et al. (2017), *RSE* —
TSS-RESTREND, la variante segmentada, más sensible.

**Limitaciones declaradas:** Wessels, van den Bergh y Scholes (2012), *RSE* 125:10–22 — con
degradación simulada ≥20 % la relación NDVI–lluvia se rompe y RESTREND deja de ser confiable;
además la degradación >20 % solo era detectable si no ocurría al inicio o al final del periodo. Con
13 años la regresión tiene poca potencia, y la precipitación a ~5 km frente a píxeles de 30 m limita
la atribución local.

---

## 12 · Procesamiento

| Decisión | Valor | Fuente |
|---|---|---|
| Mosaico path/row | Enmascarar cada escena primero, componer después | Práctica estándar de LT-GEE (`buildSRcollection`). Las franjas de solape aportan observaciones extra |
| CRS y resolución | EPSG:32719, 30 m nativos, sin remuestreo | Cualquier remuestreo mezcla píxeles vecinos; en una serie que compara el mismo píxel entre años, medio píxel de desplazamiento introduce diferencias que no están en el terreno |
| Años faltantes | No interpolar | La API de LT-GEE indica que una banda enmascarada actúa como relleno y el algoritmo omite la observación. Una interpolación lineal entre dos años *es* una tendencia, justo lo que el algoritmo busca |
| Unidad mínima | 1 ha (11 píxeles) | Decisión de alcance previa, mantenida |

---

## 13 · Vacíos reconocidos

- **No existe literatura revisada por pares que aplique LandTrendr a degradación de pastizal en
  puna, altiplano o páramo.** Las decisiones extrapolan desde estepas de Asia Central, drylands
  mediterráneos, Mongolia Interior, Tíbet y rangelands de EE. UU. Es limitación y oportunidad de
  aporte original.
- **No hay comparación publicada de LandTrendr vs. CCDC, BFAST o Theil-Sen para degradación gradual
  de pastizal.** Lo disponible es de otros dominios: en cambio urbano CCDC alcanza F1 78.1 % frente
  a 74.3 % de BFAST y 71.3 % de LandTrendr (*Remote Sensing* 2025, 17(14):2402); en bosque del Gran
  Khingan LandTrendr tuvo la mayor exactitud espacial (OA 0.862). Correr CCDC o CODED en una
  submuestra para comparar sería un aporte original.
- **El efecto de las heladas de época seca sobre el verdor Landsat en puna no está cuantificado.** Lo
  más cercano es Anderson et al. (2021), *JGR Biogeosciences*, que identifica las temperaturas
  mínimas de inicio de verano como influencia secundaria sobre la productividad de bofedales.
- **Bofedales:** CFMask puede marcarlos como agua. Se tratan como estrato aparte; su dinámica
  depende de agua y nieve (Chávez et al. 2019, *Remote Sensing* 11(24):2955).
