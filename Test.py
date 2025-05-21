import azure.cognitiveservices.speech as speechsdk

clave1 = "https://westus.api.cognitive.microsoft.com/
clave = "WjLxIy0kMKmebYud4wE3oJA8RIzd1632JKIsJhg1hgCqrPr78ZsIJQQJ99BEAC4f1cMXJ3w3AAAYACOGl4TH"
region = "eastus"

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
        print("Transcripción cancelada:", cancel_details.reason)
        if cancel_details.reason == speechsdk.CancellationReason.Error:
            print("Detalles del error:", cancel_details.error_details)

# Ejemplo de uso
# Sustituye con tu archivo local .wav, clave y región válidos
# transcribir_audio_local("audio.wav", "TU_CLAVE", "TU_REGION")

