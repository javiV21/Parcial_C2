# Importar librería.
import pdfplumber

# Abrir el archivo del que se desea extraer el texto.
with pdfplumber.open("pdf_prueba3.pdf") as pdf:
        # Variable que guardará el texto.
        texto = ""
        # Ciclo para recorrer las páginas del pdf.
        for pagina in pdf.pages:
            texto += pagina.extract_text()
# Ver el contenido extraído.
print(texto)