import subprocess

def download_youtube_audio(url: str, output_file: str):
    result = subprocess.run([
        "yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url
    ])
    if result.returncode != 0:
        raise Exception("Error al descargar el audio")

def convert_mp3_to_wav(mp3_file: str, wav_file: str):
    result = subprocess.run([
        "ffmpeg", "-y", "-i", mp3_file, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", wav_file
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Error al convertir MP3 a WAV")
