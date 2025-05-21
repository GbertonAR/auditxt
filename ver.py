# import requests
# import azure.cognitiveservices.speech as speechsdk

# # Parámetros: completá con los tuyos
# URL_AUDIO = "https://www.youtube.com/watch?v=eTuAblf6ako"
# URL_AUDIO = "https://github.com/Azure-Samples/cognitive-services-speech-sdk/raw/master/samples/cpp/windows/console/samples/audiofiles/whatstheweatherlike.wav"

# ARCHIVO_DESTINO = "audio.wav"
# CLAVE_AZURE = "WjLxIy0kMKmebYud4wE3oJA8RIzd1632JKIsJhg1hgCqrPr78ZsIJQQJ99BEAC4f1cMXJ3w3AAAYACOGl4TH"
# REGION_AZURE = "eastus"  # Ej: "eastus" o "westeurope"

# def descargar_audio(url, destino):
#     try:
#         print("Descargando audio...")
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         with open(destino, 'wb') as f:
#             f.write(response.content)
#         print(f"Audio descargado en: {destino}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error al descargar el archivo: {e}")
#         exit(1)

# def transcribir_audio_local(ruta_archivo, clave, region):
#     speech_config = speechsdk.SpeechConfig(subscription=clave, region=region)
#     audio_config = speechsdk.AudioConfig(filename=ruta_archivo)
#     recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

#     print("Transcribiendo...")
#     resultado = recognizer.recognize_once()

#     if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
#         print("Texto reconocido:", resultado.text)
#     elif resultado.reason == speechsdk.ResultReason.NoMatch:
#         print("No se reconoció voz.")
#     elif resultado.reason == speechsdk.ResultReason.Canceled:
#         cancel_details = resultado.cancellation_details
#         print("Cancelado:", cancel_details.reason)

# # Ejecutar todo
# descargar_audio(URL_AUDIO, ARCHIVO_DESTINO)
# transcribir_audio_local(ARCHIVO_DESTINO, CLAVE_AZURE, REGION_AZURE)


import os
import requests
import subprocess
import azure.cognitiveservices.speech as speechsdk

# Configuración
# URL_AUDIO = "https://github.com/Azure-Samples/cognitive-services-speech-sdk/raw/master/samples/cpp/windows/console/samples/audiofiles/whatstheweatherlike.wav"
URL_AUDIO = "https://www.youtube.com/watch?v=gaRCjaDra-U"
ARCHIVO_ORIGINAL = "audio_original.wav"
ARCHIVO_CONVERTIDO = "audio_convertido.wav"
# CLAVE_AZURE = "TU_CLAVE_AQUI"
# REGION_AZURE = "TU_REGION_AQUI"
CLAVE_AZURE = "WjLxIy0kMKmebYud4wE3oJA8RIzd1632JKIsJhg1hgCqrPr78ZsIJQQJ99BEAC4f1cMXJ3w3AAAYACOGl4TH"
REGION_AZURE = "eastus"  # Ej: "eastus" o "westeurope"

def descargar_audio(url, destino):
    print("Descargando audio...")
    response = requests.get(url)
    with open(destino, 'wb') as f:
        f.write(response.content)
    print("Audio descargado en:", destino)
    return destino

def convertir_audio(origen, destino_convertido):
    print("Convirtiendo audio a formato compatible con Azure...")
    comando = [
        "ffmpeg", "-y", "-i", origen,
        "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", destino_convertido
    ]
    subprocess.run(comando, check=True)
    print("Audio convertido en:", destino_convertido)

def transcribir_audio_local(ruta_archivo, clave, region):
    speech_config = speechsdk.SpeechConfig(subscription=clave, region=region)
    audio_config = speechsdk.AudioConfig(filename=ruta_archivo)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Transcribiendo...")
    resultado = recognizer.recognize_once()

    if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Texto reconocido:", resultado.text)
    elif resultado.reason == speechsdk.ResultReason.NoMatch:
        print("No se reconoció voz.")
    elif resultado.reason == speechsdk.ResultReason.Canceled:
        cancel_details = resultado.cancellation_details
        print("Cancelado:", cancel_details.reason)

# Ejecución
descargar_audio(URL_AUDIO, ARCHIVO_ORIGINAL)
convertir_audio(ARCHIVO_ORIGINAL, ARCHIVO_CONVERTIDO)
transcribir_audio_local(ARCHIVO_CONVERTIDO, CLAVE_AZURE, REGION_AZURE)

