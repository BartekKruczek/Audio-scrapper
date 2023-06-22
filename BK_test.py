# 1 - pobieranie linku w formie string z linku do yt

# import requests

# x = requests.get("https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt")
# print(x.url)

# 2 - pobieranie listy linków w postaci stringów z playlisty
# from youtubesearchpython import *
# import yt_dlp


# URLS = []

# try:
#     ydl_opts = {
#         "format": "m4a/bestaudio/best",
#         # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#         "postprocessors": [
#             {  # Extract audio using ffmpeg
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#             }
#         ],
#     }

#     playlistVideos = Playlist.getVideos(
#         "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq"
#     )

#     # wyodrębnianie url
#     for key in playlistVideos:
#         value = playlistVideos[key]
#         print(value)

#     for video in value:
#         url = video["link"]
#         # print(str(url))
#         URLS.append(str(url))
# except Exception:
#     print("Coś nie działa byczqu")
# finally:
#     for i in URLS:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             error_code = ydl.download(i)

# 3 - zatrzymywanie pętli
from youtubesearchpython import *
import yt_dlp

URLS = []

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

    playlistVideos = Playlist.getVideos(
        "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq"
    )

    # wyodrębnianie url
    for key in playlistVideos:
        value = playlistVideos[key]
        print(value)

    for video in value:
        url = video["link"]
        URLS.append(str(url))

except Exception:
    print("Coś nie działa byczqu")

finally:
    if len(URLS) > 0:
        for i in URLS:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(i)
                if error_code != 0:
                    break
    else:
        print("Brak URLS do pobrania")

# 4 - zatrzymanie pętli
# from youtubesearchpython import *
# import yt_dlp

# URLS = []

# try:
#     ydl_opts = {
#         "format": "m4a/bestaudio/best",
#         # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#         "postprocessors": [
#             {  # Extract audio using ffmpeg
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#             }
#         ],
#     }

#     playlistVideos = Playlist.getVideos(
#         "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq"
#     )

#     # wyodrębnianie url
#     for key in playlistVideos:
#         value = playlistVideos[key]
#         print(value)

#     for video in value:
#         url = video["link"]
#         URLS.append(str(url))

#     if len(URLS) > 0:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             error_code = ydl.download(URLS)
#             if error_code != 0:
#                 print("Błąd podczas pobierania.")
#     else:
#         print("Brak URLS do pobrania")

# except Exception as e:
#     print("Coś nie działa byczqu:", str(e))
