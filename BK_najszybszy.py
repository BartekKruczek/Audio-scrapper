import yt_dlp
import os

URLS = [
    "https://www.youtube.com/watch?v=BaW_jenozKc",
    "https://www.youtube.com/watch?v=xpYw22NaMUc&ab_channel=PrzemekGórczykPodcast",
]
output = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"


try:
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(
            output, "%(title)s.%(ext)s"
        ),  # zewnętrzna ścieżka zapisu
        "ignoreerrors": True,
    }
except Exception:
    print("Coś nie działa byczqu")
finally:
    for i in URLS:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(i)
