import yt_dlp
import os

# URLS = [
#     "https://www.youtube.com/watch?v=BaW_jenozKc",
#     "https://www.youtube.com/watch?v=xpYw22NaMUc&ab_channel=PrzemekGórczykPodcast",
# ]

output = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"
playlist_urls = "https://www.youtube.com/watch?v=BaW_jenozKc"
URLS = (
    []
)  # chcemy dodać tu wszystkie linki z playlistu, potem w pętli z tąd wszystko pobrać

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
        "quiet": True,
    }

    # pobieranie linków z całej playlisty
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_urls, download=False)

        # for link in playlist_info

except Exception:
    print("Coś nie działa byczqu")
finally:
    for i in URLS:
        error_code = ydl.download(i)
