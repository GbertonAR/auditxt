import os
import subprocess
import azure.cognitiveservices.speech as speechsdk
import threading
import json

# CONFIGURA TUS CLAVES Y DATOS
#YOUTUBE_URL = "https://www.youtube.com/watch?v=Sdb9yyA4W5k"  # ← Reemplaza con tu URL
YOUTUBE_URL = "https://www.youtube.com/watch?v=pQhWE1cOPSg"
AUDIO_FILENAME = "output_audio.mp3"
WAV_FILENAME = "output_audio.wav"
AZURE_SPEECH_KEY = "5HlXtb6RGzYmKEkoKMQYrg0FS9XmcbfruyiJlHYCnaTAoBv8YDhvJQQJ99BEAC4f1cMXJ3w3AAAYACOGovY5"
AZURE_REGION = "westus"
LANGUAGE = "es-ES"

def download_audio(url, output_file):
    print("Descargando audio de YouTube...")
    result = subprocess.run([
        "yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url
    ])
    if result.returncode == 0:
        print("Audio descargado correctamente.")
    else:
        raise Exception("Error al descargar audio con yt-dlp.")

def convert_mp3_to_wav(mp3_file, wav_file):
    print("Convirtiendo MP3 a WAV...")
    command = [
    "ffmpeg", "-y", "-i", mp3_file,
    "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", wav_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Conversión completada.")
    else:
        print(result.stderr.decode())
        raise Exception("Error al convertir MP3 a WAV.")

def transcribe_audio_detailed(file_path, speech_key, region, language="es-ES"):
    print("Transcribiendo audio con Azure (salida detallada)...")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language = language
    speech_config.output_format = speechsdk.OutputFormat.Detailed

    audio_input = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    transcriptions = []
    stop_event = threading.Event()
    orador_flag = True

    def recognized_handler(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            result_json = json.loads(evt.result.json)
            for nbest in result_json.get("NBest", []):
                display_text = nbest.get("Display", "")
                nonlocal orador_flag
                orador = "Orador 1" if orador_flag else "Orador 2"
                orador_flag = not orador_flag
                transcriptions.append(f"{orador}: {display_text}")

    def canceled_handler(evt):
        print(f"Reconocimiento cancelado: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Detalles del error: {evt.error_details}")

    def session_stopped_handler(evt):
        print("Reconocimiento finalizado.")
        stop_event.set()

    recognizer.recognized.connect(recognized_handler)
    recognizer.canceled.connect(canceled_handler)
    recognizer.session_stopped.connect(session_stopped_handler)

    recognizer.start_continuous_recognition()
    stop_event.wait()
    recognizer.stop_continuous_recognition()

    return "\n".join(transcriptions)

def transcripcion_a_dialogo(texto: str) -> str:
    import re
    lineas = texto.splitlines()
    dialogo = []
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        if ":" in linea:
            orador, contenido = linea.split(":", 1)
            frases = re.split(r'(?<=[.?!])\s+', contenido.strip())
            for frase in frases:
                if frase:
                    dialogo.append(f"{orador.strip()}: {frase.strip()}")
        else:
            dialogo.append(linea)
    return "\n".join(dialogo)

def resumen_tematico(texto: str) -> str:
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = [texto[i:i+1024] for i in range(0, len(texto), 1024)]
    resumenes = summarizer(chunks, max_length=300, min_length=100, do_sample=False)
    return "\n\n".join([r['summary_text'] for r in resumenes])

def procesar_transcripcion(texto_crudo: str, modo: str = "dialogo") -> str:
    if modo == "dialogo":
        return transcripcion_a_dialogo(texto_crudo)
    elif modo == "resumen":
        return resumen_tematico(texto_crudo)
    else:
        raise ValueError("Modo inválido. Usar 'dialogo' o 'resumen'.")

def guardar_transcripcion(texto, archivo="transcripcion2_final.txt"):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Transcripción guardada en {archivo}")

def procesar_link(link, modo_salida="dialogo"):
    try:
        download_audio(link, AUDIO_FILENAME)
        convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME)
        texto_crudo = transcribe_audio_detailed(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE)
        if texto_crudo:
            texto_procesado = procesar_transcripcion(texto_crudo, modo=modo_salida)
            guardar_transcripcion(texto_procesado)
            return texto_procesado
    except Exception as e:
        print(f"Ocurrió un error al procesar el link: {e}")
        return None

if __name__ == "__main__":
    modo = "dialogo"  # Cambiar a "resumen" si se desea salida resumida
    resultado = procesar_link(YOUTUBE_URL, modo_salida=modo)
    if resultado:
        print(f"\nTranscripción procesada en modo '{modo}':\n")
        print(resultado)
