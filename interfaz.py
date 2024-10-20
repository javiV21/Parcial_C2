import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                             QPushButton, QSizePolicy, QSpacerItem, 
                             QHBoxLayout, QSlider, QComboBox, QFileDialog, QMessageBox)
import pyttsx3
import pdfplumber

# Definir clase principal
class PDFReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Lector de PDF con Texto a Voz")
        self.setGeometry(750, 400, 400, 400)

        # Inicialización de pyttsx3
        self.engine = pyttsx3.init()
        self.paused = False

        # Botón para seleccionar archivo PDF
        self.btnArchivo = QPushButton("Seleccionar Archivo PDF")
        self.btnArchivo.clicked.connect(self.seleccionar_archivo)

        # Slider para controlar la velocidad de lectura
        self.sliderVelocidad = QSlider()
        self.sliderVelocidad.setOrientation(1)  # Slider horizontal
        self.sliderVelocidad.setMinimum(50)
        self.sliderVelocidad.setMaximum(200)
        self.sliderVelocidad.setValue(100)

        # Opción de idioma para traducción
        self.comboIdioma = QComboBox()
        self.comboIdioma.addItems(["Inglés", "Español", "Francés", "Alemán"])

        # Botón para iniciar la lectura en voz alta
        self.btnLeer = QPushButton("Leer en Voz Alta")
        self.btnLeer.clicked.connect(self.leer_pdf)

        # Botón para pausar la lectura
        self.btnPausar = QPushButton("Pausar")
        self.btnPausar.clicked.connect(self.pausar_lectura)
        self.btnPausar.setEnabled(False)  # Desactivado hasta que se inicie la lectura

        # Botón para reanudar la lectura
        self.btnReanudar = QPushButton("Reanudar")
        self.btnReanudar.clicked.connect(self.reanudar_lectura)
        self.btnReanudar.setEnabled(False)  # Desactivado hasta que se pause la lectura

        # Layout de formulario
        layoutF = QFormLayout()
        layoutF.addRow("Seleccionar archivo PDF:", self.btnArchivo)
        layoutF.addRow(self.btnLeer)
        layoutF.addRow("Velocidad de lectura:", self.sliderVelocidad)
        layoutF.addRow("Idioma de traducción:", self.comboIdioma)
        layoutF.addRow(self.btnPausar)
        layoutF.addRow(self.btnReanudar)

        # Layout vertical (centrado)
        layoutV = QVBoxLayout()
        layoutV.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layoutV.addLayout(layoutF)
        layoutV.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Layout horizontal (centrado)
        layoutH = QHBoxLayout()
        layoutH.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layoutH.addLayout(layoutV)
        layoutH.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Widget central
        central = QWidget()
        central.setLayout(layoutH)
        self.setCentralWidget(central)

    # Función para seleccionar archivo PDF
    def seleccionar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo PDF", "", "PDF Files (*.pdf)")
        if archivo:
            self.archivo_pdf = archivo
            self.btnPausar.setEnabled(False)
            self.btnReanudar.setEnabled(False)
        else:
            self.archivo_pdf = None

    # Función para leer el contenido del PDF en voz alta
    def leer_pdf(self):
        if not hasattr(self, 'archivo_pdf') or not self.archivo_pdf:
            # Mostrar ventana emergente de advertencia
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Archivo no seleccionado")
            msgBox.setText("Por favor, selecciona un archivo PDF antes de continuar.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return

        try:
            # Extraer texto del PDF usando pdfplumber
            with pdfplumber.open(self.archivo_pdf) as pdf:
                texto = ''
                for page in pdf.pages:
                    texto += page.extract_text()

            if not texto:
                print("No se pudo extraer texto del PDF.")  # Se podría reemplazar con una ventana de advertencia
                return

            # Configurar y leer el texto usando pyttsx3
            velocidad = self.sliderVelocidad.value()
            self.engine.setProperty('rate', velocidad)
            self.engine.say(texto)
            self.engine.runAndWait()

            self.btnPausar.setEnabled(True)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")  # Se podría reemplazar con una ventana de advertencia

    # Función para pausar la lectura
    def pausar_lectura(self):
        if not self.paused:
            self.engine.stop()
            self.paused = True
            self.btnPausar.setEnabled(False)
            self.btnReanudar.setEnabled(True)

    # Función para reanudar la lectura
    def reanudar_lectura(self):
        if self.paused:
            self.engine.runAndWait()
            self.paused = False
            self.btnPausar.setEnabled(True)
            self.btnReanudar.setEnabled(False)

# Creación de la aplicación
app = QApplication(sys.argv)
ventana = PDFReaderApp()
ventana.show()
sys.exit(app.exec_())