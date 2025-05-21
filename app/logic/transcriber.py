import azure.cognitiveservices.speech as speechsdk
import threading
from app.config import AZURE_SPEECH_KEY, AZURE_REGION, LANGUAGE

def transcribe_audio_dialogo(file_path: str) -> str:
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    speech_config.speech_recognition_language = LANGUAGE
    audio_input = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    transcriptions = []
    stop_event = threading.Event()
    orador_flag = True

    def recognized_handler(evt):
        nonlocal orador_flag
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            orador = "Orador 1" if orador_flag else "Orador 2"
            transcriptions.append(f"{orador}: {evt.result.text.strip()}")
            orador_flag = not orador_flag

    recognizer.recognized.connect(recognized_handler)
    recognizer.session_stopped.connect(lambda evt: stop_event.set())
    recognizer.start_continuous_recognition()
    stop_event.wait()
    recognizer.stop_continuous_recognition()

    return "\n".join(transcriptions)
