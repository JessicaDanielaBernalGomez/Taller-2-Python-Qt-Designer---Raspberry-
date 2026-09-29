import math
from collections import deque
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 760)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(20, 8, 60, 50))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")
        _pixmap_logo = QtGui.QPixmap("logo_universidad.png")
        if not _pixmap_logo.isNull():
            self.label_logo.setPixmap(_pixmap_logo)
        else:
            self.label_logo.setText("[LOGO]")
            self.label_logo.setAlignment(QtCore.Qt.AlignCenter)
            self.label_logo.setStyleSheet("border: 1px solid gray; font-size: 8pt; color: gray;")

        self.label_universidad = QtWidgets.QLabel(self.centralwidget)
        self.label_universidad.setGeometry(QtCore.QRect(90, 8, 820, 20))
        font_universidad = QtGui.QFont()
        font_universidad.setPointSize(10)
        font_universidad.setBold(True)
        self.label_universidad.setFont(font_universidad)
        self.label_universidad.setObjectName("label_universidad")

        self.label_integrantes = QtWidgets.QLabel(self.centralwidget)
        self.label_integrantes.setGeometry(QtCore.QRect(90, 28, 820, 20))
        font_integrantes = QtGui.QFont()
        font_integrantes.setPointSize(9)
        self.label_integrantes.setFont(font_integrantes)
        self.label_integrantes.setObjectName("label_integrantes")

        self.linea_separadora = QtWidgets.QFrame(self.centralwidget)
        self.linea_separadora.setGeometry(QtCore.QRect(20, 54, 900, 2))
        self.linea_separadora.setFrameShape(QtWidgets.QFrame.HLine)
        self.linea_separadora.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_separadora.setObjectName("linea_separadora")


        font6 = QtGui.QFont()
        font6.setPointSize(11)
        font6.setBold(True)

        self.label_rc_titulo = QtWidgets.QLabel(self.centralwidget)
        self.label_rc_titulo.setGeometry(QtCore.QRect(20, 72, 700, 25))
        self.label_rc_titulo.setFont(font6)
        self.label_rc_titulo.setObjectName("label_rc_titulo")

        font_slider = QtGui.QFont()
        font_slider.setPointSize(10)

        # --- Slider Resistencia (R) ---
        self.label_valor_r = QtWidgets.QLabel(self.centralwidget)
        self.label_valor_r.setGeometry(QtCore.QRect(20, 108, 220, 25))
        self.label_valor_r.setFont(font_slider)
        self.label_valor_r.setObjectName("label_valor_r")

        self.slider_r = QtWidgets.QSlider(self.centralwidget)
        self.slider_r.setGeometry(QtCore.QRect(20, 135, 380, 25))
        self.slider_r.setOrientation(QtCore.Qt.Horizontal)
        self.slider_r.setMinimum(100)
        self.slider_r.setMaximum(10000)
        self.slider_r.setSingleStep(50)
        self.slider_r.setValue(1000)
        self.slider_r.setObjectName("slider_r")

        # --- Slider Capacitancia (C) ---
        self.label_valor_c = QtWidgets.QLabel(self.centralwidget)
        self.label_valor_c.setGeometry(QtCore.QRect(430, 108, 220, 25))
        self.label_valor_c.setFont(font_slider)
        self.label_valor_c.setObjectName("label_valor_c")

        self.slider_c = QtWidgets.QSlider(self.centralwidget)
        self.slider_c.setGeometry(QtCore.QRect(430, 135, 240, 25))
        self.slider_c.setOrientation(QtCore.Qt.Horizontal)
        self.slider_c.setMinimum(1)
        self.slider_c.setMaximum(1000)
        self.slider_c.setValue(100)
        self.slider_c.setObjectName("slider_c")

        # --- Slider Voltaje (V) ---
        self.label_valor_v = QtWidgets.QLabel(self.centralwidget)
        self.label_valor_v.setGeometry(QtCore.QRect(700, 108, 180, 25))
        self.label_valor_v.setFont(font_slider)
        self.label_valor_v.setObjectName("label_valor_v")

        self.slider_v = QtWidgets.QSlider(self.centralwidget)
        self.slider_v.setGeometry(QtCore.QRect(700, 135, 190, 25))
        self.slider_v.setOrientation(QtCore.Qt.Horizontal)
        self.slider_v.setMinimum(1)
        self.slider_v.setMaximum(24)
        self.slider_v.setValue(12)
        self.slider_v.setObjectName("slider_v")

        # --- Botón reiniciar simulación ---
        self.pushButton_reiniciar_rc = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reiniciar_rc.setGeometry(QtCore.QRect(20, 172, 160, 35))
        font_boton_rc = QtGui.QFont()
        font_boton_rc.setPointSize(10)
        self.pushButton_reiniciar_rc.setFont(font_boton_rc)
        self.pushButton_reiniciar_rc.setObjectName("pushButton_reiniciar_rc")

        # --- Estado (cargando / descargando) ---
        self.label_estado_rc = QtWidgets.QLabel(self.centralwidget)
        self.label_estado_rc.setGeometry(QtCore.QRect(200, 172, 690, 35))
        font_estado_rc = QtGui.QFont()
        font_estado_rc.setPointSize(11)
        font_estado_rc.setBold(True)
        self.label_estado_rc.setFont(font_estado_rc)
        self.label_estado_rc.setObjectName("label_estado_rc")

        # --- Objeto tipo axes: gráfica en tiempo real de Vc(t) ---
        self.figure_rc = Figure(figsize=(5, 4))
        self.canvas_rc = FigureCanvas(self.figure_rc)
        self.canvas_rc.setParent(self.centralwidget)
        self.canvas_rc.setGeometry(QtCore.QRect(20, 220, 900, 500))
        self.axes_rc = self.figure_rc.add_subplot(111)
        self.axes_rc.set_xlabel("Tiempo (s)")
        self.axes_rc.set_ylabel("Voltaje en el condensador Vc (V)")
        self.axes_rc.grid(True)
        (self.linea_rc,) = self.axes_rc.plot([], [], color="tab:blue", linewidth=1.8)
        self.linea_v_fuente = self.axes_rc.axhline(0, color="red", linestyle="--", linewidth=1.0)
        self.figure_rc.tight_layout()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ---------- Conexiones ----------
        self.slider_r.valueChanged.connect(self._cambiar_parametros_rc)
        self.slider_c.valueChanged.connect(self._cambiar_parametros_rc)
        self.slider_v.valueChanged.connect(self._cambiar_parametros_rc)
        self.pushButton_reiniciar_rc.clicked.connect(self.reiniciar_rc)

        self._rc_reloj = QtCore.QElapsedTimer()
        self._rc_timer = QtCore.QTimer(MainWindow)
        self._rc_timer.setInterval(40)
        self._rc_timer.timeout.connect(self._avanzar_rc)
        MainWindow.destroyed.connect(self._rc_timer.stop)
        self.reiniciar_rc()
        self._rc_timer.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_universidad.setText(_translate("MainWindow", "Universidad ECCI"))
        self.label_integrantes.setText(_translate(
            "MainWindow", "Integrantes: Jessica Daniela Bernal Gomez, Jorman Santiago Preciado Duque, Danilo Rodriguez Malago, Brayan Rincon Daza"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto 4 - Circuito RC"))
        self.label_rc_titulo.setText(_translate(
            "MainWindow", "Carga y descarga de un condensador (circuito RC)"))
        self.pushButton_reiniciar_rc.setText(_translate("MainWindow", "Reiniciar"))

    # ---------------------------------------------------------------
    # Circuito RC: carga y descarga del condensador en tiempo real
    # ---------------------------------------------------------------
    # Duración de cada fase (carga / descarga) antes de conmutar, en segundos.
    _RC_DURACION_FASE = 4.0
    # Ventana de tiempo (segundos) que se muestra en la gráfica tipo osciloscopio.
    _RC_VENTANA = 20.0

    def _inicializar_estado_rc(self):
        self._rc_t = 0.0
        self._rc_vc = 0.0
        self._rc_fase = 0
        self._rc_historial_t = deque([0.0])
        self._rc_historial_v = deque([0.0])
        self._rc_parametros = self._leer_parametros_rc()
        self._rc_reloj.start()

    def reiniciar_rc(self):
        self._inicializar_estado_rc()
        self._actualizar_grafica_rc()

    def _leer_parametros_rc(self):
        r = self.slider_r.value()          # ohmios
        c = self.slider_c.value() * 1e-6   # microfaradios -> faradios
        v = self.slider_v.value()          # voltios
        return r, c, v

    def _cambiar_parametros_rc(self):
        # Completar el intervalo anterior con sus parámetros originales.
        self._integrar_rc(self._rc_reloj.nsecsElapsed() / 1e9)
        self._rc_parametros = self._leer_parametros_rc()
        # El ajuste interactivo conserva Vc y el historial; no reinicia el ciclo.
        self._actualizar_grafica_rc()

    def _integrar_rc(self, tiempo):
        r, c, v = self._rc_parametros
        tau = r * c
        while self._rc_t < tiempo:
            fin_fase = (self._rc_fase + 1) * self._RC_DURACION_FASE
            # Dividir en la conmutación para no integrar dos fases juntas.
            siguiente = min(tiempo, fin_fase, self._rc_t + 0.04)
            objetivo = v if self._rc_fase % 2 == 0 else 0.0
            dt = siguiente - self._rc_t
            # Solución exacta del RC desde el voltaje actual.
            self._rc_vc += (objetivo - self._rc_vc) * (-math.expm1(-dt / tau))
            self._rc_t = siguiente
            self._rc_historial_t.append(self._rc_t)
            self._rc_historial_v.append(self._rc_vc)
            if siguiente >= fin_fase:
                self._rc_fase += 1

        # Conservar solo la ventana visible y un punto previo para unir la curva.
        limite = self._rc_t - self._RC_VENTANA
        while len(self._rc_historial_t) > 2 and self._rc_historial_t[1] < limite:
            self._rc_historial_t.popleft()
            self._rc_historial_v.popleft()

    def _avanzar_rc(self):
        # Reloj monotónico: los retrasos de dibujo no ralentizan la simulación.
        self._integrar_rc(self._rc_reloj.nsecsElapsed() / 1e9)
        self._actualizar_grafica_rc()

    def _actualizar_grafica_rc(self):
        r, c, v = self._rc_parametros
        self.label_valor_r.setText(f"Resistencia R = {r} Ω")
        self.label_valor_c.setText(f"Capacitancia C = {c * 1e6:g} µF")
        self.label_valor_v.setText(f"Voltaje V = {v} V")
        self.linea_v_fuente.set_ydata([v, v])
        self.linea_rc.set_data(list(self._rc_historial_t), list(self._rc_historial_v))
        derecha = max(self._RC_VENTANA, self._rc_t)
        self.axes_rc.set_xlim(derecha - self._RC_VENTANA, derecha)
        # Mantener visible el voltaje residual incluso si baja la fuente.
        maximo = max(v, max(self._rc_historial_v))
        margen = max(maximo * 0.10, 0.5)
        self.axes_rc.set_ylim(-margen, maximo + margen)
        fase = "CARGA" if self._rc_fase % 2 == 0 else "DESCARGA"
        self.label_estado_rc.setText(
            f"Fase: {fase} | Vc = {self._rc_vc:.2f} V | τ = {r * c:.3g} s")
        self.canvas_rc.draw_idle()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())