from fastapi import APIRouter, Form
from app.logic.downloader import download_youtube_audio, convert_mp3_to_wav
from app.logic.transcriber import transcribe_audio_dialogo
from app.logic.formatter import format_text
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.post("/transcribir")
async def transcribir(link: str = Form(...)):
    mp3_file = "audio.mp3"
    wav_file = "audio.wav"

    download_youtube_audio(link, mp3_file)
    convert_mp3_to_wav(mp3_file, wav_file)

    texto = transcribe_audio_dialogo(wav_file)
    texto_formateado = format_text(texto)

    return {"resultado": texto_formateado}


@router.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Bienvenido a Auditxt</title>
        <style>
            body {
                background: linear-gradient(135deg, #0077ff, #00c3ff);
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                font-size: 3em;
            }
            p {
                font-size: 1.5em;
            }
            a {
                margin-top: 20px;
                background: white;
                color: #0077ff;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }
            a:hover {
                background: #e0e0e0;
            }
        </style>
    </head>
    <body>
        <h1>¡Bienvenido a Auditxt!</h1>
        <p>API para transcripción inteligente desde audio o YouTube</p>
        <a href="/docs">Ir a la documentación</a>
    </body>
    </html>
    """

