"""Adaptadores de simulación y Raspberry Pi. Numeración de pines BCM."""
import json
import math
import time
from pathlib import Path

CONFIG = json.loads(Path(__file__).with_name("configuracion.json").read_text(encoding="utf-8"))
SECUENCIA = ((1,0,0,0), (1,1,0,0), (0,1,0,0), (0,1,1,0),
             (0,0,1,0), (0,0,1,1), (0,0,0,1), (1,0,0,1))

class Simulador:
    def __init__(self, punto):
        self.angulos = [90, 90]
        self.leds = [False, False]
        self.brillos = [0, 0]
        self.entrada = False
        self.pasos = 0
        self.energizado = False

    def servo(self, indice, angulo):
        self.angulos[indice] = angulo

    def led(self, indice, estado):
        self.leds[indice] = estado

    def brillo(self, indice, valor):
        self.brillos[indice] = valor

    def sensor(self):
        return 24 + math.sin(time.monotonic() / 5)

    def digital(self):
        return self.entrada

    def paso(self, direccion):
        self.pasos += direccion
        self.energizado = True

    def detener_motor(self):
        self.energizado = False

    def close(self):
        self.leds = [False, False]
        self.brillos = [0, 0]
        self.detener_motor()


class Raspberry:
    def __init__(self, punto):
        self.dispositivos = []
        self.bus = None
        self.bobinas = []
        self.fase = -1
        try:
            if punto == 3:
                import board
                import adafruit_bmp280
                self.bus = board.I2C()
                self.bmp = adafruit_bmp280.Adafruit_BMP280_I2C(
                    self.bus, address=int(CONFIG["i2c_direccion"], 0))
                # Verifica que el sensor responda durante la conexión.
                _ = self.bmp.temperature
                return
            from gpiozero import AngularServo, LED, PWMLED, DigitalInputDevice, DigitalOutputDevice
            if punto == 1:
                self.servos = []
                for pin in CONFIG["servos"]:
                    servo = AngularServo(pin, min_angle=0, max_angle=180,
                        initial_angle=None,
                        min_pulse_width=CONFIG["servo_pulso_min_ms"] / 1000,
                        max_pulse_width=CONFIG["servo_pulso_max_ms"] / 1000)
                    self.dispositivos.append(servo)
                    self.servos.append(servo)
            elif punto == 2:
                self.leds = []
                self.pwm = []
                for pin in CONFIG["leds"]:
                    led = LED(pin, initial_value=False)
                    self.dispositivos.append(led)
                    self.leds.append(led)
                for pin in CONFIG["leds_pwm"]:
                    led = PWMLED(pin, initial_value=0, frequency=1000)
                    self.dispositivos.append(led)
                    self.pwm.append(led)
            elif punto == 4:
                self.entrada = DigitalInputDevice(CONFIG["entrada"], pull_up=False)
                self.dispositivos.append(self.entrada)
            elif punto == 5:
                for pin in CONFIG["motor"]:
                    salida = DigitalOutputDevice(pin, initial_value=False)
                    self.dispositivos.append(salida)
                    self.bobinas.append(salida)
        except Exception:
            self.close()
            raise

    def servo(self, indice, angulo):
        self.servos[indice].angle = angulo

    def led(self, indice, estado):
        self.leds[indice].value = estado

    def brillo(self, indice, valor):
        self.pwm[indice].value = valor

    def sensor(self):
        return self.bmp.temperature

    def digital(self):
        return bool(self.entrada.value)

    def paso(self, direccion):
        self.fase = (self.fase + direccion) % len(SECUENCIA)
        for salida, valor in zip(self.bobinas, SECUENCIA[self.fase]):
            salida.value = valor

    def detener_motor(self):
        for salida in self.bobinas:
            salida.off()

    def close(self):
        # Cerrar también los recursos creados antes de un fallo de conexión.
        for dispositivo in reversed(self.dispositivos):
            try:
                if hasattr(dispositivo, "detach"):
                    dispositivo.detach()
                elif hasattr(dispositivo, "off"):
                    dispositivo.off()
                dispositivo.close()
            except Exception:
                pass
        self.dispositivos.clear()
        if self.bus is not None:
            self.bus.deinit()
            self.bus = None
