import os
import cv2
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

        self.label_imagen_titulo = QtWidgets.QLabel(self.centralwidget)
        self.label_imagen_titulo.setGeometry(QtCore.QRect(20, 72, 700, 25))
        self.label_imagen_titulo.setFont(font6)
        self.label_imagen_titulo.setObjectName("label_imagen_titulo")

        # ---------- Push button: buscar y cargar la imagen ----------
        self.pushButton_cargar_imagen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cargar_imagen.setGeometry(QtCore.QRect(20, 105, 220, 45))
        font_boton_img = QtGui.QFont()
        font_boton_img.setPointSize(11)
        self.pushButton_cargar_imagen.setFont(font_boton_img)
        self.pushButton_cargar_imagen.setObjectName("pushButton_cargar_imagen")

        # ---------- Static Text: ruta/nombre del archivo seleccionado ----------
        self.label_ruta_imagen = QtWidgets.QLabel(self.centralwidget)
        self.label_ruta_imagen.setGeometry(QtCore.QRect(260, 105, 400, 22))
        self.label_ruta_imagen.setObjectName("label_ruta_imagen")

        # ---------- Static Text: número de contornos encontrados ----------
        self.label_num_contornos = QtWidgets.QLabel(self.centralwidget)
        self.label_num_contornos.setGeometry(QtCore.QRect(260, 128, 400, 22))
        font_info_img = QtGui.QFont()
        font_info_img.setPointSize(10)
        font_info_img.setBold(True)
        self.label_num_contornos.setFont(font_info_img)
        self.label_num_contornos.setObjectName("label_num_contornos")

        # ---------- Objeto tipo axes: imagen original ----------
        self.figure_img_original = Figure(figsize=(4, 4))
        self.canvas_img_original = FigureCanvas(self.figure_img_original)
        self.canvas_img_original.setParent(self.centralwidget)
        self.canvas_img_original.setGeometry(QtCore.QRect(20, 165, 440, 555))
        self.axes_img_original = self.figure_img_original.add_subplot(111)
        self.axes_img_original.axis("off")
        self.figure_img_original.tight_layout()

        # ---------- Objeto tipo axes: contornos detectados ----------
        self.figure_img_contornos = Figure(figsize=(4, 4))
        self.canvas_img_contornos = FigureCanvas(self.figure_img_contornos)
        self.canvas_img_contornos.setParent(self.centralwidget)
        self.canvas_img_contornos.setGeometry(QtCore.QRect(480, 165, 440, 555))
        self.axes_img_contornos = self.figure_img_contornos.add_subplot(111)
        self.axes_img_contornos.axis("off")
        self.figure_img_contornos.tight_layout()

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

        self.pushButton_cargar_imagen.clicked.connect(self.cargar_imagen)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_universidad.setText(_translate("MainWindow", "Universidad: NOMBRE_DE_LA_UNIVERSIDAD"))
        self.label_integrantes.setText(_translate(
            "MainWindow", "Integrantes: Jessica Daniela Bernal Gomez, Jorman Santiago Preciado Duque, Danilo Rodriguez Malago, Brayan Rincon Daza"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto 5 - Imagen y contornos"))
        self.label_imagen_titulo.setText(_translate(
            "MainWindow", "Cargar imagen del PC y detectar sus contornos"))
        self.pushButton_cargar_imagen.setText(_translate("MainWindow", "Buscar imagen..."))
        self.label_ruta_imagen.setText(_translate("MainWindow", "Ningún archivo seleccionado"))
        self.label_num_contornos.setText(_translate("MainWindow", ""))

    # ---------------------------------------------------------------
    # Cargar imagen y detectar contornos
    # ---------------------------------------------------------------
    def cargar_imagen(self):
        ruta, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Seleccionar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;Todos los archivos (*)",
        )
        if not ruta:
            return  # el usuario canceló la búsqueda

        imagen_bgr = cv2.imread(ruta)
        if imagen_bgr is None:
            QtWidgets.QMessageBox.warning(
                None, "Error al abrir la imagen",
                "No se pudo leer el archivo seleccionado como una imagen válida.")
            return

        self.label_ruta_imagen.setText(os.path.basename(ruta))

        # --- Procesamiento: escala de grises, suavizado y bordes ---
        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        suavizada = cv2.GaussianBlur(gris, (5, 5), 0)
        bordes = cv2.Canny(suavizada, 50, 150)

        # --- Detección de contornos ---
        contornos, _ = cv2.findContours(
            bordes, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        imagen_contornos = imagen_bgr.copy()
        cv2.drawContours(imagen_contornos, contornos, -1, (0, 255, 0), 2)

        self.label_num_contornos.setText(f"Contornos detectados: {len(contornos)}")

        # --- Mostrar imagen original ---
        imagen_original_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
        self.axes_img_original.clear()
        self.axes_img_original.imshow(imagen_original_rgb)
        self.axes_img_original.set_title("Imagen original")
        self.axes_img_original.axis("off")
        self.figure_img_original.tight_layout()
        self.canvas_img_original.draw()

        # --- Mostrar imagen con los contornos resaltados ---
        imagen_contornos_rgb = cv2.cvtColor(imagen_contornos, cv2.COLOR_BGR2RGB)
        self.axes_img_contornos.clear()
        self.axes_img_contornos.imshow(imagen_contornos_rgb)
        self.axes_img_contornos.set_title("Contornos detectados")
        self.axes_img_contornos.axis("off")
        self.figure_img_contornos.tight_layout()
        self.canvas_img_contornos.draw()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())