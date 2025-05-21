import spacy

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Leer el contenido del archivo de texto
with open('transcripcion.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Procesar el texto con spaCy
doc = nlp(texto)

# Mostrar los resultados: Intervenciones y etiquetas gramaticales
for sent in doc.sents:
    print(f"Intervención: {sent.text.strip()}")
    for token in sent:
        print(f"{token.text} - {token.pos_} - {token.dep_}")
    print("\n")
