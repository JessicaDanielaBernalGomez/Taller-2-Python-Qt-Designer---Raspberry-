"""Ejecuta un programa Python o previsualiza un diseño de Qt Designer."""
import argparse
import os
from pathlib import Path
import runpy
import sys

RAIZ = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", type=Path, help="Ruta al archivo .py o .ui")
    args = parser.parse_args()
    archivo = args.archivo.resolve()
    if not archivo.is_file():
        parser.error(f"No existe el archivo: {archivo}")
    if archivo.suffix.lower() not in (".py", ".ui"):
        parser.error("Selecciona un archivo .py o .ui.")
    # Los programas del taller buscan el logo en el directorio de trabajo.
    os.chdir(RAIZ)
    if archivo.suffix.lower() == ".py":
        sys.path.insert(0, str(archivo.parent))
        sys.argv = [str(archivo)]
        runpy.run_path(str(archivo), run_name="__main__")
    else:
        from PyQt5 import QtWidgets, uic
        app = QtWidgets.QApplication([str(archivo)])
        # Resolver recursos relativos al archivo de Designer.
        os.chdir(archivo.parent)
        ventana = uic.loadUi(str(archivo))
        ventana.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
