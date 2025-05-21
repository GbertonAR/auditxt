import requests
import time
import json

# Datos
AZURE_SPEECH_KEY = "5HlXtb6RGzYmKEkoKMQYrg0FS9XmcbfruyiJlHYCnaTAoBv8YDhvJQQJ99BEAC4f1cMXJ3w3AAAYACOGovY5"
AZURE_REGION = "westus"
AUDIO_URL = "https://tu_blob_storage/output_audio.wav"  # Audio debe estar en blob público o SAS URL

endpoint = f"https://{AZURE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions"

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
    "Content-Type": "application/json"
}

body = {
    "contentUrls": [AUDIO_URL],
    "locale": "es-ES",
    "displayName": "Transcripcion con diarización",
    "properties": {
        "diarizationEnabled": True,
        "wordLevelTimestampsEnabled": True,
        "punctuationMode": "DictatedAndAutomatic"
    }
}

# Crear transcripción batch
print("Creando transcripción batch con diarización...")
response = requests.post(endpoint, headers=headers, json=body)
if response.status_code != 202:
    print("Error al crear la transcripción batch:", response.text)
    exit(1)

transcription_url = response.headers["Location"]
print(f"Transcripción creada. URL de seguimiento: {transcription_url}")

# Esperar a que termine la transcripción (polling)
while True:
    r = requests.get(transcription_url, headers=headers)
    status = r.json().get("status")
    print(f"Estado de la transcripción: {status}")
    if status in ("Succeeded", "Failed"):
        break
    time.sleep(15)

if status == "Succeeded":
    # Obtener resultados
    results_url = r.json()["resultsUrls"]["channel_0"]  # Usualmente un JSON con diarización y palabras
    results_response = requests.get(results_url)
    results_json = results_response.json()

    # Aquí puedes parsear y mostrar resultados con diarización
    print("Resultados de la transcripción con diarización:")
    for segment in results_json.get("combinedRecognizedPhrases", []):
        print(f"{segment['speakerId']} ({segment['offset']}-{segment['offset'] + segment['duration']}): {segment['display']}")

else:
    print("La transcripción falló.")
