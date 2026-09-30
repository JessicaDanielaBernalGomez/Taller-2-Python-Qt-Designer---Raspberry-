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
El MPU6050 se detecta automáticamente en `0x68` o `0x69`.
AD0 a GND selecciona 0x68; AD0 a 3,3 V selecciona 0x69.
Si aparecen ambas direcciones, selecciona explícitamente una en
`i2c_direccion` de `configuracion.json`. Detectar una dirección no basta:
el controlador verifica también la identidad del sensor.
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
| B3 | MPU6050: SDA GPIO2, SCL GPIO3, VCC compatible a 3,3 V físico1 y GND físico9 |
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
- **B3:** aceleración (m/s²), giro (rad/s) y temperatura (°C) MPU6050 cada 0,2 s durante el tiempo indicado.
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
- [MPU6050: Python y CircuitPython](https://docs.circuitpython.org/projects/mpu6050/en/latest/api.html)

## Pines físicos reservados al ventilador

**No conectar componentes del taller a los pines físicos 4, 6 u 8.**
Son 5 V, GND y GPIO14, respectivamente. Usar **GND físico9** para sensores,
LEDs, servos y tierra común de la fuente externa. Ninguna señal actual
usa GPIO14. GPIO6 del motor corresponde al físico31: no es un conflicto.

El mapa BCM/físico y las reservas están al principio de `hardware.py`.
`validar_pines` rechaza GPIO14, duplicados y una tierra reservada antes
de abrir dispositivos. `configuracion.json` contiene los pines ajustables.

| Función | BCM | Pin físico |
|---|---|---|
| Servos 1 / 2 | 12 / 13 | 32 / 33 |
| LED rojo / verde | 17 / 27 | 11 / 13 |
| LEDs de brillo | 22 / 23 | 15 / 16 |
| MPU6050 SDA / SCL | 2 / 3 | 3 / 5 |
| Entrada digital | 24 | 18 |
| ULN2003 IN1 / IN2 / IN3 / IN4 | 5 / 6 / 16 / 26 | 29 / 31 / 36 / 37 |
| Tierra común | GND | 9 |

MPU6050: para un módulo compatible, VCC a 3,3 V físico1 y GND físico9.
INT, XDA y XCL no se utilizan. No llevar señales I2C a 5 V.
Tras actualizar los archivos en Raspberry, ejecutar:
```bash
.venv/bin/python -m pip install -r requirements-raspberry.txt
i2cdetect -y 1
.venv/bin/python ejecutar.py ParteB/PuntoB-3.py
```
Seleccionar hardware real y conectar. Si el escaneo no muestra 68 o 69,
revisar alimentación, SDA/SCL, AD0 e I2C habilitado. Si aparece una dirección
pero falla la identificación, revisar que el componente sea MPU6050.

## Sensor con WHO_AM_I = 0x70

0x70 identifica un MPU6500. La dirección I2C sigue siendo 0x68 o 0x69;
no poner 0x70 como dirección en configuracion.json.
El programa selecciona el controlador según el registro 0x75:
0x68 -> MPU6050 (Adafruit), 0x70 -> MPU6500 (sensores_mpu.py).
Otros identificadores se rechazan. La interfaz muestra el modelo detectado.

El MPU6500 usa ±2 g, ±250 grados/s y temperatura raw/333.87 + 21 °C.
La salida se expresa en m/s², rad/s y °C. No se elimina gravedad ni se
calibran offsets. En reposo, la magnitud de la aceleración ronda 9,81 m/s²
y el giro debe estar cerca de cero (con sesgo y ruido propios del sensor).
Se comprueba la configuración escrita y se limita la espera de reinicio.

Copiar también sensores_mpu.py al actualizar hardware.py, interfaz.py
y PuntoB-3.ui en la Raspberry. Se utiliza Blinka ya incluido en los requisitos;
no es necesario modificar la librería instalada del MPU6050.

Referencia: https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/mpu-6500-datasheet2.pdf
