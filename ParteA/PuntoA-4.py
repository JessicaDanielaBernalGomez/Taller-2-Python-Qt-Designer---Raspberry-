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
        self.label_estado_rc.setGeometry(QtCore.QRect(200, 172, 690, 35))
        font_estado_rc = QtGui.QFont()
        font_estado_rc.setPointSize(11)
        font_estado_rc.setBold(True)
        self.label_estado_rc.setFont(font_estado_rc)
        self.label_estado_rc.setObjectName("label_estado_rc")

        # --- Objeto tipo axes: gráfica estática de carga y descarga ---
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

        self._actualizar_grafica_rc()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_universidad.setText(_translate("MainWindow", "Universidad ECCI"))
        self.label_integrantes.setText(_translate(
            "MainWindow", "Integrantes: Jessica Daniela Bernal Gomez, Jorman Santiago Preciado Duque, Danilo Rodriguez Malago, Brayan Rincon Daza"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto 4 - Circuito RC"))
        self.label_rc_titulo.setText(_translate(
            "MainWindow", "Carga y descarga de un condensador (circuito RC)"))
        self.pushButton_reiniciar_rc.setText(_translate("MainWindow", "Restablecer valores"))

    # Curvas independientes: t=0 al iniciar cada fase.
    # Carga desde 0 V; descarga desde V de la fuente. No hay temporizador.
    def reiniciar_rc(self):
        for slider, valor in ((self.slider_r, 1000), (self.slider_c, 100),
                              (self.slider_v, 12)):
            slider.blockSignals(True)
            slider.setValue(valor)
            slider.blockSignals(False)
        self._actualizar_grafica_rc()

    def _leer_parametros_rc(self):
        return self.slider_r.value(), self.slider_c.value() * 1e-6, self.slider_v.value()

    def _actualizar_grafica_rc(self):
        r, c, v = self._leer_parametros_rc()
        tau = r * c
        cinco_tau = 5 * tau
        tiempos = [i * tau / 100 for i in range(601)]
        carga = [v * (-math.expm1(-t / tau)) for t in tiempos]
        descarga = [v * math.exp(-t / tau) for t in tiempos]
        self.label_valor_r.setText(f"Resistencia R = {r} Ω")
        self.label_valor_c.setText(f"Capacitancia C = {c * 1e6:g} µF")
        self.label_valor_v.setText(f"Voltaje V = {v} V")
        self.label_estado_rc.setText(f"τ = RC = {tau:.6g} s     |     5τ = {cinco_tau:.6g} s")
        ax = self.axes_rc
        ax.clear()
        self.linea_carga, = ax.plot(tiempos, carga, color="tab:blue", label="Carga desde 0 V")
        self.linea_descarga, = ax.plot(tiempos, descarga, color="tab:orange", label="Descarga desde V")
        ax.axhline(v, color="gray", linestyle=":", linewidth=1)
        self.marca_cinco_tau = ax.axvline(cinco_tau, color="crimson", linestyle="--", linewidth=2)
        ax.text(cinco_tau, v * 1.10, f"5τ = {cinco_tau:.6g} s",
                ha="center", color="crimson", fontweight="bold",
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})
        vc5, vd5 = v * (1 - math.exp(-5)), v * math.exp(-5)
        ax.scatter([cinco_tau, cinco_tau], [vc5, vd5], color=["tab:blue", "tab:orange"], zorder=5)
        ax.annotate(f"Carga: 99,33 % = {vc5:.4g} V", (cinco_tau, vc5),
                    xytext=(2.4 * tau, 0.83 * v), arrowprops={"arrowstyle": "->"},
                    color="tab:blue")
        ax.annotate(f"Descarga: 0,67 % = {vd5:.4g} V", (cinco_tau, vd5),
                    xytext=(2.4 * tau, 0.20 * v), arrowprops={"arrowstyle": "->"},
                    color="tab:orange")
        ax.set_xlim(0, 6 * tau)
        ax.set_ylim(-0.06 * v, 1.2 * v)
        ax.set_xlabel("Tiempo desde el inicio de cada fase (s)")
        ax.set_ylabel("Voltaje del condensador (V)")
        ax.set_title("Carga y descarga RC · referencia de establecimiento: 5τ")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="center right")
        self.figure_rc.tight_layout()
        self.canvas_rc.draw_idle()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())