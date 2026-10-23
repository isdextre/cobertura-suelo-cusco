# Notebooks

Orden de ejecución del flujo vigente (degradación de pastizal, Landsat 8 + LandTrendr).
Cada notebook depende de los anteriores: ejecútalos en orden.

| # | Notebook | Qué hace | Estado |
|---|---|---|---|
| 01 | `01_limite_provincial.ipynb` | Carga y verifica el límite provincial del INEI. Define el AOI que usa todo el resto | Ejecutado |
| 02 | `02_mapbiomas_referencia.ipynb` | Composición de la provincia por clase y año, máscara de pastizal (clase 12) e indicadores de referencia | Ejecutado · pide revisión (ver abajo) |
| 03 | `03_landsat8_compuestos_anuales.ipynb` | Serie anual 2013–2025 de Landsat 8: compuesto medoide de estación seca con 7 índices espectrales | **Ejecutado 2026-10-22** · notebook de referencia |
| 04 | `04_landtrendr.ipynb` | Segmentación temporal con −TCW y los 6 índices acompañantes | Por crear |
| 05 | `05_tipo_de_cambio.ipynb` | Caracteriza cada quiebre: degradación, quema, conversión agrícola, urbano | Por crear |
| 06 | `06_validacion.ipynb` | Muestreo estratificado, interpretación visual y estimación de área con IC 95 % | Por crear |
| 07 | `07_atribucion_climatica.ipynb` | RESTREND para separar degradación antrópica de respuesta a sequía | Por crear |
| 08 | `08_indicadores_entregables.ipynb` | Indicadores finales, tablas, mapas y visualización | Por crear |

El notebook **03** es el estándar de estilo y documentación del proyecto: constantes
parametrizadas al inicio, una celda markdown explicando el *por qué* antes de cada bloque de
código, diagnóstico de calidad de los datos, control visual y celda de resumen al final. Los
notebooks nuevos siguen ese formato.

## Pendiente en el notebook 02

Se ejecutó con el enfoque anterior del proyecto (pérdida de bosque), así que agrupa las clases con
el bosque al centro: `{'bosque': [3,4,5,6], 'agricola': [21], 'pastos': [12,15], ...}`.

Sus números siguen siendo válidos y son los que sustentan el cambio de enfoque
(`docs/00_proyecto.md` §2), pero cuando se vuelva a ejecutar hay que reorientar la agrupación al
pastizal y añadir la máscara de la clase 12, que es lo que consume el paso 2 de la metodología.

## Qué se eliminó y por qué

La reorganización del 2026-10-22 quitó 11 notebooks. Motivos:

| Notebook | Motivo |
|---|---|
| `02_revision_fuentes.ipynb` | Auditaba 7 fuentes, 5 de ellas ya descartadas. Su resultado quedó escrito en `docs/01_datos_fuentes.md`, que es donde pertenece |
| `03_viabilidad_anios.ipynb` | Contaba escenas por año sobre el año completo. Lo reemplaza el diagnóstico del notebook 03, que mide la ventana real con la máscara real |
| `05_visor_imagenes.ipynb` | Existía para elegir el índice espectral a ojo. El índice se decidió con bibliografía (`docs/03_decisiones.md` §5) y el notebook 03 ya trae control visual |
| `06_MapBiomas_Landsat8_Indicadores*` (6 versiones + 1 HTML) | Su mitad Landsat la reemplaza el notebook 03; su mitad MapBiomas, el notebook 02. Los compuestos mensuales que exploraba se abandonaron al pasar a compuesto anual |
| `07_definir_indicadores*` (2 versiones) | Servía para decidir qué indicadores de MapBiomas usar. Ya decidido en `docs/00_proyecto.md` §3 |

Si el repositorio tenía estos archivos commiteados, siguen recuperables con `git log` y
`git checkout`. El script `reorganizar_notebooks.py` por defecto los mueve a `_archivo/` en vez de
borrarlos.
