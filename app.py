from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
import tempfile
from ScriptFull1 import procesar_link
#from formatear2 import formatear

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Configuración de Azure OpenAI
# openai.api_type = "azure"
# openai.api_base = "https://<TU-RESOURCE-NAME>.openai.azure.com/"
# openai.api_version = "2023-09-01"
# openai.api_key = os.getenv("AZURE_OPENAI_KEY")


@app.route('/transcribir', methods=['POST'])
def transcribir():
    link = request.form.get('link')
    archivo = request.files.get('archivo')

    if not link and not archivo:
        return jsonify({'error': 'Se requiere un archivo o un link'}), 400

    if link:
        # Procesar con Scriptfull1.py
        texto = procesar_link(link)
    elif archivo:
        filename = secure_filename(archivo.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(file_path)

        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                file=audio_file,
                model="whisper",  # tu deployment en Azure
            )
        texto = transcript['text']

    # Procesar con formatear2.py
    #texto_formateado = formatear(texto)
    texto_formateado = texto

    return jsonify({"resultado": texto_formateado})


if __name__ == '__main__':
    app.run(debug=True)
