# Taller 2 – Python (Qt Designer - Raspberry)
EP1 Algoritmos de Robótica

## Integrantes:

Jessica Daniela Bernal Gómez - 120093

Jorman Santiago Preciado Duque - 122828

Danilo Rodríguez Malago - 119238

Brayan Rincón Daza - 89458

## Entorno y ejecución en Windows

El entorno local está en `.venv`. No se sube a Git y no necesita activarse
para usar los comandos siguientes desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe ejecutar.py parteA/PuntoA-4.py
.\.venv\Scripts\python.exe ejecutar.py parteA/PuntoA-5.py
.\.venv\Scripts\python.exe ejecutar.py ruta/al/diseno.ui
```

También se puede usar `.\ejecutar.ps1 parteA/PuntoA-4.py` si la política
de PowerShell permite scripts.

Los archivos `.ui` se previsualizan con PyQt5; la lógica de botones,
cálculos y GPIO debe conectarse desde Python. La parte B incluye cinco archivos `.ui` editables. El entorno incluye `pyuic5.exe` para convertirlos:

```powershell
.\.venv\Scripts\pyuic5.exe diseno.ui -o diseno_ui.py
```

Qt Designer es un editor separado; no es necesario para abrir los diseños
con este lanzador. Los widgets personalizados y recursos compilados
requieren sus módulos correspondientes.

Para recrear el entorno con Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements-lock.txt` registra las versiones verificadas del entorno;
puede usarse en lugar de `requirements.txt` para reproducirlas.

La parte A funciona en Windows. La parte B incluye cinco interfaces con
conexión directa GPIO/I2C en Raspberry Pi OS. Consulta
[ParteB/README.md](ParteB/README.md) para conexiones, componentes y ejecución.
El ejemplo MicroPython anterior se conserva como referencia.
