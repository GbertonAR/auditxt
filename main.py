from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import openai
import shutil
import tempfile
from ScriptFull1 import procesar_link
from formatear2 import formatear

app = FastAPI()

# Configuración de CORS (opcional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar por seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Azure OpenAI
openai.api_type = "azure"
openai.api_base = "https://<TU-RESOURCE-NAME>.openai.azure.com/"
openai.api_version = "2023-09-01"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/transcribir")
async def transcribir(link: str = Form(None), archivo: UploadFile = File(None)):
    if not link and not archivo:
        raise HTTPException(status_code=400, detail="Se requiere un archivo o un link.")

    if link:
        try:
            texto = procesar_link(link)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando el link: {str(e)}")
    elif archivo:
        try:
            # Crear archivo temporal
            filename = os.path.join(UPLOAD_FOLDER, archivo.filename)
            with open(filename, "wb") as buffer:
                shutil.copyfileobj(archivo.file, buffer)

            with open(filename, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    file=audio_file,
                    model="whisper"
                )
            texto = transcript["text"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(e)}")

    # Formatear resultado
    try:
        texto_formateado = formatear(texto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en formatear2: {str(e)}")

    return JSONResponse(content={"resultado": texto_formateado})
