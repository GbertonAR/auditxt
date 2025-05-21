import spacy
import re

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Leer el contenido del archivo
with open('./transcripcion.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Lista de nombres o frases comunes que indican cambio de interlocutor
nombres = ["Adrián", "Andrés", "Adri", "Contanos", "Gracias"]

# Convertir lista de nombres en expresión regular para detección eficiente
patron_nombres = re.compile(rf"^({'|'.join(map(re.escape, nombres))})(\b|:)", re.IGNORECASE)

# Procesar texto con spaCy y dividir en oraciones
doc = nlp(texto)
oraciones = [sent.text.strip() for sent in doc.sents]

# Inicializamos variables
lineas = []
hablante_actual = None
buffer = ""

for frase in oraciones:
    match = patron_nombres.match(frase)
    if match:
        # Si encontramos un nuevo hablante, guardamos el anterior
        if buffer:
            lineas.append(f"{hablante_actual}: {buffer.strip()}" if hablante_actual else buffer.strip())
        hablante_actual = match.group(1)
        buffer = frase[len(match.group(0)):].strip()
    else:
        buffer += " " + frase

# Guardar la última línea
if buffer:
    lineas.append(f"{hablante_actual}: {buffer.strip()}" if hablante_actual else buffer.strip())

# Imprimir resultado
print("🗣️ Diálogo formateado:\n")
for linea in lineas:
    print(linea)
