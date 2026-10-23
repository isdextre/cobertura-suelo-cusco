# Proyecto · Degradación de pastizal altoandino en la provincia de Cusco

**Versión:** 1.0 · **Fecha:** 2026-10-22 · **Cliente:** Gobierno Regional de Cusco
**Reemplaza:** `00_proyecto.md` v0.x y `01_alcance.md` (ambos planteaban pérdida de bosque como
indicador principal; ver sección 6, "Cambio de enfoque").

---

## 1. Objetivo

Medir la **degradación de pastizal altoandino** en la provincia de Cusco entre 2013 y 2025:
la pérdida gradual de cobertura vegetal herbácea con aparición de suelo desnudo, detectada a
partir de la trayectoria temporal de cada píxel en Landsat 8.

### Pregunta principal

¿Qué superficie de pastizal se degradó en la provincia de Cusco entre 2013 y 2025, dónde, en qué
año empezó cada proceso y con qué incertidumbre se estima?

### Preguntas secundarias

- ¿Dónde se concentra la degradación (zonas críticas)?
- ¿Qué parte de la pérdida detectada es atribuible a variabilidad climática y qué parte no?
- ¿Cómo evoluciona la tasa de degradación a lo largo del periodo?
- ¿Qué aporta este análisis que MapBiomas no reporta?

---

## 2. Por qué el pastizal y no el bosque

La decisión se tomó con datos, no por preferencia. Composición de la provincia según MapBiomas
Perú Colección 4 (notebook 02, ejecutado), en km² para 2013 sobre un total de 530.1 km²:

| Clase MapBiomas | km² | % de la provincia |
|---|---|---|
| **12 · Formación herbácea** | **258.3** | **48.6 %** |
| 21 · Mosaico agropecuario | 148.4 | 27.9 % |
| 24 · Infraestructura urbana | 28.3 | 5.3 % |
| 9 · Plantación forestal | 9.9 | 1.9 % |
| **3 · Bosque** | **2.0** | **0.38 %** |
| 15 · Pasto (beta) | 1.7 | 0.3 % |

Dos consecuencias:

**El bosque no es medible aquí con el rigor que exige el entregable.** MapBiomas reporta una
pérdida de bosque de 0.02 a 0.11 km² por año en la provincia. A 30 m de resolución, 0.08 km² son
unos 89 píxeles, y la unidad mínima de mapeo de 1 ha (11 píxeles) deja buena parte de esos cambios
por debajo del umbral reportable. Una estimación de área con intervalos de confianza según
Olofsson et al. (2014) sobre una población de ese tamaño produce intervalos más anchos que la
propia estimación. No es una limitación del método: es que no hay suficiente bosque que medir.

**El pastizal es casi la mitad del territorio y MapBiomas lo reporta estable.** La formación
herbácea pasa de 258.3 km² en 2013 a 260.5 km² en 2025 — sin cambio neto apreciable. Ahí está el
aporte de este trabajo: MapBiomas asigna una clase por año, así que informa si el píxel **sigue
siendo** pastizal, no en qué **condición** está. Un pajonal que pierde densidad y expone suelo
sigue clasificándose como formación herbácea hasta que el cambio es tan grande que cruza a otra
clase. Esa degradación intraclase es invisible para un clasificador anual y sí es detectable con
segmentación temporal sobre un índice sensible a humedad y suelo expuesto.

---

## 3. Indicadores

### Principal

- **Superficie degradada de pastizal** (km² y % del pastizal), por año de inicio del proceso,
  con intervalo de confianza al 95 %.
- **Año de quiebre** por píxel: cuándo empieza la trayectoria descendente.
- **Magnitud y duración** del proceso de degradación.
- **Tasa de degradación** por periodo.

### Secundarios

- **Degradación atribuible a clima vs. no atribuible**, separadas con un control de precipitación
  (paso 7 de la metodología).
- **Tipo de cambio**: degradación gradual, quema, conversión a agrícola, expansión urbana
  (paso 5).
- **Pérdida y ganancia de bosque**: se reporta **como referencia de MapBiomas**, con la limitación
  de la sección 2 declarada explícitamente. No se calcula con indicador propio ni se le aplica
  estimación de área con intervalos, porque el tamaño de la población no lo soporta.

### Fuera de alcance

- Expansión urbana como indicador propio. Se menciona como factor asociado donde explique
  degradación de pastizal (la clase 24 crece de 28.3 a 33.7 km² entre 2013 y 2021, mayormente
  sobre mosaico agropecuario).
- Territorios fuera de la provincia de Cusco, aunque pertenezcan al departamento.
- Bofedales y humedales como objeto propio: su dinámica depende de agua y nieve, no del pajonal.
  Se tratan como estrato aparte y se excluyen del indicador principal.

---

## 4. Entregables

| # | Entregable | Fuente (paso de metodología) |
|---|---|---|
| 1 | Mapa de degradación de pastizal: año de inicio, magnitud y duración por píxel | 4 |
| 2 | Tabla de superficie degradada por periodo con IC 95 % | 6 |
| 3 | Reporte de exactitud con matriz de error en proporción de área | 6 |
| 4 | Mapa de zonas críticas y tabla de factores asociados | 5 y 7 |
| 5 | Separación clima / no clima de la pérdida detectada | 7 |
| 6 | Tabla comparativa contra los indicadores de referencia de MapBiomas | 2 y 8 |
| 7 | Visualización de la evolución 2013–2025 | 8 |

---

## 5. Alcance

- **Espacial:** provincia de Cusco (`ccdd = 08`, `ccpp = 01`) del límite INEI, 530.1 km² en
  EPSG:32719. El notebook 01 verifica si el polígono cruza el meridiano −72° (frontera UTM 18S/19S).
- **Temporal:** 2013–2025. 2013 es el primer año de Landsat 8.
- **Resolución:** 30 m, nativa de Landsat, sin remuestreo.
- **Unidad mínima de mapeo:** 1 ha (11 píxeles de 30 m). Los parches menores se reportan como
  "no reportable".
- **Clase objetivo:** MapBiomas clase 12 (formación herbácea). La clase 15 (pasto, marcada como
  beta por MapBiomas) se evalúa aparte por su carácter preliminar y su tamaño reducido.
- **2026:** fuera del periodo. La ventana seca de 2026 ya pasó y podría clasificarse como
  extensión, marcada como tal.

---

## 6. Cambio de enfoque (2026-10-22)

El planteamiento original de este proyecto tenía la **pérdida de bosque** como indicador principal,
con clases bosque / no bosque y la definición de GEOBOSQUES como autoridad. Está documentado en las
versiones anteriores de `00_proyecto.md`, `01_alcance.md` y `metodologia_general.md`, y en los dos
documentos de `docs/` en formato Word.

Ese enfoque se reemplaza por el de este documento. El motivo es el de la sección 2: el bosque ocupa
el 0.38 % de la provincia y su cambio anual está en el orden de decenas de píxeles.

**Pendiente de actualizar con este enfoque:**

- `docs/Paper_Cusco_LandTrendr_MapBiomas.docx` — título, resumen, objetivos y metodología están
  escritos sobre pérdida de bosque.
- `docs/Informe_Entregable1_Cusco.docx` — mismos indicadores; además asume Landsat 8 + 9, y la
  decisión vigente es solo Landsat 8 (ver `01_datos_fuentes.md`).
