# testowanie na użytek własny
# from __future__ import unicode_literals
# import youtube_dl

# podejście nr 1

# ydl_opts = {
#     "format": "bestaudio/best",
#     "postprocessors": [
#         {
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": "mp3",
#             "preferredquality": "192",
#         }
#     ],
# }
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(["http://www.youtube.com/watch?v=BaW_jenozKc"])

# podejście nr 2 (yt-dlp)

import yt_dlp

URLS = [
    "https://www.youtube.com/watch?v=BaW_jenozKc",
    "https://www.youtube.com/watch?v=xpYw22NaMUc&ab_channel=PrzemekGórczykPodcast",
]

try:
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "ignoreerrors": True,
    }
except Exception:
    print("Coś nie działa byczqu")
finally:
    for i in URLS:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(i)
