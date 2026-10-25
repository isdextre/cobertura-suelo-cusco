"""
Reorganiza la estructura del repo tras la renumeración de notebooks (2026-10-23).

Los notebooks con los NOMBRES NUEVOS ya están en notebooks/. Este script se encarga de lo
que queda: quitar los archivos con los nombres viejos y renombrar las carpetas de salida
para que lleven el número del notebook que las genera.

Por defecto NO toca nada: imprime lo que haría.

    python reorganizar_estructura.py                    # simulación
    python reorganizar_estructura.py --aplicar          # archiva en _archivo/
    python reorganizar_estructura.py --aplicar --borrar # borra en vez de archivar

Revisa la salida de la simulación antes de usar --aplicar.
Si el repositorio tiene los archivos commiteados, los borrados siguen recuperables con git.
"""

import argparse
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Notebooks viejos: su contenido vive ahora en el nombre nuevo
# ---------------------------------------------------------------------------
NOTEBOOKS_VIEJOS = {
    "01_limite_provincial.ipynb":
        "renombrado a 01_area_de_estudio.ipynb (+ celda de exportación del AOI)",
    "02_mapbiomas_referencia.ipynb":
        "renombrado a 02_referencia_cobertura.ipynb (+ celda de exportación de máscaras)",
    "03_landsat8_compuestos_anuales.ipynb":
        "renombrado a 04_serie_anual_landsat.ipynb (+ celda de exportación a asset)",
    "04_landtrendr.ipynb":
        "partido en 05_deteccion_cambio.ipynb y 06_control_deteccion.ipynb",
}

# ---------------------------------------------------------------------------
# Carpetas de salida: pasan a llevar el número del notebook que las genera
# ---------------------------------------------------------------------------
CARPETAS_SALIDA = {
    "mapbiomas_referencia": "02_referencia_cobertura",
    "landsat_compuestos_anuales": "04_serie_anual_landsat",
    "landtrendr": "05_deteccion_cambio",
}

# Todas las carpetas de salida del flujo. Las que no existan tras los renombres se crean
# vacías, para que la estructura se vea completa desde el principio.
CARPETAS_NUEVAS = [
    "01_area_de_estudio",
    "02_referencia_cobertura",
    "03_referencia_fuego",
    "04_serie_anual_landsat",
    "05_deteccion_cambio",
    "06_control_deteccion",
]

