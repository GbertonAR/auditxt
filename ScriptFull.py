import os
import subprocess
import azure.cognitiveservices.speech as speechsdk
import threading

# CONFIGURA TUS CLAVES Y DATOS
YOUTUBE_URL = "https://www.youtube.com/watch?v=UNKCDLmQEw4"  # ← Reemplaza con tu URL
AUDIO_FILENAME = "output_audio.mp3"
WAV_FILENAME = "output_audio.wav"
AZURE_SPEECH_KEY = "5HlXtb6RGzYmKEkoKMQYrg0FS9XmcbfruyiJlHYCnaTAoBv8YDhvJQQJ99BEAC4f1cMXJ3w3AAAYACOGovY5"
AZURE_REGION = "westus"  # ej: "eastus"
LANGUAGE = "es-ES"  # Cambia a tu idioma si es necesario

# # PASO 1: Descargar audio desde YouTube usando yt-dlp
# def download_audio(url, output_file):
#     print("Descargando audio de YouTube...")
#     result = subprocess.run([
#         "yt-dlp",
#         "-x", "--audio-format", "mp3",
#         "-o", output_file,
#         url
#     ])
#     if result.returncode == 0:
#         print("Audio descargado correctamente.")
#     else:
#         raise Exception("Error al descargar audio con yt-dlp.")

# # PASO 2: Convertir MP3 a WAV compatible con Azure
# def convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME):
#     print("Convirtiendo MP3 a WAV...")
#     result = subprocess.run([
#         "ffmpeg",
#         "-i", AUDIO_FILENAME,
#         "-ar", "16000",
#         "-ac", "1",
#         "-acodec", "pcm_s16le",
#         WAV_FILENAME
#     ])
#     if result.returncode == 0:
#         print("Conversión completada.")
#     else:
#         raise Exception("Error al convertir MP3 a WAV con ffmpeg.")

# # PASO 3: Transcribir el audio con Azure
# def transcribe_audio(file_path, speech_key, region, language="es-ES"):
#     print("Transcribiendo audio...")
#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
#     speech_config.speech_recognition_language = language
#     audio_input = speechsdk.audio.AudioConfig(filename=file_path)
#     recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

#     result = recognizer.recognize_once()

#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         print("Transcripción:")
#         print(result.text)
#         return result.text
#     elif result.reason == speechsdk.ResultReason.NoMatch:
#         print("No se reconoció ningún discurso.")
#     else:
#         print(f"Error: {result.reason}")
#         print(f"Detalles: {result.cancellation_details.error_details}")

#     return ""

# # PASO 4: Guardar la transcripción en un archivo de texto
# def guardar_transcripcion(texto, archivo="transcripcion.txt"):
#     with open(archivo, "w", encoding="utf-8") as f:
#         f.write(texto)
#     print(f"Transcripción guardada en {archivo}")

# # Ejecutar flujo completo
# if __name__ == "__main__":
#     try:
#         download_audio(YOUTUBE_URL, AUDIO_FILENAME)
#         convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME)
#         texto = transcribe_audio(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE)
#         if texto:
#             guardar_transcripcion(texto)
#     except Exception as e:
#         print(f"Ocurrió un error: {e}")

# PASO 1: Descargar audio desde YouTube usando yt-dlp
def download_audio(url, output_file):
    print("Descargando audio de YouTube...")
    result = subprocess.run([
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_file,
        url
    ])
    if result.returncode == 0:
        print("Audio descargado correctamente.")
    else:
        raise Exception("Error al descargar audio con yt-dlp.")

# PASO 2: Convertir MP3 a WAV (mono, 16kHz, PCM)
def convert_mp3_to_wav(mp3_file, wav_file):
    print("Convirtiendo MP3 a WAV...")
    command = [
        "ffmpeg",
        "-y",  # sobrescribir sin preguntar
        "-i", mp3_file,
        "-ac", "1",  # mono
        "-ar", "16000",  # 16 kHz
        "-sample_fmt", "s16",  # PCM 16 bits
        wav_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Conversión completada.")
    else:
        print(result.stderr.decode())
        raise Exception("Error al convertir MP3 a WAV.")

# PASO 3: Transcribir el audio con reconocimiento continuo de Azure
def transcribe_audio_continuous(file_path, speech_key, region, language="es-ES"):
    print("Transcribiendo audio con reconocimiento continuo...")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language = language
    audio_input = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # Lista para almacenar los resultados de la transcripción
    transcriptions = []

    # Evento para manejar los resultados reconocidos
    def recognized_handler(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Reconocido: {evt.result.text}")
            transcriptions.append(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No se reconoció ningún discurso.")

    # Evento para manejar errores de cancelación
    def canceled_handler(evt):
        print(f"Reconocimiento cancelado: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Detalles del error: {evt.error_details}")

    # Evento para indicar que el reconocimiento ha finalizado
    def session_stopped_handler(evt):
        print("Reconocimiento finalizado.")
        stop_event.set()

    # Conectar los manejadores de eventos
    recognizer.recognized.connect(recognized_handler)
    recognizer.canceled.connect(canceled_handler)
    recognizer.session_stopped.connect(session_stopped_handler)

    # Iniciar el reconocimiento continuo
    stop_event = threading.Event()
    recognizer.start_continuous_recognition()
    stop_event.wait()  # Esperar hasta que el reconocimiento finalice
    recognizer.stop_continuous_recognition()

    # Unir las transcripciones en un solo texto
    full_transcription = ' '.join(transcriptions)
    return full_transcription

# PASO 4: Guardar la transcripción en un archivo de texto
def guardar_transcripcion(texto, archivo="transcripcion.txt"):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Transcripción guardada en {archivo}")

# Ejecutar flujo completo
if __name__ == "__main__":
    try:
        download_audio(YOUTUBE_URL, AUDIO_FILENAME)
        convert_mp3_to_wav(AUDIO_FILENAME, WAV_FILENAME)
        texto = transcribe_audio_continuous(WAV_FILENAME, AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE)
        if texto:
            guardar_transcripcion(texto)
    except Exception as e:
        print(f"Ocurrió un error: {e}")