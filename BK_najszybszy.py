import yt_dlp

URLS = [
    "https://www.youtube.com/watch?v=BaW_jenozKc",
    "https://www.youtube.com/watch?v=xpYw22NaMUc&ab_channel=PrzemekGórczykPodcast",
]

try:
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }
except Exception:
    print("Coś nie działa byczqu")
finally:
    for i in URLS:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(i)