# Notebooks que deben existir con el nombre nuevo (verificación, no se tocan)
ESPERADOS = [
    "01_area_de_estudio.ipynb",
    "02_referencia_cobertura.ipynb",
    "03_referencia_fuego.ipynb",
    "04_serie_anual_landsat.ipynb",
    "05_deteccion_cambio.ipynb",
    "06_control_deteccion.ipynb",
]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--aplicar", action="store_true", help="ejecuta los cambios")
    p.add_argument("--borrar", action="store_true",
                   help="con --aplicar, borra los notebooks viejos en vez de archivarlos")
    p.add_argument("--raiz", default=None, help="raíz del repo (por defecto: la carpeta actual)")
    args = p.parse_args()

    raiz = Path(args.raiz) if args.raiz else Path.cwd()
    if not (raiz / "notebooks").is_dir():
        if (raiz.parent / "notebooks").is_dir():
            raiz = raiz.parent
        else:
            sys.exit("No encuentro la carpeta notebooks/. Usa --raiz RUTA")
    raiz = raiz.resolve()

    nb = raiz / "notebooks"
    out = raiz / "outputs"

    print(f"Raíz   : {raiz}")
    print(f"Modo   : {'APLICAR' if args.aplicar else 'SIMULACIÓN (no se modifica nada)'}"
          f"{'  ·  BORRADO DEFINITIVO' if args.aplicar and args.borrar else ''}")
    print("=" * 78)

    acciones, avisos = 0, []

    # ------------------------------------------------- 1. verificar los nuevos
    print("\nVERIFICACIÓN · los notebooks nuevos deben estar en su sitio")
    print("-" * 78)
    for nombre in ESPERADOS:
        existe = (nb / nombre).is_file()
        print(f"  {'✓' if existe else '✗'} {nombre}")
        if not existe:
            avisos.append(f"FALTA el notebook nuevo: {nombre}")

    if any(not (nb / n).is_file() for n in ESPERADOS):
        print("\n⚠ Faltan notebooks nuevos. Cópialos antes de aplicar este script,")
        print("  o los viejos se archivarán sin tener reemplazo en su sitio.")

    # ------------------------------------------------- 2. notebooks viejos
    print("\nNOTEBOOKS CON NOMBRE VIEJO")
    print("-" * 78)
    archivo = nb / "_archivo"
    for nombre, motivo in NOTEBOOKS_VIEJOS.items():
        if not (nb / nombre).is_file():
            avisos.append(f"no estaba: notebooks/{nombre}")
            continue
        destino = "borrar" if args.borrar else f"_archivo/{nombre}"
        print(f"  {nombre}")
        print(f"      -> {destino}")
        print(f"      {motivo}")
        acciones += 1
        if not args.aplicar:
            continue
        if args.borrar:
            (nb / nombre).unlink()
        else:
            archivo.mkdir(exist_ok=True)
            shutil.move(str(nb / nombre), str(archivo / nombre))

    # ------------------------------------------------- 3. carpetas de salida
    print("\nCARPETAS DE SALIDA")
    print("-" * 78)
    if out.is_dir():
        for viejo, nuevo in CARPETAS_SALIDA.items():
            origen, destino = out / viejo, out / nuevo
            if not origen.is_dir():
                avisos.append(f"no estaba: outputs/{viejo}")
                continue
            if destino.exists():
                avisos.append(f"el destino ya existe, no se renombra: outputs/{nuevo}")
                continue
            n = len(list(origen.iterdir()))
            print(f"  outputs/{viejo}  ->  outputs/{nuevo}   ({n} archivo(s))")
            acciones += 1
            if args.aplicar:
                origen.rename(destino)

        # Carpetas vacías de los notebooks que todavía no han corrido
        for nueva in CARPETAS_NUEVAS:
            if (out / nueva).is_dir():
                continue
            print(f"  crear outputs/{nueva}/   (vacía, la llenará su notebook)")
            acciones += 1
            if args.aplicar:
                (out / nueva).mkdir(parents=True, exist_ok=True)
    else:
        avisos.append("no existe la carpeta outputs/")

    # ------------------------------------------------- 4. motivos
    if args.aplicar and not args.borrar and archivo.is_dir():
        lineas = ["Notebooks archivados en la renumeración del 2026-10-23.",
                  "Su contenido vive ahora en los nombres nuevos (ver notebooks/README.md):", ""]
        lineas += [f"- {n}: {m}" for n, m in NOTEBOOKS_VIEJOS.items()]
        destino_txt = archivo / "MOTIVOS_renumeracion.txt"
        destino_txt.write_text("\n".join(lineas), encoding="utf-8")
        print(f"\nEscrito {destino_txt}")

    # ------------------------------------------------- resumen
    print("\n" + "=" * 78)
    print(f"{acciones} acción(es) {'aplicadas' if args.aplicar else 'pendientes'}")
    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print("  ·", a)
    if not args.aplicar:
        print("\nNada se modificó. Para ejecutarlo:")
        print("  python reorganizar_estructura.py --aplicar")
        print("  python reorganizar_estructura.py --aplicar --borrar   (sin archivar)")
    else:
        print("\nEstado final de notebooks/:")
        for f in sorted(nb.iterdir()):
            print(f"   {'[dir] ' if f.is_dir() else ''}{f.name}")
        if out.is_dir():
            print("\nEstado final de outputs/:")
            for f in sorted(out.iterdir()):
                n = len(list(f.iterdir())) if f.is_dir() else 0
                print(f"   {f.name}/   ({n} archivo(s))")


if __name__ == "__main__":
    main()
