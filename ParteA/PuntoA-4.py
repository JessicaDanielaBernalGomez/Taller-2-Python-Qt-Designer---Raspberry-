import math
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
        self.label_estado_rc.setGeometry(QtCore.QRect(200, 172, 300, 35))
        font_estado_rc = QtGui.QFont()
        font_estado_rc.setPointSize(11)
        font_estado_rc.setBold(True)
        self.label_estado_rc.setFont(font_estado_rc)
        self.label_estado_rc.setObjectName("label_estado_rc")

        # --- Objeto tipo axes: gráfica estática de Vc(t) ---
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
        self.slider_r.valueChanged.connect(self._actualizar_grafica_rc)
        self.slider_c.valueChanged.connect(self._actualizar_grafica_rc)
        self.slider_v.valueChanged.connect(self._actualizar_grafica_rc)
        self.pushButton_reiniciar_rc.clicked.connect(self.reiniciar_rc)

        self._inicializar_estado_rc()
        self._actualizar_grafica_rc()

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
        # La simulación se calcula completa y se muestra de forma estática.
        self._rc_historial_t = []
        self._rc_historial_v = []

    def reiniciar_rc(self):
        # Reinicia y vuelve a calcular la gráfica completa.
        self._actualizar_grafica_rc()

    def _leer_parametros_rc(self):
        r = self.slider_r.value()          # ohmios
        c = self.slider_c.value() * 1e-6   # microfaradios -> faradios
        v = self.slider_v.value()          # voltios
        return r, c, v

    def _actualizar_grafica_rc(self):
        r, c, v = self._leer_parametros_rc()

        # Actualizar los valores mostrados
        self.label_valor_r.setText(f"Resistencia R = {r} Ω")
        self.label_valor_c.setText(f"Capacitancia C = {self.slider_c.value()} µF")
        self.label_valor_v.setText(f"Voltaje V = {v} V")
        self.linea_v_fuente.set_ydata([v, v])

        # Constante de tiempo del circuito
        tau = max(r * c, 1e-6)

        # Tiempo total de la gráfica: 20 s
        dt = 0.01
        tiempo_total = self._RC_VENTANA

        tiempos = []
        voltajes = []

        # Simulación estática de carga y descarga.
        # Cada fase dura 4 segundos.
        for i in range(int(tiempo_total / dt) + 1):
            t = i * dt
            t_fase = t % (2 * self._RC_DURACION_FASE)

            if t_fase < self._RC_DURACION_FASE:
                # Carga: inicia en 0 V y se aproxima a V
                tiempo_carga = t_fase
                vc = v * (1 - math.exp(-tiempo_carga / tau))
                estado = "Estado: CARGANDO"
            else:
                # Descarga: parte del valor alcanzado al final de la carga
                tiempo_descarga = t_fase - self._RC_DURACION_FASE
                vc_carga = v * (1 - math.exp(-self._RC_DURACION_FASE / tau))
                vc = vc_carga * math.exp(-tiempo_descarga / tau)
                estado = "Estado: DESCARGANDO"

            tiempos.append(t)
            voltajes.append(vc)

        self._rc_historial_t = tiempos
        self._rc_historial_v = voltajes

        # Dibujar la curva completa de una sola vez
        self.linea_rc.set_data(tiempos, voltajes)
        self.axes_rc.set_xlim(0, self._RC_VENTANA)

        # Ajustar el eje Y al voltaje seleccionado
        margen = max(v * 0.10, 0.5)
        self.axes_rc.set_ylim(-margen, v + margen)

        # Mostrar el estado inicial
        self.label_estado_rc.setText("Estado: CARGANDO")

        self.canvas_rc.draw_idle()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())