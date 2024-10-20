import pdfplumber
import pyttsx3
import os
from tkinter import messagebox, Text, Tk, Button, Label, Scrollbar, VERTICAL, END

# Variable global para almacenar el nombre del último archivo de audio generado
ultimo_audio_generado = None

# Ruta del archivo PDF en la carpeta Descargas
ruta_pdf = "Cuento Corto.pdf"  # Ruta actualizada

# Inicializar pyttsx3
engine = pyttsx3.init()

# Función para leer el PDF predefinido y convertirlo a voz
def leer_pdf_predefinido(pdf_path):
    global ultimo_audio_generado
    try:
        with pdfplumber.open(pdf_path) as pdf:
            texto_completo = ""
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo += texto
                else:
                    print("No se pudo extraer texto de esta página.")
        
        if texto_completo:
            texto_area.delete(1.0, END)
            texto_area.insert(END, texto_completo)
            
            engine.save_to_file(texto_completo, 'Audio1_interfaz.mp3')
            engine.runAndWait()
            ultimo_audio_generado = "Audio1_interfaz.mp3"
            
            messagebox.showinfo("Éxito", f"El audio del PDF ha sido generado y guardado como '{ultimo_audio_generado}'.")
        else:
            messagebox.showerror("Error", "El PDF no contiene texto legible.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al leer el PDF.\n{e}")

# Función para convertir texto ingresado a voz
def leer_texto_manual():
    global ultimo_audio_generado
    texto = texto_area.get(1.0, END).strip()
    if texto:
        try:
            engine.save_to_file(texto, 'Audio2_interfaz.mp3')
            engine.runAndWait()
            ultimo_audio_generado = "Audio2_interfaz.mp3"
            messagebox.showinfo("Éxito", f"El audio ha sido generado y guardado como '{ultimo_audio_generado}'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo convertir el texto a voz.\n{e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa algún texto para convertirlo a voz.")

# Función para reproducir el último audio generado
def escuchar_audio():
    if ultimo_audio_generado and os.path.exists(ultimo_audio_generado):
        try:
            os.system(f"start {ultimo_audio_generado}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reproducir el archivo de audio.\n{e}")
    else:
        messagebox.showwarning("Advertencia", "No se ha generado ningún audio para escuchar.")

# Prueba básica para verificar si la conversión de texto a voz funciona correctamente
def prueba_texto_a_voz():
    texto_de_prueba = "Hola, este es un texto de prueba para convertir a audio y reproducir."
    engine.save_to_file(texto_de_prueba, 'prueba_audio.mp3')
    engine.runAndWait()

    if os.path.exists('prueba_audio.mp3'):
        os.system(f"start prueba_audio.mp3")
    else:
        messagebox.showerror("Error", "No se pudo generar el archivo de audio de prueba.")

# Crear la ventana principal
ventana = Tk()
ventana.title("Lector de Cuentos - Texto a Voz")
ventana.geometry("600x500")

# Cambiar color de fondo
ventana.configure(bg="#ADD8E6")  # Color azul claro de fondo

# Etiqueta de título
label_titulo = Label(ventana, text="Lector de Cuentos - Texto a Voz", font=("Arial", 18, "bold"), fg="#FFFFFF", bg="#4682B4")
label_titulo.pack(pady=15)

# Botón para leer el PDF predefinido (con colores y borde redondeado)
boton_pdf = Button(ventana, text="Leer texto del pdf", command=lambda: leer_pdf_predefinido(ruta_pdf), font=("Arial", 12, "bold"), bg="#2920bb", fg="#FFFFFF", activebackground="#FF6347", relief="groove", bd=4)
boton_pdf.pack(pady=10)

# Cuadro de texto con scrollbar
scrollbar = Scrollbar(ventana, orient=VERTICAL)
texto_area = Text(ventana, wrap="word", yscrollcommand=scrollbar.set, height=10, font=("Arial", 12), bg="#F5F5DC", fg="#000000", relief="solid", bd=2)
scrollbar.config(command=texto_area.yview)
scrollbar.pack(side="right", fill="y")
texto_area.pack(pady=10, padx=10)

# Botón para leer el texto ingresado manualmente
boton_leer_texto = Button(ventana, text="Leer texto", command=leer_texto_manual, font=("Arial", 12, "bold"), bg="#8A2BE2", fg="#FFFFFF", activebackground="#FFA500", relief="groove", bd=4)
boton_leer_texto.pack(pady=10)

# Botón para reproducir el último audio generado
boton_escuchar = Button(ventana, text="Escuchar audio", command=escuchar_audio, font=("Arial", 12, "bold"), bg="#8A2BE2", fg="#FFFFFF", activebackground="#32CD32", relief="groove", bd=4)
boton_escuchar.pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()