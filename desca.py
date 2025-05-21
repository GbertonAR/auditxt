import requests

def descargar_audio(url, destino):
    response = requests.get(url)
    with open(destino, 'wb') as f:
        f.write(response.content)
    return destino

# Prueba con una URL real de audio
#url_audio = "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav"  # Archivo de prueba (público)
url_audio = "https://www.youtube.com/watch?v=eTuAblf6ako"
archivo_destino = "starwars.wav"

descargar_audio(url_audio, archivo_destino)