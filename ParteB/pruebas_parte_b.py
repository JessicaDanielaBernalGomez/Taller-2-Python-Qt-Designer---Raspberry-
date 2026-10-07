"""Pruebas funcionales de las interfaces, sin GPIO real ni ventanas visibles."""
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import sys
import math
import time
from unittest.mock import patch
import interfaz
from PyQt5 import QtCore, QtWidgets
from interfaz import Ventana
from hardware import CONFIG, validar_pines, detectar_mpu

class HardwarePrueba:
    def __init__(self, punto):
        self.modelo = "MPU6500"
        self.direccion = 0x68
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
        t = time.monotonic()
        return {"aceleracion": (math.sin(t), 0.2 * math.cos(t), 9.81),
                "giro": (0.01 * math.sin(t), 0.02 * math.cos(t), 0.0),
                "temperatura": 24 + math.sin(t / 5)}

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


app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

def esperar(ms):
    bucle = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(ms, bucle.quit)
    bucle.exec_()

def probar():
    validar_pines(CONFIG)
    conflicto = dict(CONFIG, leds=[14, 27])
    try:
        validar_pines(conflicto)
    except ValueError:
        pass
    else:
        raise AssertionError("Se permitió el pin físico8 del ventilador.")
    class Bus:
        def __init__(self, direcciones):
            self.direcciones = direcciones
            self.liberado = False
        def try_lock(self):
            return True
        def scan(self):
            return self.direcciones
        def unlock(self):
            self.liberado = True
    for direccion in (0x68, 0x69):
        bus = Bus([direccion])
        assert detectar_mpu(bus, "auto") == direccion and bus.liberado
    for direcciones in ([], [0x76], [0x68, 0x69]):
        try:
            detectar_mpu(Bus(direcciones), "auto")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Detección ausente o ambigua aceptada.")
    assert detectar_mpu(Bus([0x68, 0x69]), "0x69") == 0x69
    ventanas = []
    try:
        for punto in range(1, 6):
            w = Ventana(punto)
            ventanas.append(w)
            w.show()
            app.processEvents()
            assert not w.logo.pixmap().isNull()
            assert "RASPBERRY PI" in w.estado_conexion.text()
            assert not hasattr(w, "modo")
            assert not hasattr(w, "simulado")
        b1, b2, b3, b4, b5 = ventanas

        b1.angulo.setValue(180)
        b1.selector.setText("2")
        b1.angulo.setValue(0)
        assert b1.hw.angulos == [180, 0]
        b1.selector.setText("1")
        assert b1.angulo.value() == 180
        b1.selector.setText("3")
        assert not b1.angulo.isEnabled()
        assert not hasattr(b1, "liberar_servos")

        b2.led1.click()
        b2.led2.click()
        assert b2.hw.leds == [True, True]
        assert "#d32f2f" in b2.led1.styleSheet()
        assert "#15803d" in b2.led2.styleSheet()
        b2.led1.click()
        assert b2.hw.leds == [False, True]
        b2.brillo1.setValue(25)
        b2.brillo2.setValue(75)
        assert b2.hw.brillos == [0.25, 0.75]

        b3.duracion.setText("nan")
        b3.iniciar.click()
        assert b3.trabajador is None
        b3.duracion.setText("0,3")
        b3.iniciar.click()
        esperar(500)
        assert b3.trabajador is None
        assert "Temperatura:" in b3.lectura.text()
        assert "Aceleración (m/s²)" in b3.lectura.text()
        assert "Giroscopio (rad/s)" in b3.lectura.text()
        assert "Tiempo finalizado" in b3.estado.text()
        ultima = b3.lectura.text()
        esperar(100)
        assert b3.lectura.text() == ultima
        b3.duracion.setText("10")
        b3.iniciar.click()
        assert not b3.conectar.isEnabled()
        b3.detener.click()
        esperar(100)
        assert b3.trabajador is None
        assert "detenida" in b3.estado.text()

        b4.hw.entrada = True
        b4.leer_digital()
        assert b4.nivel.text() == "alto"
        assert "#c62828" in b4.nivel.styleSheet()
        b4.hw.entrada = False
        b4.leer_digital()
        assert b4.nivel.text() == "bajo"
        assert "#1565c0" in b4.nivel.styleSheet()

        for vueltas, pasos in (("0.5", 2048), ("1", 4096), ("2,5", 10240), ("-0.5", 2048)):
            antes = b5.hw.pasos
            b5.vueltas.setText(vueltas)
            b5.iniciar.click()
            assert b5.objetivo == pasos
            b5.timer.stop()  # Acelerar exclusivamente la prueba del conteo.
            for _ in range(pasos):
                b5.paso_motor()
            assert b5.realizados == pasos
            assert b5.progreso.value() == 100
            assert b5.hw.pasos - antes == (-pasos if vueltas.startswith("-") else pasos)
            assert not b5.hw.energizado
        for invalido in ("0", "nan", "inf", "texto"):
            b5.vueltas.setText(invalido)
            b5.iniciar.click()
            assert not b5.timer.isActive()
            assert b5.estado.text().startswith("Error:")
        b5.vueltas.setText("1")
        b5.iniciar.click()
        b5.timer.stop()
        b5.paso_motor()
        b5.detener.click()
        assert not b5.hw.energizado and b5.realizados == 1

        # Error de lectura: no dejar botones bloqueados ni ocultar el error.
        def fallo():
            raise OSError("Sensor desconectado")
        b3.hw.sensor = fallo
        b3.iniciar.click()
        esperar(100)
        assert b3.trabajador is None
        assert "Sensor desconectado" in b3.estado.text()
        assert b3.iniciar.isEnabled()

        # Un cierre durante lectura espera al hilo antes de liberar el bus.
        b3.cambiar_conexion()
        b3.iniciar.click()
        b3.close()
        esperar(100)
        assert b3.trabajador is None and b3.hw is None

        led_backend = b2.hw
        b2.close()
        assert led_backend.leds == [False, False]
        assert led_backend.brillos == [0, 0]
        print("OK: cinco UI, servos, LEDs/PWM, I2C, errores, entrada digital, vueltas y cierre.")
    finally:
        for w in ventanas:
            w.close()
        esperar(100)

if __name__ == "__main__":
    with patch.object(interfaz, "Raspberry", HardwarePrueba):
        probar()
