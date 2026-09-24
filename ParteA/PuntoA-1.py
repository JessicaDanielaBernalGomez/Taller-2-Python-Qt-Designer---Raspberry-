import math

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 620)

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


        # ---------- Título ----------
        self.label_titulo = QtWidgets.QLabel(self.centralwidget)
        self.label_titulo.setGeometry(QtCore.QRect(20, 80, 910, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_titulo.setFont(font)
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo.setObjectName("label_titulo")

        # ---------- Entradas ----------
        self.label_a = QtWidgets.QLabel(self.centralwidget)
        self.label_a.setGeometry(QtCore.QRect(60, 150, 121, 31))
        self.label_a.setAlignment(QtCore.Qt.AlignCenter)
        font2 = QtGui.QFont()
        font2.setPointSize(11)
        self.label_a.setFont(font2)
        self.label_a.setObjectName("label_a")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 180, 160, 41))
        font3 = QtGui.QFont()
        font3.setPointSize(13)
        self.textEdit.setFont(font3)
        self.textEdit.setObjectName("textEdit")

        self.label_b = QtWidgets.QLabel(self.centralwidget)
        self.label_b.setGeometry(QtCore.QRect(260, 150, 121, 31))
        self.label_b.setAlignment(QtCore.Qt.AlignCenter)
        self.label_b.setFont(font2)
        self.label_b.setObjectName("label_b")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(240, 180, 160, 41))
        self.textEdit_2.setFont(font3)
        self.textEdit_2.setObjectName("textEdit_2")

        self.label_igual = QtWidgets.QLabel(self.centralwidget)
        self.label_igual.setGeometry(QtCore.QRect(430, 180, 41, 41))
        font4 = QtGui.QFont()
        font4.setPointSize(16)
        self.label_igual.setFont(font4)
        self.label_igual.setAlignment(QtCore.Qt.AlignCenter)
        self.label_igual.setObjectName("label_igual")

        # ---------- Resultado (Static Text) ----------
        self.label_resultado = QtWidgets.QLabel(self.centralwidget)
        self.label_resultado.setGeometry(QtCore.QRect(490, 160, 400, 61))
        font5 = QtGui.QFont()
        font5.setPointSize(16)
        self.label_resultado.setFont(font5)
        self.label_resultado.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_resultado.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_resultado.setAlignment(QtCore.Qt.AlignCenter)
        self.label_resultado.setText("")
        self.label_resultado.setObjectName("label_resultado")

        # ---------- Botones de operaciones aritméticas ----------
        self.label_aritmetica = QtWidgets.QLabel(self.centralwidget)
        self.label_aritmetica.setGeometry(QtCore.QRect(40, 250, 450, 25))
        font6 = QtGui.QFont()
        font6.setPointSize(11)
        font6.setBold(True)
        self.label_aritmetica.setFont(font6)
        self.label_aritmetica.setObjectName("label_aritmetica")

        self.pushButton_suma = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_suma.setGeometry(QtCore.QRect(40, 280, 90, 45))
        self.pushButton_suma.setObjectName("pushButton_suma")

        self.pushButton_resta = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_resta.setGeometry(QtCore.QRect(140, 280, 90, 45))
        self.pushButton_resta.setObjectName("pushButton_resta")

        self.pushButton_mult = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mult.setGeometry(QtCore.QRect(240, 280, 90, 45))
        self.pushButton_mult.setObjectName("pushButton_mult")

        self.pushButton_cociente = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cociente.setGeometry(QtCore.QRect(340, 280, 110, 45))
        self.pushButton_cociente.setObjectName("pushButton_cociente")

        self.pushButton_residuo = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_residuo.setGeometry(QtCore.QRect(460, 280, 110, 45))
        self.pushButton_residuo.setObjectName("pushButton_residuo")

        for b in (self.pushButton_suma, self.pushButton_resta, self.pushButton_mult,
                  self.pushButton_cociente, self.pushButton_residuo):
            f = QtGui.QFont()
            f.setPointSize(12)
            b.setFont(f)

        # ---------- Botones de operaciones trigonométricas ----------
        self.label_trig = QtWidgets.QLabel(self.centralwidget)
        self.label_trig.setGeometry(QtCore.QRect(40, 360, 550, 25))
        self.label_trig.setFont(font6)
        self.label_trig.setObjectName("label_trig")

        self.pushButton_sen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_sen.setGeometry(QtCore.QRect(40, 390, 90, 45))
        self.pushButton_sen.setObjectName("pushButton_sen")

        self.pushButton_cos = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cos.setGeometry(QtCore.QRect(140, 390, 90, 45))
        self.pushButton_cos.setObjectName("pushButton_cos")

        self.pushButton_tan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tan.setGeometry(QtCore.QRect(240, 390, 90, 45))
        self.pushButton_tan.setObjectName("pushButton_tan")

        self.pushButton_cot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cot.setGeometry(QtCore.QRect(340, 390, 90, 45))
        self.pushButton_cot.setObjectName("pushButton_cot")

        self.pushButton_sec = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_sec.setGeometry(QtCore.QRect(440, 390, 90, 45))
        self.pushButton_sec.setObjectName("pushButton_sec")

        self.pushButton_csc = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_csc.setGeometry(QtCore.QRect(540, 390, 90, 45))
        self.pushButton_csc.setObjectName("pushButton_csc")

        for b in (self.pushButton_sen, self.pushButton_cos, self.pushButton_tan,
                  self.pushButton_cot, self.pushButton_sec, self.pushButton_csc):
            f = QtGui.QFont()
            f.setPointSize(12)
            b.setFont(f)

        # ---------- Nota informativa ----------
        self.label_nota = QtWidgets.QLabel(self.centralwidget)
        self.label_nota.setGeometry(QtCore.QRect(40, 460, 870, 40))
        font7 = QtGui.QFont()
        font7.setPointSize(9)
        font7.setItalic(True)
        self.label_nota.setFont(font7)
        self.label_nota.setWordWrap(True)
        self.label_nota.setObjectName("label_nota")

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
        self.pushButton_suma.clicked.connect(self.suma)
        self.pushButton_resta.clicked.connect(self.resta)
        self.pushButton_mult.clicked.connect(self.multiplicacion)
        self.pushButton_cociente.clicked.connect(self.cociente)
        self.pushButton_residuo.clicked.connect(self.residuo)

        self.pushButton_sen.clicked.connect(self.seno)
        self.pushButton_cos.clicked.connect(self.coseno)
        self.pushButton_tan.clicked.connect(self.tangente)
        self.pushButton_cot.clicked.connect(self.cotangente)
        self.pushButton_sec.clicked.connect(self.secante)
        self.pushButton_csc.clicked.connect(self.cosecante)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_universidad.setText(_translate("MainWindow", "Universidad ECCI"))
        self.label_integrantes.setText(_translate(
            "MainWindow", "Integrantes: Jessica Daniela Bernal Gomez, Jorman Santiago Preciado Duque, Danilo Rodriguez Malago, Brayan Rincon Daza"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto 1 - Calculadora Aritmética y Trigonométrica"))
        self.label_titulo.setText(_translate("MainWindow", "CALCULADORA ARITMÉTICA Y TRIGONOMÉTRICA"))
        self.label_a.setText(_translate("MainWindow", "Valor A"))
        self.label_b.setText(_translate("MainWindow", "Valor B"))
        self.label_igual.setText(_translate("MainWindow", "="))
        self.label_aritmetica.setText(_translate("MainWindow", "Operaciones aritméticas (usan A y B)"))
        self.pushButton_suma.setText(_translate("MainWindow", "+"))
        self.pushButton_resta.setText(_translate("MainWindow", "−"))
        self.pushButton_mult.setText(_translate("MainWindow", "×"))
        self.pushButton_cociente.setText(_translate("MainWindow", "A // B"))
        self.pushButton_residuo.setText(_translate("MainWindow", "A % B"))
        self.label_trig.setText(_translate("MainWindow", "Operaciones trigonométricas (usan A, en grados)"))
        self.pushButton_sen.setText(_translate("MainWindow", "sen"))
        self.pushButton_cos.setText(_translate("MainWindow", "cos"))
        self.pushButton_tan.setText(_translate("MainWindow", "tan"))
        self.pushButton_cot.setText(_translate("MainWindow", "cot"))
        self.pushButton_sec.setText(_translate("MainWindow", "sec"))
        self.pushButton_csc.setText(_translate("MainWindow", "csc"))
        self.label_nota.setText(_translate(
            "MainWindow",
            "Nota: para +, −, ×, // y % se usan los valores A y B. Para sen, cos, tan, cot, sec y csc "
            "solo se usa el valor A (ángulo en grados)."))

    # ---------------------------------------------------------------
    # Utilidades internas
    # ---------------------------------------------------------------
    def _leer_a(self):
        return float(self.textEdit.toPlainText().strip())

    def _leer_ab(self):
        a = float(self.textEdit.toPlainText().strip())
        b = float(self.textEdit_2.toPlainText().strip())
        return a, b

    def _mostrar(self, valor):
        self.label_resultado.setText(str(valor))

    def _mostrar_error(self, mensaje):
        self.label_resultado.setText(mensaje)

    # ---------------------------------------------------------------
    # Operaciones aritméticas
    # ---------------------------------------------------------------
    def suma(self):
        try:
            a, b = self._leer_ab()
            self._mostrar(a + b)
        except ValueError:
            self._mostrar_error("Valores inválidos")

    def resta(self):
        try:
            a, b = self._leer_ab()
            self._mostrar(a - b)
        except ValueError:
            self._mostrar_error("Valores inválidos")

    def multiplicacion(self):
        try:
            a, b = self._leer_ab()
            self._mostrar(a * b)
        except ValueError:
            self._mostrar_error("Valores inválidos")

    def cociente(self):
        try:
            a, b = self._leer_ab()
            self._mostrar(a // b)
        except ZeroDivisionError:
            self._mostrar_error("División por cero")
        except ValueError:
            self._mostrar_error("Valores inválidos")

    def residuo(self):
        try:
            a, b = self._leer_ab()
            self._mostrar(a % b)
        except ZeroDivisionError:
            self._mostrar_error("División por cero")
        except ValueError:
            self._mostrar_error("Valores inválidos")

    # ---------------------------------------------------------------
    # Operaciones trigonométricas (ángulo en grados, solo usan A)
    # ---------------------------------------------------------------
    def seno(self):
        try:
            a = self._leer_a()
            self._mostrar(round(math.sin(math.radians(a)), 6))
        except ValueError:
            self._mostrar_error("Valor inválido")

    def coseno(self):
        try:
            a = self._leer_a()
            self._mostrar(round(math.cos(math.radians(a)), 6))
        except ValueError:
            self._mostrar_error("Valor inválido")

    def tangente(self):
        try:
            a = self._leer_a()
            self._mostrar(round(math.tan(math.radians(a)), 6))
        except ValueError:
            self._mostrar_error("Valor inválido")

    def cotangente(self):
        try:
            a = self._leer_a()
            t = math.tan(math.radians(a))
            self._mostrar(round(1 / t, 6))
        except ZeroDivisionError:
            self._mostrar_error("Indefinido")
        except ValueError:
            self._mostrar_error("Valor inválido")

    def secante(self):
        try:
            a = self._leer_a()
            c = math.cos(math.radians(a))
            self._mostrar(round(1 / c, 6))
        except ZeroDivisionError:
            self._mostrar_error("Indefinido")
        except ValueError:
            self._mostrar_error("Valor inválido")

    def cosecante(self):
        try:
            a = self._leer_a()
            s = math.sin(math.radians(a))
            self._mostrar(round(1 / s, 6))
        except ZeroDivisionError:
            self._mostrar_error("Indefinido")
        except ValueError:
            self._mostrar_error("Valor inválido")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())