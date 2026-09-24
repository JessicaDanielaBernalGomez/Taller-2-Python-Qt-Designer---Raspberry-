import numpy as np
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


        self.label_grafica = QtWidgets.QLabel(self.centralwidget)
        self.label_grafica.setGeometry(QtCore.QRect(20, 75, 550, 25))
        font6 = QtGui.QFont()
        font6.setPointSize(11)
        font6.setBold(True)
        self.label_grafica.setFont(font6)
        self.label_grafica.setObjectName("label_grafica")

        # ---------- Pop Up Menú: selección de función ----------
        self.label_funcion = QtWidgets.QLabel(self.centralwidget)
        self.label_funcion.setGeometry(QtCore.QRect(20, 110, 70, 31))
        self.label_funcion.setObjectName("label_funcion")

        self.comboBox_funcion = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_funcion.setGeometry(QtCore.QRect(90, 108, 150, 35))
        font8 = QtGui.QFont()
        font8.setPointSize(11)
        self.comboBox_funcion.setFont(font8)
        self.comboBox_funcion.setObjectName("comboBox_funcion")
        for _ in range(6):
            self.comboBox_funcion.addItem("")

        # ---------- Edit Text: valor mínimo ----------
        self.label_min = QtWidgets.QLabel(self.centralwidget)
        self.label_min.setGeometry(QtCore.QRect(270, 110, 40, 31))
        self.label_min.setObjectName("label_min")

        self.textEdit_min = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_min.setGeometry(QtCore.QRect(315, 105, 100, 40))
        self.textEdit_min.setFont(font8)
        self.textEdit_min.setObjectName("textEdit_min")

        # ---------- Edit Text: valor máximo ----------
        self.label_max = QtWidgets.QLabel(self.centralwidget)
        self.label_max.setGeometry(QtCore.QRect(435, 110, 45, 31))
        self.label_max.setObjectName("label_max")

        self.textEdit_max = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_max.setGeometry(QtCore.QRect(485, 105, 100, 40))
        self.textEdit_max.setFont(font8)
        self.textEdit_max.setObjectName("textEdit_max")

        # ---------- Push button: graficar ----------
        self.pushButton_graficar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_graficar.setGeometry(QtCore.QRect(610, 105, 140, 40))
        font9 = QtGui.QFont()
        font9.setPointSize(12)
        self.pushButton_graficar.setFont(font9)
        self.pushButton_graficar.setObjectName("pushButton_graficar")

        # ---------- Objeto tipo axes ----------
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(20, 160, 900, 570))
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel("x (grados)")
        self.axes.grid(True)
        self.figure.tight_layout()

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

        self.pushButton_graficar.clicked.connect(self.graficar)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_universidad.setText(_translate("MainWindow", "Universidad ECCI"))
        self.label_integrantes.setText(_translate(
            "MainWindow", "Integrantes: Jessica Daniela Bernal Gomez, Jorman Santiago Preciado Duque, Danilo Rodriguez Malago, Brayan Rincon Daza"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto 2 - Gráficas trigonométricas"))
        self.label_grafica.setText(_translate("MainWindow", "Graficar función trigonométrica"))
        self.label_funcion.setText(_translate("MainWindow", "Función:"))
        self.comboBox_funcion.setItemText(0, _translate("MainWindow", "sen(x)"))
        self.comboBox_funcion.setItemText(1, _translate("MainWindow", "cos(x)"))
        self.comboBox_funcion.setItemText(2, _translate("MainWindow", "tan(x)"))
        self.comboBox_funcion.setItemText(3, _translate("MainWindow", "cot(x)"))
        self.comboBox_funcion.setItemText(4, _translate("MainWindow", "sec(x)"))
        self.comboBox_funcion.setItemText(5, _translate("MainWindow", "csc(x)"))
        self.label_min.setText(_translate("MainWindow", "Mín:"))
        self.label_max.setText(_translate("MainWindow", "Máx:"))
        self.pushButton_graficar.setText(_translate("MainWindow", "GRAFICAR"))

    # ---------------------------------------------------------------
    # Graficación de funciones trigonométricas
    # ---------------------------------------------------------------
    @staticmethod
    def _cortar_asintotas(y, limite=50.0):
        """Reemplaza con NaN los valores muy grandes cerca de una asíntota,
        para que matplotlib deje un espacio en vez de trazar una línea vertical."""
        y = y.copy()
        y[np.abs(y) > limite] = np.nan
        return y

    def graficar(self):
        try:
            x_min = float(self.textEdit_min.toPlainText().strip())
            x_max = float(self.textEdit_max.toPlainText().strip())
        except ValueError:
            QtWidgets.QMessageBox.warning(
                None, "Valores inválidos",
                "Ingrese valores numéricos válidos en Mín y Máx.")
            return

        if x_min >= x_max:
            QtWidgets.QMessageBox.warning(
                None, "Rango inválido",
                "El valor mínimo debe ser menor que el valor máximo.")
            return

        funcion = self.comboBox_funcion.currentText()
        x_deg = np.linspace(x_min, x_max, 2000)
        x_rad = np.radians(x_deg)
        limite_y = None

        if funcion == "sen(x)":
            y = np.sin(x_rad)
        elif funcion == "cos(x)":
            y = np.cos(x_rad)
        elif funcion == "tan(x)":
            y = self._cortar_asintotas(np.tan(x_rad))
            limite_y = 10
        elif funcion == "cot(x)":
            seno = np.sin(x_rad)
            with np.errstate(divide="ignore", invalid="ignore"):
                y = self._cortar_asintotas(np.cos(x_rad) / seno)
            limite_y = 10
        elif funcion == "sec(x)":
            coseno = np.cos(x_rad)
            with np.errstate(divide="ignore", invalid="ignore"):
                y = self._cortar_asintotas(1.0 / coseno)
            limite_y = 10
        elif funcion == "csc(x)":
            seno = np.sin(x_rad)
            with np.errstate(divide="ignore", invalid="ignore"):
                y = self._cortar_asintotas(1.0 / seno)
            limite_y = 10
        else:
            return

        self.axes.clear()
        self.axes.plot(x_deg, y, linewidth=1.8)
        self.axes.axhline(0, color="gray", linewidth=0.8)
        self.axes.axvline(0, color="gray", linewidth=0.8)
        self.axes.set_title(f"Gráfica de {funcion}")
        self.axes.set_xlabel("x (grados)")
        self.axes.set_ylabel(funcion)
        self.axes.grid(True)
        if limite_y is not None:
            self.axes.set_ylim(-limite_y, limite_y)
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())