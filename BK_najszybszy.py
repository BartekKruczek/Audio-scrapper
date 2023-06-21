# wersja 1
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
video = ""
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
except Exception:
    print("Coś nie działa!")
finally:
    # pobieranie linków z całej playlisty
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_urls, download=False)

        if "entries" in result:
            video = result["entries"]

            for i, item in enumerate(video):
                video = result["entries"][i]

    print(str(video))

# wersja 2
# import os
# import requests

# playlist_url = "https://www.youtube.com/watch?v=BaW_jenozKc"
# output_path = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"
# URLS = []

# try:
#     response = requests.get(
#         f"https://www.youtube.com/playlist_ajax?list={playlist_url}"
#     )
#     playlist_data = response.json()
#     videos = playlist_data["video"]

#     for video in videos:
#         video_url = f"https://www.youtube.com/watch?v={video['encrypted_id']}"
#         URLS.append(video_url)

# except Exception as e:
#     print(f"Wystąpił błąd: {str(e)}")

# print(URLS)