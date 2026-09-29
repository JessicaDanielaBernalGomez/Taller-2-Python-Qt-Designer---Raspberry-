# Parte B — Qt Designer y Raspberry Pi

Los cinco programas cargan sus archivos `.ui` editables en Qt Designer.
Todos arrancan en **SIMULACIÓN**, incluyendo en Raspberry Pi. Seleccionar
«Raspberry Pi (hardware real)» y pulsar «Conectar / reiniciar conexión» activa
el hardware. Un error se muestra como SIN CONEXIÓN y no cambia a simulación.

## Ejecutar en Windows

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe ejecutar.py ParteB/PuntoB-1.py
.\.venv\Scripts\python.exe ejecutar.py ParteB/PuntoB-2.py
.\.venv\Scripts\python.exe ejecutar.py ParteB/PuntoB-3.py
.\.venv\Scripts\python.exe ejecutar.py ParteB/PuntoB-4.py
.\.venv\Scripts\python.exe ejecutar.py ParteB/PuntoB-5.py
```

En VS Code selecciona el intérprete `.venv/Scripts/python.exe` y abre el
archivo `PuntoB-N.py` para usar «Run Python File».
Abrir un `.ui` con el lanzador solo previsualiza el diseño; ejecutar su
`.py` conecta botones y controladores.

## Raspberry Pi OS con escritorio

No copies el entorno Windows: créalo de nuevo en la Raspberry.
Desde la raíz del repositorio:

```bash
sudo apt update
sudo apt install python3-venv python3-pyqt5 python3-gpiozero python3-lgpio i2c-tools
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -r requirements-raspberry.txt
.venv/bin/python ejecutar.py ParteB/PuntoB-1.py
```

Habilita I2C en `sudo raspi-config` y verifica con `i2cdetect -y 1`.
El sensor BMP280 se configura en `0x76`; cambia a `0x77` en
`configuracion.json` si esa es su dirección. No es un BME280.
Ejecuta en la sesión gráfica de Raspberry Pi OS. El usuario necesita acceso
a GPIO e I2C. GPIO Zero selecciona su controlador disponible; consulta
[su documentación de pines](https://gpiozero.readthedocs.io/en/stable/api_pins.html)
si tu modelo requiere configuración adicional.

## Conexiones propuestas

Los números son **BCM**, no posiciones físicas del conector.
Se editan en `configuracion.json`.

| Punto | Conexión |
|---|---|
| B1 | Señales de servo 1 y 2: GPIO12 y GPIO13 |
| B2 | LED rojo GPIO17, verde GPIO27; LEDs de brillo GPIO22 y GPIO23 |
| B3 | BMP280: SDA GPIO2, SCL GPIO3, alimentación compatible a 3,3 V y GND |
| B4 | Entrada GPIO24; resistencia pull-down interna; pulsador entre 3,3 V y GPIO24 |
| B5 | ULN2003 IN1, IN2, IN3, IN4: GPIO5, GPIO6, GPIO16, GPIO26 |

Usa resistencia limitadora en cada LED. Los servos y el motor requieren
alimentación adecuada a sus especificaciones con tierra común a la Raspberry;
no se alimentan desde un GPIO. No apliques 5 V a la entrada GPIO24.
El motor se conecta al ULN2003, no directamente a los pines.

## Comportamiento

- **B1:** escribe 1 o 2; el slider envía 0–180°. Cada servo recuerda su
  consigna. Al conectar hardware no se ordena movimiento hasta mover el
  slider. No hay realimentación de posición. Los pulsos de 1–2 ms son
  valores iniciales que deben calibrarse según el servo; no garantizan
  un recorrido físico exacto de 180° en todos los modelos.
- **B2:** un botón alterna cada LED rojo/verde y adopta su color encendido.
  Los sliders controlan otros dos LEDs mediante PWM.
- **B3:** temperatura BMP280 cada 0,2 s durante el tiempo indicado.
  La lectura corre en un hilo para mantener operativa la ventana. Al
  terminar conserva el último valor. Detener cancela las siguientes lecturas;
  una lectura I2C que ya esté en curso debe retornar antes de cerrar.
- **B4:** consulta la entrada cada 100 ms; alto en rojo, bajo en azul.
  En simulación hay una casilla para cambiar el nivel.
- **B5:** secuencia de medio paso para 28BYJ-48/ULN2003, por defecto
  4096 medios pasos por vuelta, intervalo mínimo de 3 ms. El factor es
  nominal y debe calibrarse para el reductor real. Acepta vueltas
  fraccionarias y signo negativo; redondea al paso más cercano.
  Qt controla la secuencia sin bloquear la interfaz; la duración depende
  del planificador del sistema. El contador representa órdenes enviadas,
  no movimiento medido. Al completar, detener o cerrar libera bobinas.

Los programas liberan sus GPIO al cerrar. B2 original era MicroPython con
pulsadores/ADC; se conserva en `referencia/PuntoB-2-micropython.py`.

## Validación

`pruebas_parte_b.py` comprueba las cinco interfaces, entradas inválidas,
estados LED, lectura temporizada y cancelación, entrada digital, conteo de
pasos y cierre en simulación. Las conexiones físicas y calibración deben
validarse en la Raspberry con los componentes reales.

Referencias:
- [GPIO Zero: salidas y servos](https://gpiozero.readthedocs.io/en/stable/api_output.html)
- [GPIO Zero: entradas digitales](https://gpiozero.readthedocs.io/en/stable/api_input.html)
- [BMP280: Python y CircuitPython](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test)
