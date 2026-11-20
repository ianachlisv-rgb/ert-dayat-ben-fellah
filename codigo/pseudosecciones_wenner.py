"""Lee archivos de datos ERT en formato Res2DInv (arreglo Wenner) y dibuja sus pseudosecciones.

Formato esperado (.dat / .txt), como los de Dayat Ben Fellah:
    línea 1: nombre del perfil
    línea 2: espaciamiento mínimo entre electrodos (m)
    línea 3: tipo de arreglo (1 = Wenner)
    línea 4: número de datos
    línea 5: tipo de posición en x (1 = punto medio)
    línea 6: bandera de IP (0 = sin IP)
    luego, una fila por dato:  x_medio, a, resistividad aparente (Ω·m)
    (los comentarios y ceros finales del archivo se ignoran)

Pseudoprofundidad del arreglo Wenner: z = 0.519·a  (profundidad mediana de investigación, Edwards 1977).
Es una profundidad de dibujo, no la profundidad real de las estructuras.

Uso:
    python pseudosecciones_wenner.py carpeta_con_archivos/ salida/
    python pseudosecciones_wenner.py perfil.txt salida/
"""
import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

Z_FACTOR = 0.519   # Wenner


def leer_dat(ruta):
    """Devuelve (nombre, x, a, rho) como arreglos de numpy."""
    with open(ruta, encoding="latin-1") as f:
        lineas = [ln.strip() for ln in f.read().splitlines()]
    nombre = lineas[0] or os.path.basename(ruta)
    n = int(float(lineas[3]))
    filas = []
    for ln in lineas[5:]:
        partes = ln.replace(",", " ").split()
        if len(partes) < 3:
            if filas:
                break                                   # fin de los datos (ceros o líneas vacías)
            continue                                    # algunos archivos traen una línea en blanco antes de los datos
        try:
            filas.append([float(v) for v in partes[:3]])
        except ValueError:
            if filas:
                break
            continue
        if len(filas) == n:
            break
    if not filas:
        raise ValueError(f"{ruta}: no se encontraron datos")
    d = np.array(filas)
    if len(d) != n:
        print(f"  Aviso {nombre}: el encabezado dice {n} datos y se leyeron {len(d)}.", file=sys.stderr)
    return nombre.strip(), d[:, 0], d[:, 1], d[:, 2]


def pseudoseccion(nombre, x, a, rho, ruta_png):
    z = Z_FACTOR * a
    fig, ax = plt.subplots(figsize=(10, 3.6))
    sc = ax.scatter(x, z, c=rho, s=70, marker="s", cmap="turbo",
                    norm=LogNorm(vmin=max(rho.min(), 1), vmax=rho.max()))
    ax.invert_yaxis()
    ax.set_xlabel("Distancia (m)")
    ax.set_ylabel("Pseudoprofundidad (m)")
    ax.set_title(f"{nombre}: resistividad aparente, arreglo Wenner")
    ax.set_aspect("equal", adjustable="box")
    fig.colorbar(sc, ax=ax, label="ρa (Ω·m)", shrink=0.8)
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=200)
    plt.close(fig)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    entrada, salida = sys.argv[1], sys.argv[2]
    archivos = sorted(glob.glob(os.path.join(entrada, "*.txt")) + glob.glob(os.path.join(entrada, "*.dat"))) \
        if os.path.isdir(entrada) else [entrada]
    os.makedirs(salida, exist_ok=True)
    for ruta in archivos:
        nombre, x, a, rho = leer_dat(ruta)
        png = os.path.join(salida, os.path.splitext(os.path.basename(ruta))[0].replace(" ", "_").replace("'", "p") + ".png")
        pseudoseccion(nombre, x, a, rho, png)
        print(f"{nombre}: {len(rho)} datos, ρa {rho.min():.1f} a {rho.max():.1f} Ω·m, a = {a.min():g} a {a.max():g} m -> {png}")


if __name__ == "__main__":
    main()
