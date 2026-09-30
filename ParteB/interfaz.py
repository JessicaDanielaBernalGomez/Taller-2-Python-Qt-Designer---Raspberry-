"""Controladores Qt de los cinco ejercicios de la parte B."""
import math
import sys
import threading
import time
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from hardware import CONFIG, Raspberry, Simulador

CARPETA = Path(__file__).resolve().parent

def numero(texto, nombre, minimo, maximo):
    try:
        valor = float(texto.strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"{nombre}: ingresa un número válido.")
    if not math.isfinite(valor) or not minimo <= valor <= maximo:
        raise ValueError(f"{nombre}: debe estar entre {minimo} y {maximo}.")
    return valor

class LecturaI2C(QtCore.QThread):
    lectura = QtCore.pyqtSignal(object, float)
    fallo = QtCore.pyqtSignal(str)

    def __init__(self, hardware, duracion, parent):
        super().__init__(parent)
        self.hardware = hardware
        self.duracion = duracion
        self.cancelado = threading.Event()

    def run(self):
        inicio = time.monotonic()
        try:
            while not self.cancelado.is_set():
                transcurrido = time.monotonic() - inicio
                if transcurrido >= self.duracion:
                    break
                valor = self.hardware.sensor()
                transcurrido = time.monotonic() - inicio
                if transcurrido >= self.duracion or self.cancelado.is_set():
                    break
                self.lectura.emit(valor, transcurrido)
                self.cancelado.wait(min(0.2, self.duracion - transcurrido))
        except Exception as exc:
            self.fallo.emit(str(exc))

