import os
import subprocess
import azure.cognitiveservices.speech as speechsdk
import threading
import json
import re
from difflib import SequenceMatcher
from transformers import pipeline
from diagnostico_audio import diagnostico_completo

# CONFIGURA TUS CLAVES Y DATOS
#YOUTUBE_URL = "https://www.youtube.com/watch?v=Sdb9yyA4W5k"
YOUTUBE_URL = "https://www.youtube.com/watch?v=j0UauyQYuGQ"
AUDIO_FILENAME = "output_audio.mp3"
WAV_FILENAME = "output_audio.wav"
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "tu_clave")
AZURE_REGION = "westus"
LANGUAGE = "es-ES"

# Configura tu ruta y claves
ruta_wav = "output_audio.wav"
azure_key = AZURE_SPEECH_KEY
azure_region = AZURE_REGION

def download_audio(url, output_file):
    print("Descargando audio de YouTube...")
    result = subprocess.run([
        "yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url
    ])
    if result.returncode != 0:
        raise Exception("Error al descargar audio con yt-dlp.")
    print("Audio descargado correctamente.")

def convert_mp3_to_wav(mp3_file, wav_file):
    print("Convirtiendo MP3 a WAV...")
    command = [
        "ffmpeg", "-y", "-i", mp3_file,
        "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", wav_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Error al convertir MP3 a WAV.")
    print("Conversión completada.")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.95

def transcribe_audio_detailed(ruta_wav, azure_key, azure_region, language="es-ES"):
    import azure.cognitiveservices.speech as speechsdk

    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
    speech_config.speech_recognition_language = language
    audio_input = speechsdk.AudioConfig(filename=ruta_wav)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    transcripcion_completa = []

    def handle_final_result(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcripcion_completa.append(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("⚠️ NoMatch: No se reconoció voz en un fragmento.")

    # def handle_cancel(evt):
    #     print("❌ Transcripción cancelada.")
    #     print(f"   Motivo: {evt.reason}")
    #     if evt.reason == speechsdk.CancellationReason.Error and evt.error_details:
    #         print(f"   Detalles: {evt.error_details}")

    speech_recognizer.recognized.connect(handle_final_result)
    # speech_recognizer.canceled.connect(handle_cancel)

    done = False
    def stop_cb(evt):
        nonlocal done
        done = True

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("▶️ Iniciando transcripción larga con Azure...")
    speech_recognizer.start_continuous_recognition()

    import time
    while not done:
        time.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()

    texto_final = " ".join(transcripcion_completa)
    if texto_final.strip():
        print("✅ Transcripción completa finalizada.")
    else:
        print("⚠️ Transcripción vacía.")
    return texto_final

def limpiar_y_formatear_dialogo(texto: str) -> str:
    dialogo = []
    for linea in texto.splitlines():
        if ":" in linea:
            orador, contenido = linea.split(":", 1)
            frases = re.split(r'(?<=[.?!])\s+', contenido.strip())
            for frase in frases:
                if frase:
                    dialogo.append(f"{orador.strip()}: {frase.strip()}")
    return "\n".join(dialogo)

def resumen_tematico(texto: str) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = [texto[i:i+1024] for i in range(0, len(texto), 1024)]
    resumenes = summarizer(chunks, max_length=300, min_length=100, do_sample=False)
    return "\n\n".join([r['summary_text'] for r in resumenes])

def generar_documento_presentacion(texto_dialogo: str, archivo="transcripcion_presentable.txt"):
    contenido = f"TRANSCRIPCIÓN LIMPIA\n\n{texto_dialogo}"
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"Documento generado: {archivo}")

def procesar_link(link, modo_salida="dialogo"):
    try:
        download_audio(link, AUDIO_FILENAME)
        convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME)

        # Diagnóstico completo antes de transcribir
        #diagnostico_completo(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION)

        texto_crudo = transcribe_audio_detailed(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE)

        if not texto_crudo:
            print("No se obtuvo texto.")
            return None

        if modo_salida == "dialogo":
            dialogo = limpiar_y_formatear_dialogo(texto_crudo)
            generar_documento_presentacion(dialogo)
            return dialogo

        elif modo_salida == "resumen":
            return resumen_tematico(texto_crudo)

        else:
            raise ValueError("Modo inválido. Usar 'dialogo' o 'resumen'.")

    except Exception as e:
        print(f"Error procesando el link: {e}")
        return None

if __name__ == "__main__":
    resultado = procesar_link(YOUTUBE_URL, modo_salida="dialogo")
    if resultado:
        print("\nResultado final:\n")
        print(resultado)
