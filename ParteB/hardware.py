"""Adaptadores de simulación y Raspberry Pi. Numeración de pines BCM."""
import json
import math
import time
from pathlib import Path

CONFIG = json.loads(Path(__file__).with_name("configuracion.json").read_text(encoding="utf-8"))
# ===== CONEXIONES FÍSICAS / VENTILADOR: NO MODIFICAR SIN REVISAR CABLEADO =====
# Ventilador reservado: físico 4 (5V), físico 6 (GND), físico 8 (BCM14).
# GND de TODOS los componentes del taller: físico 9.
# BCM12/13 -> físicos32/33: servos.
# BCM17/27 -> físicos11/13: LEDs; BCM22/23 -> físicos15/16: PWM.
# MPU6050/MPU6500: SDA BCM2 físico3; SCL BCM3 físico5; VCC 3,3V físico1; GND físico9.
# Entrada BCM24 -> físico18.
# ULN2003 IN1..IN4: BCM5/6/16/26 -> físicos29/31/36/37.
# IMPORTANTE: BCM6 NO es el pin físico6 del ventilador.
BCM_A_FISICO = {2:3, 3:5, 4:7, 14:8, 15:10, 17:11, 18:12, 27:13,
               22:15, 23:16, 24:18, 10:19, 9:21, 25:22, 11:23,
               8:24, 7:26, 0:27, 1:28, 5:29, 6:31, 12:32,
               13:33, 19:35, 16:36, 26:37, 20:38, 21:40}
VENTILADOR_FISICOS = {4, 6, 8}

def validar_pines(config):
    pines = (config["servos"] + config["leds"] + config["leds_pwm"]
             + [config["entrada"]] + config["motor"] + [2, 3])
    for pin in pines:
        if pin not in BCM_A_FISICO:
            raise ValueError(f"GPIO BCM no válido: {pin}")
        if BCM_A_FISICO[pin] in VENTILADOR_FISICOS:
            raise ValueError(f"GPIO{pin} ocupa el pin físico {BCM_A_FISICO[pin]} reservado al ventilador.")
    if len(pines) != len(set(pines)):
        raise ValueError("Hay GPIO repetidos entre los componentes.")
    if config["gnd_componentes_pin_fisico"] not in (9,14,20,25,30,34,39):
        raise ValueError("Elige un GND físico libre; el pin6 está reservado al ventilador.")

def detectar_mpu(bus, direccion):
    limite = time.monotonic() + 1
    while not bus.try_lock():
        if time.monotonic() > limite:
            raise RuntimeError("Bus I2C ocupado; cierra otros programas y vuelve a conectar.")
        time.sleep(0.01)
    try:
        disponibles = bus.scan()
    finally:
        bus.unlock()
    if direccion != "auto":
        elegido = int(direccion, 0)
        if elegido not in (0x68, 0x69):
            raise ValueError("MPU6050/MPU6500 usa 0x68 o 0x69; configura i2c_direccion como auto.")
        candidatos = [elegido] if elegido in disponibles else []
    else:
        candidatos = [d for d in (0x68, 0x69) if d in disponibles]
    if len(candidatos) > 1:
        raise RuntimeError("Hay dispositivos en 0x68 y 0x69; elige uno en configuracion.json.")
    if not candidatos:
        encontrados = ", ".join(hex(d) for d in disponibles) or "ninguno"
        raise RuntimeError("MPU6050/MPU6500 no detectado en la dirección esperada. "
                           f"I2C detectados: {encontrados}. Revisa I2C habilitado, SDA físico3, "
                           "SCL físico5, GND físico9 y AD0. Ejecuta i2cdetect -y 1.")
    return candidatos[0]

SECUENCIA = ((1,0,0,0), (1,1,0,0), (0,1,0,0), (0,1,1,0),
             (0,0,1,0), (0,0,1,1), (0,0,0,1), (1,0,0,1))

class Raspberry:
    def __init__(self, punto):
        validar_pines(CONFIG)
        self.dispositivos = []
        self.bus = None
        self.bobinas = []
        self.fase = -1
        try:
            if punto == 3:
                try:
                    import board
                    from sensores_mpu import abrir_mpu
                except ImportError as exc:
                    raise RuntimeError("Falta el controlador MPU6050/MPU6500. Ejecuta: "
                                       ".venv/bin/python -m pip install -r requirements-raspberry.txt") from exc
                self.bus = board.I2C()
                self.direccion = detectar_mpu(self.bus, CONFIG["i2c_direccion"])
                try:
                    self.mpu = abrir_mpu(self.bus, self.direccion)
                    self.modelo = self.mpu.modelo
                    self.sensor()
                except Exception as exc:
                    raise RuntimeError(f"Dispositivo en {self.direccion:#04x}, pero falla "
                                       f"la identificación/lectura MPU6050/MPU6500: {exc}") from exc
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
        return self.mpu.leer()

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
