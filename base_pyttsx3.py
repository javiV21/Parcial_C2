# Importar librería.
import pyttsx3

#Inicializar el servicio de la librería con idioma español.
engine = pyttsx3.init()
engine.setProperty('voice', 'es')
# Variable que contiene texto a convertir en audio.
texto = "Esto se convertirá en audio"
# Guardar como mp3.
engine.save_to_file(texto, 'Audio_prueba1.mp3')
engine.runAndWait()