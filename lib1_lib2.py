# Importar librerías.
import pdfplumber
import pyttsx3

# Inicializar el servicio de la librería.
engine = pyttsx3.init()
# Función que extrae el texto del pdf.
def ExtraerTexto(docPDF):
    # Abrir pdf que se le pase a la función.
    with pdfplumber.open(docPDF) as pdf:
        # Variable que almacenará texto extraído.
        texto = ""
        # Ciclo que recorre las páginas del pdf.
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    # Retornar el texto para posterior uso.
    return texto

# Función que lee el texto en voz alta.
def LeerTexto(texto):
    # Métodos para indicar lectura y ejecución.
    engine.say(texto)
    engine.runAndWait()

# Extraer texto del pdf.
texto = ExtraerTexto("Cuento corto.pdf")

# Guardar como mp3.
engine.save_to_file(texto, 'Cuento.mp3')

# Activar lectura
LeerTexto(texto)