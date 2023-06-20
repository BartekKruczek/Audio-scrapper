# testowanie na użytek własny, ctr+c w terminalu -> terminate code PRZYDAJE SIE

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

# import yt_dlp

# URLS = [
#     "https://www.youtube.com/watch?v=BaW_jenozKc",
#     "https://www.youtube.com/watch?v=xpYw22NaMUc&ab_channel=PrzemekGórczykPodcast",
# ]

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
# except Exception:
#     print("Coś nie działa byczqu")
# finally:
#     for i in URLS:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             error_code = ydl.download(i)

# wersja 4 (pobieranie całej playlisty)

# import yt_dlp
# import os


# def download_playlist_audio(playlist_url, output_path):
#     ydl_opts = {
#         "format": "m4a/bestaudio/best",
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192",
#             }
#         ],
#         "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
#         "ignoreerrors": True,
#         "n_threads": 4,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         playlist_info = ydl.extract_info(playlist_url, download=False)
#         playlist_title = playlist_info["title"]
#         print(f"Pobieranie audio z playlisty: {playlist_title}")

#         for video in playlist_info["entries"]:
#             video_title = video["title"]
#             video_url = video["url"]

#             print(f"Pobieranie audio z filmu: {video_title}")

#             # Pobieranie pliku audio
#             ydl.download([video_url])


# # Przykładowe użycie funkcji dla playlisty na YouTube
# playlist_url = "https://youtube.com/playlist?list=PLJYMhYKidccNMcmNVIqpFLkmOAtKgIfu-"
# output_path = r"C:\Users\krucz\Documents\Projekty\Anonimowi-Akustycy\Nagrania"
# download_playlist_audio(playlist_url, output_path)

# wersja 5 (zwiększenie szybkości pobierania playlist)

import yt_dlp
import os

playlist_url = "https://youtube.com/playlist?list=PLJYMhYKidccNMcmNVIqpFLkmOAtKgIfu-"
output_path = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"

try:
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "ignoreerrors": True,
        "n_threads": 4,
    }
except Exception:
    print("Nie działa!")
finally:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        playlist_title = playlist_info["title"]
        print(f"Pobieranie audio z playlisty: {playlist_title}")

        for video in playlist_info["entries"]:
            video_title = video["title"]
            video_url = video["url"]

            print(f"Pobieranie audio z filmu: {video_title}")

            # Pobieranie pliku audio
            ydl.download([video_url])
