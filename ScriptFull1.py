import os
import subprocess
import azure.cognitiveservices.speech as speechsdk
import threading

# CONFIGURA TUS CLAVES Y DATOS
YOUTUBE_URL = "https://www.youtube.com/watch?v=Sdb9yyA4W5k"  # ← Reemplaza con tu URL
AUDIO_FILENAME = "output_audio.mp3"
WAV_FILENAME = "output_audio.wav"
AZURE_SPEECH_KEY = "5HlXtb6RGzYmKEkoKMQYrg0FS9XmcbfruyiJlHYCnaTAoBv8YDhvJQQJ99BEAC4f1cMXJ3w3AAAYACOGovY5"
AZURE_REGION = "westus"  # ej: "eastus"
LANGUAGE = "es-ES"  # Cambia a tu idioma si es necesario

# PASO 1: Descargar audio desde YouTube
def download_audio(url, output_file):
    print("Descargando audio de YouTube...")
    result = subprocess.run([
        "yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url
    ])
    if result.returncode == 0:
        print("Audio descargado correctamente.")
    else:
        raise Exception("Error al descargar audio con yt-dlp.")

# PASO 2: Convertir MP3 a WAV
def convert_mp3_to_wav(mp3_file, wav_file):
    print("Convirtiendo MP3 a WAV...")
    command = [
        "ffmpeg", "-y", "-i", mp3_file,
        "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", wav_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Conversión completada.")
    else:
        print(result.stderr.decode())
        raise Exception("Error al convertir MP3 a WAV.")

# PASO 3: Transcripción con alternancia de oradores
def transcribe_audio_dialogo(file_path, speech_key, region, language="es-ES"):
    print("Transcribiendo audio con Azure...")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language = language
    audio_input = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    transcriptions = []
    stop_event = threading.Event()
    orador_flag = True  # alterna entre oradores

    def recognized_handler(evt):
        nonlocal orador_flag
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            texto = evt.result.text.strip()
            if texto:
                orador = "Orador 1" if orador_flag else "Orador 2"
                transcriptions.append(f"{orador}: {texto}")
                orador_flag = not orador_flag

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

# PASO 4: Guardar en archivo
def guardar_transcripcion(texto, archivo="transcripcion.txt"):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Transcripción guardada en {archivo}")

def procesar_link(link):
    try:
        download_audio(link, AUDIO_FILENAME)
        convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME)
        texto = transcribe_audio_dialogo(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE)
        if texto:
            guardar_transcripcion(texto)
        return texto
    except Exception as e:
        print(f"Ocurrió un error al procesar el link: {e}")
        return None

# FLUJO COMPLETO
if __name__ == "__main__":
    # Solo para pruebas locales
    resultado = procesar_link("https://www.youtube.com/watch?v=Sdb9yyA4W5k")
    if resultado:
        print("Transcripción de prueba:")
        print(resultado)
    # try:
    #     download_audio(YOUTUBE_URL, AUDIO_FILENAME)
    #     convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME)
    #     texto = transcribe_audio_dialogo(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE)
    #     if texto:
    #         guardar_transcripcion(texto)
    # except Exception as e:
    #     print(f"Ocurrió un error: {e}")