class Ventana(QtWidgets.QWidget):
    def __init__(self, punto):
        super().__init__()
        self.punto = punto
        self.hw = None
        self.trabajador = None
        self.cierre_pendiente = False
        self.error_lectura = False
        self.angulos = [90, 90]
        self.leds = [False, False]
        self.realizados = 0
        uic.loadUi(str(CARPETA / f"PuntoB-{punto}.ui"), self)
        logo = QtGui.QPixmap(str(CARPETA.parent / "logo_universidad.png"))
        self.logo.setPixmap(logo.scaled(130, 70, QtCore.Qt.KeepAspectRatio,
                                      QtCore.Qt.SmoothTransformation))
        self.conectar.clicked.connect(self.cambiar_conexion)
        self.timer = QtCore.QTimer(self)
        if punto == 1:
            self.selector.textChanged.connect(self.seleccionar_servo)
            self.angulo.valueChanged.connect(self.mover_servo)
        elif punto == 2:
            self.led1.clicked.connect(lambda: self.alternar_led(0))
            self.led2.clicked.connect(lambda: self.alternar_led(1))
            self.brillo1.valueChanged.connect(lambda v: self.cambiar_brillo(0, v))
            self.brillo2.valueChanged.connect(lambda v: self.cambiar_brillo(1, v))
        elif punto == 3:
            self.iniciar.clicked.connect(self.iniciar_lectura)
            self.detener.clicked.connect(self.detener_lectura)
            self.detener.setEnabled(False)
        elif punto == 4:
            self.simulado.toggled.connect(self.cambiar_entrada)
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.leer_digital)
            self.timer.start()
        elif punto == 5:
            self.iniciar.clicked.connect(self.iniciar_motor)
            self.detener.clicked.connect(self.detener_motor)
            self.detener.setEnabled(False)
            self.timer.setTimerType(QtCore.Qt.PreciseTimer)
            self.timer.setInterval(CONFIG["motor_intervalo_ms"])
            self.timer.timeout.connect(self.paso_motor)
        self.cambiar_conexion()

    def informar_error(self, exc):
        self.estado.setText(f"Error: {exc}")

    def cambiar_conexion(self):
        if self.hw is not None:
            self.hw.close()
        self.hw = None
        self.controles.setEnabled(False)
        try:
            real = self.modo.currentIndex() == 1
            self.hw = Raspberry(self.punto) if real else Simulador(self.punto)
            self.modo_activo.setText("RASPBERRY PI: hardware conectado" if real
                                    else "SIMULACIÓN: sin conexión a GPIO")
            self.controles.setEnabled(True)
            self.estado.setText("Listo.")
            if self.punto == 3 and real:
                self.modo_activo.setText(f"RASPBERRY PI: MPU6050 conectado en {self.hw.direccion:#04x}")
            if self.punto == 1:
                self.angulos = [90, 90]
                self.seleccionar_servo()
            elif self.punto == 2:
                self.leds = [False, False]
                for i, slider in enumerate((self.brillo1, self.brillo2)):
                    slider.setValue(0)
                    self.actualizar_led(i)
                    getattr(self, f"valor_brillo{i+1}").setText("Brillo: 0 %")
            elif self.punto == 4:
                self.simulado.setVisible(not real)
                self.simulado.setChecked(False)
                self.leer_digital()
        except Exception as exc:
            self.modo_activo.setText("SIN CONEXIÓN")
            self.informar_error(exc)

    def bloquear_conexion(self, ocupado):
        self.modo.setEnabled(not ocupado)
        self.conectar.setEnabled(not ocupado)

    def indice_servo(self):
        texto = self.selector.text().strip()
        if texto not in ("1", "2"):
            raise ValueError("Escribe 1 o 2 para seleccionar el servomotor.")
        return int(texto) - 1

    def seleccionar_servo(self):
        try:
            indice = self.indice_servo()
            self.angulo.setEnabled(True)
            self.angulo.blockSignals(True)
            self.angulo.setValue(self.angulos[indice])
            self.angulo.blockSignals(False)
            self.valor_angulo.setText(f"Servo {indice+1}: {self.angulos[indice]}° (consigna)")
            self.estado.setText("Mueve el slider para enviar el ángulo al servo seleccionado.")
        except ValueError as exc:
            self.angulo.setEnabled(False)
            self.informar_error(exc)

    def mover_servo(self, valor):
        try:
            indice = self.indice_servo()
            self.hw.servo(indice, valor)
            self.angulos[indice] = valor
            self.valor_angulo.setText(f"Servo {indice+1}: {valor}° (consigna)")
        except Exception as exc:
            self.informar_error(exc)

    def actualizar_led(self, indice):
        boton = (self.led1, self.led2)[indice]
        color = ("#d32f2f", "#15803d")[indice] if self.leds[indice] else "#4b5563"
        nombre = ("rojo", "verde")[indice]
        estado = "encendido" if self.leds[indice] else "apagado"
        boton.setText(f"LED {indice+1} ({nombre}): {estado}")
        boton.setStyleSheet(f"background-color: {color}; color: white; padding: 14px;")

    def alternar_led(self, indice):
        try:
            nuevo = not self.leds[indice]
            self.hw.led(indice, nuevo)
            self.leds[indice] = nuevo
            self.actualizar_led(indice)
        except Exception as exc:
            self.informar_error(exc)

    def cambiar_brillo(self, indice, valor):
        try:
            self.hw.brillo(indice, valor / 100)
            getattr(self, f"valor_brillo{indice+1}").setText(f"Brillo: {valor} %")
        except Exception as exc:
            self.informar_error(exc)

    def iniciar_lectura(self):
        if self.trabajador is not None:
            return
        try:
            duracion = numero(self.duracion.text(), "Duración (s)", 0.1, 3600)
        except ValueError as exc:
            self.informar_error(exc)
            return
        self.error_lectura = False
        self.bloquear_conexion(True)
        self.iniciar.setEnabled(False)
        self.detener.setEnabled(True)
        self.duracion.setEnabled(False)
        self.lectura.setText("Esperando lectura...")
        self.estado.setText("Leyendo sensor.")
        self.trabajador = LecturaI2C(self.hw, duracion, self)
        self.trabajador.lectura.connect(self.mostrar_lectura)
        self.trabajador.fallo.connect(self.fallo_lectura)
        self.trabajador.finished.connect(self.fin_lectura)
        self.trabajador.start()

    def mostrar_lectura(self, valor, transcurrido):
        ax, ay, az = valor["aceleracion"]
        gx, gy, gz = valor["giro"]
        self.lectura.setText(
            f"Aceleración (m/s²): X={ax:.2f}  Y={ay:.2f}  Z={az:.2f}\n"
            f"Giroscopio (rad/s): X={gx:.3f}  Y={gy:.3f}  Z={gz:.3f}\n"
            f"Temperatura: {valor['temperatura']:.2f} °C")
        self.estado.setText(f"Lectura activa: {transcurrido:.1f} s")

    def fallo_lectura(self, mensaje):
        self.error_lectura = True
        self.informar_error(mensaje)

    def detener_lectura(self):
        if self.trabajador is not None:
            self.trabajador.cancelado.set()
            self.estado.setText("Deteniendo lectura...")

    def fin_lectura(self):
        cancelado = self.trabajador.cancelado.is_set()
        self.trabajador.deleteLater()
        self.trabajador = None
        self.bloquear_conexion(False)
        self.iniciar.setEnabled(True)
        self.detener.setEnabled(False)
        self.duracion.setEnabled(True)
        if not self.error_lectura:
            self.estado.setText("Lectura detenida." if cancelado else "Tiempo finalizado. Última lectura conservada.")
        if self.cierre_pendiente:
            self.close()

    def cambiar_entrada(self, alto):
        if isinstance(self.hw, Simulador):
            self.hw.entrada = alto
            self.leer_digital()

    def leer_digital(self):
        if self.hw is None:
            return
        try:
            alto = self.hw.digital()
            self.nivel.setText("alto" if alto else "bajo")
            color = "#c62828" if alto else "#1565c0"
            self.nivel.setStyleSheet(f"background-color: {color}; color: white; font-size: 28px; padding: 20px;")
        except Exception as exc:
            self.nivel.setText("Sin lectura")
            self.nivel.setStyleSheet("")
            self.informar_error(exc)

    def iniciar_motor(self):
        try:
            vueltas = numero(self.vueltas.text(), "Vueltas", -100, 100)
            pasos = round(abs(vueltas) * CONFIG["motor_pasos_vuelta"])
            if pasos == 0:
                raise ValueError("La cantidad debe corresponder al menos a un paso.")
        except ValueError as exc:
            self.informar_error(exc)
            return
        self.objetivo = pasos
        self.realizados = 0
        self.direccion = 1 if vueltas > 0 else -1
        self.progreso.setValue(0)
        self.bloquear_conexion(True)
        self.iniciar.setEnabled(False)
        self.vueltas.setEnabled(False)
        self.detener.setEnabled(True)
        self.estado.setText(f"Moviendo: 0 / {pasos} medios pasos.")
        self.timer.start()

    def paso_motor(self):
        try:
            self.hw.paso(self.direccion)
            self.realizados += 1
            self.progreso.setValue(round(100 * self.realizados / self.objetivo))
            if self.realizados % 32 == 0:
                self.estado.setText(f"Moviendo: {self.realizados} / {self.objetivo} medios pasos.")
            if self.realizados >= self.objetivo:
                self.detener_motor(completo=True)
        except Exception as exc:
            self.detener_motor()
            self.informar_error(exc)

    def detener_motor(self, checked=False, completo=False):
        self.timer.stop()
        try:
            if self.hw is not None:
                self.hw.detener_motor()
        except Exception as exc:
            self.informar_error(exc)
        else:
            texto = "Completado" if completo else "Detenido"
            self.estado.setText(f"{texto}: {self.realizados} medios pasos enviados.")
        self.bloquear_conexion(False)
        self.iniciar.setEnabled(True)
        self.vueltas.setEnabled(True)
        self.detener.setEnabled(False)

    def closeEvent(self, event):
        if self.trabajador is not None:
            self.cierre_pendiente = True
            self.detener_lectura()
            event.ignore()
            return
        self.timer.stop()
        if self.hw is not None:
            self.hw.close()
            self.hw = None
        event.accept()

def ejecutar(punto):
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana(punto)
    ventana.show()
    sys.exit(app.exec_())
