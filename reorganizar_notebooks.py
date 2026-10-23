"""
Reorganiza notebooks/ según el flujo vigente (degradación de pastizal, Landsat 8 + LandTrendr).

Por defecto NO toca nada: imprime lo que haría.

    python reorganizar_notebooks.py              # simulación, no modifica nada
    python reorganizar_notebooks.py --aplicar    # renombra y mueve los obsoletos a notebooks/_archivo/
    python reorganizar_notebooks.py --aplicar --borrar   # renombra y BORRA los obsoletos

Revisa la salida de la simulación antes de usar --aplicar.
Si el repositorio tiene los archivos commiteados, los borrados siguen recuperables con git.
"""

import argparse
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Renombres: nombre actual -> nombre nuevo
# ---------------------------------------------------------------------------
RENOMBRAR = {
    "01_inspeccion_limite_provincial.ipynb": "01_limite_provincial.ipynb",
    "04_catalogo_indicadores.ipynb": "02_mapbiomas_referencia.ipynb",
    "08_landsat8_compuestos_anuales.ipynb": "03_landsat8_compuestos_anuales.ipynb",
}

# ---------------------------------------------------------------------------
# Obsoletos: archivo -> motivo (el motivo se imprime y queda en _archivo/MOTIVOS.txt)
# ---------------------------------------------------------------------------
OBSOLETOS = {
    "02_revision_fuentes.ipynb":
        "Auditaba 7 fuentes, 5 ya descartadas. Resultado escrito en docs/01_datos_fuentes.md",
    "03_viabilidad_anios.ipynb":
        "Contaba escenas sobre el año completo. Lo reemplaza el diagnóstico del notebook 03",
    "05_visor_imagenes.ipynb":
        "Servía para elegir el índice a ojo. Decidido con bibliografía en docs/03_decisiones.md §5",
    "06_MapBiomas_Landsat8_Indicadores.ipynb":
        "Mitad Landsat reemplazada por el notebook 03; mitad MapBiomas por el 02",
    "06_MapBiomas_Landsat8_Indicadores_v1.ipynb": "Versión intermedia del 06",
    "06_MapBiomas_Landsat8_Indicadores_v2.ipynb": "Versión intermedia del 06",
    "06_MapBiomas_Landsat8_Indicadores_v3.ipynb": "Versión intermedia del 06",
    "06_MapBiomas_Landsat8_Indicadores_v4.ipynb": "Versión intermedia del 06",
    "06_MapBiomas_Landsat8_Indicadores_v4.html": "Export HTML de una versión intermedia",
    "06_MapBiomas_Landsat8_Indicadores_v5.ipynb":
        "Última versión del 06. Compuestos mensuales abandonados al pasar a compuesto anual",
    "07_definir_indicadores.ipynb": "Versión intermedia del 07",
    "07_definir_indicadores_v2.ipynb":
        "Decidía qué indicadores de MapBiomas usar. Ya decidido en docs/00_proyecto.md §3",
}

