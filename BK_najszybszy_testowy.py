import yt_dlp
import os

output = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"

ydl = yt_dlp.YoutubeDL(
    {
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
)
video = ""
yt_url = "https://www.youtube.com/watch?v=BaW_jenozKc"

with ydl:
    result = ydl.extract_info(
        yt_url, download=False
    )  # We just want to extract the info

    if "entries" in result:
        # Can be a playlist or a list of videos
        video = result["entries"]

        # loops entries to grab each video_url
        for i, item in enumerate(video):
            video = result["entries"][i]
