"""Identificación estricta de MPU6050/MPU6500 y lectura en unidades SI.

MPU6500: TDK PS-MPU-6500A-01 y RM-MPU-6500A-00.
Rangos fijados: acelerómetro ±2 g; giroscopio ±250 grados/s.
WHO_AM_I es un identificador, NO la dirección I2C.
"""
import math
import struct
import time
from contextlib import contextmanager

class Registros:
    def __init__(self, bus, direccion):
        self.bus = bus
        self.direccion = direccion

    @contextmanager
    def bloqueo(self):
        limite = time.monotonic() + 1
        while not self.bus.try_lock():
            if time.monotonic() >= limite:
                raise TimeoutError("Bus I2C ocupado al leer el sensor.")
            time.sleep(0.005)
        try:
            yield
        finally:
            self.bus.unlock()

    def leer(self, registro, cantidad=1):
        datos = bytearray(cantidad)
        with self.bloqueo():
            self.bus.writeto_then_readfrom(self.direccion, bytes([registro]), datos)
        return datos

    def escribir(self, registro, valor):
        with self.bloqueo():
            self.bus.writeto(self.direccion, bytes([registro, valor]))

class MPU6500:
    modelo = "MPU6500"

    def __init__(self, registros):
        self.registros = registros
        if registros.leer(0x75)[0] != 0x70:
            raise RuntimeError("Identificador incorrecto para MPU6500.")
        registros.escribir(0x6B, 0x80)  # Reinicio.
        time.sleep(0.1)
        limite = time.monotonic() + 1
        while registros.leer(0x6B)[0] & 0x80:
            if time.monotonic() >= limite:
                raise TimeoutError("MPU6500 no terminó el reinicio.")
            time.sleep(0.01)
        registros.escribir(0x6B, 0x01)  # Despertar, reloj automático PLL.
        registros.escribir(0x6C, 0x00)  # Activar los seis ejes.
        configuracion = {0x1A: 0x03, 0x1B: 0x00, 0x1C: 0x00,
                         0x1D: 0x03, 0x19: 0x04}
        for registro, valor in configuracion.items():
            registros.escribir(registro, valor)
        time.sleep(0.1)
        for registro, valor in configuracion.items():
            if registros.leer(registro)[0] != valor:
                raise RuntimeError(f"MPU6500 no confirmó configuración en {registro:#04x}.")

    def leer(self):
        # Una lectura contigua: aceleración XYZ, temperatura y giro XYZ.
        ax, ay, az, temp, gx, gy, gz = struct.unpack(">7h", self.registros.leer(0x3B, 14))
        return {"aceleracion": tuple(v * 9.80665 / 16384 for v in (ax, ay, az)),
                "giro": tuple(math.radians(v / 131) for v in (gx, gy, gz)),
                "temperatura": temp / 333.87 + 21.0}

class MPU6050:
    modelo = "MPU6050"

    def __init__(self, bus, direccion):
        import adafruit_mpu6050
        self.sensor = adafruit_mpu6050.MPU6050(bus, address=direccion)

    def leer(self):
        return {"aceleracion": self.sensor.acceleration,
                "giro": self.sensor.gyro, "temperatura": self.sensor.temperature}

def abrir_mpu(bus, direccion):
    registros = Registros(bus, direccion)
    identidad = registros.leer(0x75)[0]
    if identidad == 0x70:
        return MPU6500(registros)
    if identidad == 0x68:
        return MPU6050(bus, direccion)
    raise RuntimeError(f"WHO_AM_I={identidad:#04x} no soportado. "
                       "Se espera 0x68 (MPU6050) o 0x70 (MPU6500).")
