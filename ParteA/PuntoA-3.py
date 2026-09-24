from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle, Arc


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

        self.label_robot_titulo = QtWidgets.QLabel(self.centralwidget)
        self.label_robot_titulo.setGeometry(QtCore.QRect(20, 75, 550, 25))
        self.label_robot_titulo.setFont(font6)
        self.label_robot_titulo.setObjectName("label_robot_titulo")

        # ---------- Pop-up menú: tipo de robot ----------
        self.label_tipo_robot = QtWidgets.QLabel(self.centralwidget)
        self.label_tipo_robot.setGeometry(QtCore.QRect(20, 110, 130, 31))
        self.label_tipo_robot.setObjectName("label_tipo_robot")

        self.comboBox_robot = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_robot.setGeometry(QtCore.QRect(150, 106, 260, 38))
        font10 = QtGui.QFont()
        font10.setPointSize(11)
        self.comboBox_robot.setFont(font10)
        self.comboBox_robot.setObjectName("comboBox_robot")
        for _ in range(3):
            self.comboBox_robot.addItem("")

        # ---------- Static Text: información de las articulaciones ----------
        self.label_info_robot = QtWidgets.QLabel(self.centralwidget)
        self.label_info_robot.setGeometry(QtCore.QRect(430, 100, 460, 60))
        font11 = QtGui.QFont()
        font11.setPointSize(11)
        self.label_info_robot.setFont(font11)
        self.label_info_robot.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_info_robot.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_info_robot.setWordWrap(True)
        self.label_info_robot.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info_robot.setObjectName("label_info_robot")

        # ---------- Objeto tipo axes: diagrama cinemático ----------
        self.figure_robot = Figure(figsize=(5, 4))
        self.canvas_robot = FigureCanvas(self.figure_robot)
        self.canvas_robot.setParent(self.centralwidget)
        self.canvas_robot.setGeometry(QtCore.QRect(20, 175, 900, 555))
        self.axes_robot = self.figure_robot.add_subplot(111)
        self.figure_robot.tight_layout()

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

        self.comboBox_robot.currentIndexChanged.connect(self.actualizar_robot)
        # Mostrar la información del primer robot al abrir el programa
        self.actualizar_robot(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_universidad.setText(_translate("MainWindow", "Universidad ECCI"))
        self.label_integrantes.setText(_translate(
            "MainWindow", "Integrantes: Jessica Daniela Bernal Gomez, Jorman Santiago Preciado Duque, Danilo Rodriguez Malago, Brayan Rincon Daza"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto 3 - Selección de robot y diagrama cinemático"))
        self.label_robot_titulo.setText(_translate("MainWindow", "Selección de robot y diagrama cinemático"))
        self.label_tipo_robot.setText(_translate("MainWindow", "Tipo de robot:"))
        self.comboBox_robot.setItemText(0, _translate("MainWindow", "Robot Cartesiano"))
        self.comboBox_robot.setItemText(1, _translate("MainWindow", "Robot Esférico"))
        self.comboBox_robot.setItemText(2, _translate("MainWindow", "Robot Cilíndrico"))

    # ---------------------------------------------------------------
    # Información de articulaciones + diagrama cinemático
    # ---------------------------------------------------------------
    def _info_robot(self, indice):
        info = {
            0: "Robot CARTESIANO\n3 articulaciones: todas PRISMÁTICAS\nSecuencia: P - P - P (ejes X, Y, Z)",
            1: "Robot ESFÉRICO\n3 articulaciones: 2 ROTACIONALES y 1 PRISMÁTICA\nSecuencia: R - R - P",
            2: "Robot CILÍNDRICO\n3 articulaciones: 1 ROTACIONAL y 2 PRISMÁTICAS\nSecuencia: R - P - P",
        }
        return info.get(indice, "")

    def actualizar_robot(self, indice):
        self.label_info_robot.setText(self._info_robot(indice))
        if indice == 0:
            self._dibujar_cartesiano()
        elif indice == 1:
            self._dibujar_esferico()
        elif indice == 2:
            self._dibujar_cilindrico()

    def _preparar_axes_robot(self, titulo):
        ax = self.axes_robot
        ax.clear()
        ax.set_title(titulo, fontsize=12, fontweight="bold")
        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 6)
        ax.set_aspect("equal")
        ax.axis("off")
        return ax

    @staticmethod
    def _junta_prismatica(ax, x, y, tam=0.35, angulo=0):
        """Dibuja el símbolo de una articulación prismática (rectángulo)."""
        rect = Rectangle((x - tam / 2, y - tam / 2), tam, tam,
                          angle=angulo, facecolor="white", edgecolor="black",
                          linewidth=1.6, zorder=3)
        ax.add_patch(rect)

    @staticmethod
    def _junta_rotacional(ax, x, y, radio=0.22):
        """Dibuja el símbolo de una articulación rotacional (círculo)."""
        circ = Circle((x, y), radio, facecolor="white", edgecolor="black",
                      linewidth=1.6, zorder=3)
        ax.add_patch(circ)

    def _dibujar_cartesiano(self):
        ax = self._preparar_axes_robot("Diagrama cinemático: Robot Cartesiano (P-P-P)")

        base = (0.6, 0.6)
        p1 = (0.6, 3.2)     # se desliza en Z
        p2 = (3.0, 3.2)     # se desliza en Y
        p3 = (4.6, 4.4)     # se desliza en X (representa profundidad)

        ax.add_patch(Rectangle((base[0] - 0.5, base[1] - 0.35), 1.0, 0.35,
                                facecolor="0.6", edgecolor="black", zorder=2))

        ax.plot([base[0], p1[0]], [base[1], p1[1]], "k-", linewidth=3, zorder=1)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], "k-", linewidth=3, zorder=1)
        ax.plot([p2[0], p3[0]], [p2[1], p3[1]], "k--", linewidth=2, zorder=1)

        self._junta_prismatica(ax, *p1)
        self._junta_prismatica(ax, *p2)
        self._junta_prismatica(ax, *p3)

        ax.plot(p3[0], p3[1], marker="o", markersize=6, color="red", zorder=4)

        ax.text(base[0], base[1] - 0.6, "Base", ha="center", fontsize=9)
        ax.text(p1[0] - 0.55, (base[1] + p1[1]) / 2, "P1 (Z)", fontsize=9)
        ax.text((p1[0] + p2[0]) / 2, p2[1] + 0.15, "P2 (Y)", fontsize=9)
        ax.text((p2[0] + p3[0]) / 2 + 0.1, (p2[1] + p3[1]) / 2, "P3 (X)", fontsize=9)
        ax.text(p3[0] + 0.2, p3[1], "Efector final", fontsize=9, color="red")

        self.figure_robot.tight_layout()
        self.canvas_robot.draw()

    def _dibujar_esferico(self):
        ax = self._preparar_axes_robot("Diagrama cinemático: Robot Esférico (R-R-P)")

        base = (2.0, 0.6)
        r1 = (2.0, 1.6)      # rotación de cintura (eje vertical)
        r2 = (2.0, 2.8)      # rotación de hombro
        p3 = (4.2, 4.6)      # extensión prismática (brazo telescópico)

        ax.add_patch(Rectangle((base[0] - 0.6, base[1] - 0.35), 1.2, 0.35,
                                facecolor="0.6", edgecolor="black", zorder=2))

        ax.plot([base[0], r1[0]], [base[1], r1[1]], "k-", linewidth=3, zorder=1)
        ax.plot([r1[0], r2[0]], [r1[1], r2[1]], "k-", linewidth=3, zorder=1)
        ax.plot([r2[0], p3[0]], [r2[1], p3[1]], "k-", linewidth=2, zorder=1)
        ax.plot([r2[0] + 0.1, p3[0] + 0.1], [r2[1] + 0.05, p3[1] + 0.05],
                "k-", linewidth=1, zorder=1)

        arco = Arc(r1, 1.0, 0.5, angle=0, theta1=200, theta2=340)
        ax.add_patch(arco)

        self._junta_rotacional(ax, *r1)
        self._junta_rotacional(ax, *r2)
        self._junta_prismatica(ax, *p3)

        ax.plot(p3[0], p3[1], marker="o", markersize=6, color="red", zorder=4)

        ax.text(base[0], base[1] - 0.6, "Base", ha="center", fontsize=9)
        ax.text(r1[0] + 0.3, r1[1], "R1 (cintura)", fontsize=9)
        ax.text(r2[0] + 0.3, r2[1], "R2 (hombro)", fontsize=9)
        ax.text((r2[0] + p3[0]) / 2 - 0.3, (r2[1] + p3[1]) / 2 + 0.3, "P3", fontsize=9)
        ax.text(p3[0] + 0.2, p3[1], "Efector final", fontsize=9, color="red")

        self.figure_robot.tight_layout()
        self.canvas_robot.draw()

    def _dibujar_cilindrico(self):
        ax = self._preparar_axes_robot("Diagrama cinemático: Robot Cilíndrico (R-P-P)")

        base = (1.2, 0.6)
        r1 = (1.2, 1.4)      # rotación de cintura
        p2 = (1.2, 3.6)      # desliza verticalmente (Z)
        p3 = (4.2, 3.6)      # desliza horizontalmente (radial)

        ax.add_patch(Rectangle((base[0] - 0.6, base[1] - 0.35), 1.2, 0.35,
                                facecolor="0.6", edgecolor="black", zorder=2))

        ax.plot([r1[0], p2[0]], [r1[1], p2[1]], "k-", linewidth=3, zorder=1)
        ax.plot([r1[0] + 0.12, p2[0] + 0.12], [r1[1], p2[1]], "k-", linewidth=1, zorder=1)

        ax.plot([p2[0], p3[0]], [p2[1], p3[1]], "k-", linewidth=2, zorder=1)
        ax.plot([p2[0], p3[0]], [p2[1] + 0.1, p3[1] + 0.1], "k-", linewidth=1, zorder=1)

        arco = Arc(r1, 1.0, 0.5, angle=0, theta1=200, theta2=340)
        ax.add_patch(arco)

        self._junta_rotacional(ax, *r1)
        self._junta_prismatica(ax, *p2)
        self._junta_prismatica(ax, *p3)

        ax.plot(p3[0], p3[1], marker="o", markersize=6, color="red", zorder=4)

        ax.text(base[0], base[1] - 0.6, "Base", ha="center", fontsize=9)
        ax.text(r1[0] + 0.3, r1[1], "R1 (cintura)", fontsize=9)
        ax.text(p2[0] + 0.3, (r1[1] + p2[1]) / 2, "P2 (Z)", fontsize=9)
        ax.text((p2[0] + p3[0]) / 2, p3[1] + 0.2, "P3 (radial)", fontsize=9)
        ax.text(p3[0] + 0.2, p3[1], "Efector final", fontsize=9, color="red")

        self.figure_robot.tight_layout()
        self.canvas_robot.draw()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())