# ---------------------------------------------------------------------------
# Docs superados por la documentación nueva (docs/00 a 03)
# ---------------------------------------------------------------------------
DOCS_OBSOLETOS = {
    "01_alcance.md":
        "Alcance del enfoque de bosque. Integrado en docs/00_proyecto.md §5",
    "02_datos_fuentes.md":
        "Asumía Landsat 8+9, Sentinel-2 y GEOBOSQUES. Reemplazado por docs/01_datos_fuentes.md",
    "metodologia_general.md":
        "Metodología del enfoque de bosque con umbral de GEOBOSQUES. Reemplazada por docs/02_metodologia.md",
}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--aplicar", action="store_true", help="ejecuta los cambios")
    p.add_argument("--borrar", action="store_true",
                   help="con --aplicar, borra los obsoletos en vez de archivarlos")
    p.add_argument("--notebooks", default=None,
                   help="ruta a notebooks/ (por defecto: ./notebooks o la carpeta actual)")
    args = p.parse_args()

    # Localizar notebooks/
    if args.notebooks:
        nb = Path(args.notebooks)
    elif (Path.cwd() / "notebooks").is_dir():
        nb = Path.cwd() / "notebooks"
    elif Path.cwd().name == "notebooks":
        nb = Path.cwd()
    else:
        sys.exit("No encuentro la carpeta notebooks/. Usa --notebooks RUTA")

    nb = nb.resolve()
    print(f"Carpeta: {nb}")
    print(f"Modo   : {'APLICAR' if args.aplicar else 'SIMULACIÓN (no se modifica nada)'}"
          f"{'  ·  BORRADO DEFINITIVO' if args.aplicar and args.borrar else ''}")
    print("=" * 78)

    existentes = {f.name for f in nb.iterdir() if f.is_file()}
    archivo = nb / "_archivo"
    acciones, avisos = 0, []

    # ---------------------------------------------------- 1. archivar o borrar
    print("\nOBSOLETOS")
    print("-" * 78)
    for nombre, motivo in OBSOLETOS.items():
        if nombre not in existentes:
            avisos.append(f"no estaba: {nombre}")
            continue
        destino = "borrar" if args.borrar else f"_archivo/{nombre}"
        print(f"  {nombre}")
        print(f"      -> {destino}")
        print(f"      motivo: {motivo}")
        acciones += 1
        if not args.aplicar:
            continue
        origen = nb / nombre
        if args.borrar:
            origen.unlink()
        else:
            archivo.mkdir(exist_ok=True)
            shutil.move(str(origen), str(archivo / nombre))

    # ---------------------------------------------------- 2. renombrar
    print("\nRENOMBRES")
    print("-" * 78)
    for viejo, nuevo in RENOMBRAR.items():
        if viejo not in existentes:
            avisos.append(f"no estaba: {viejo}")
            continue
        if (nb / nuevo).exists() and viejo != nuevo:
            avisos.append(f"ya existe el destino, no se renombra: {nuevo}")
            continue
        print(f"  {viejo}")
        print(f"      -> {nuevo}")
        acciones += 1
        if args.aplicar:
            (nb / viejo).rename(nb / nuevo)

    # ---------------------------------------------------- 3. docs superados
    docs = nb.parent / "docs"
    if docs.is_dir():
        print("\nDOCS SUPERADOS")
        print("-" * 78)
        docs_archivo = docs / "_archivo"
        for nombre, motivo in DOCS_OBSOLETOS.items():
            if not (docs / nombre).is_file():
                avisos.append(f"no estaba: docs/{nombre}")
                continue
            destino = "borrar" if args.borrar else f"docs/_archivo/{nombre}"
            print(f"  docs/{nombre}")
            print(f"      -> {destino}")
            print(f"      motivo: {motivo}")
            acciones += 1
            if not args.aplicar:
                continue
            if args.borrar:
                (docs / nombre).unlink()
            else:
                docs_archivo.mkdir(exist_ok=True)
                shutil.move(str(docs / nombre), str(docs_archivo / nombre))

    # ---------------------------------------------------- 4. motivos en _archivo/
    if args.aplicar and not args.borrar and archivo.is_dir():
        lineas = ["Notebooks archivados en la reorganización del 2026-10-22.",
                  "Motivo de cada uno (detalle en notebooks/README.md):", ""]
        lineas += [f"- {n}: {m}" for n, m in OBSOLETOS.items()]
        (archivo / "MOTIVOS.txt").write_text("\n".join(lineas), encoding="utf-8")
        print(f"\nEscrito {archivo / 'MOTIVOS.txt'}")

    # ---------------------------------------------------- resumen
    print("\n" + "=" * 78)
    print(f"{acciones} acción(es) {'aplicadas' if args.aplicar else 'pendientes'}")
    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print("  ·", a)
    if not args.aplicar:
        print("\nNada se modificó. Para ejecutarlo:")
        print("  python reorganizar_notebooks.py --aplicar")
        print("  python reorganizar_notebooks.py --aplicar --borrar   (sin archivar)")
    else:
        print("\nListo. Estado final de notebooks/:")
        for f in sorted(nb.iterdir()):
            if f.is_file():
                print("  ", f.name)


if __name__ == "__main__":
    main()
