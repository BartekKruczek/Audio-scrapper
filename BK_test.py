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

# except Exception:
#     print("Coś nie działa byczqu")

# finally:
#     if len(URLS) > 0:
#         for i in URLS:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 error_code = ydl.download(i)
#                 if error_code != 0:
#                     break
#     else:
#         print("Brak URLS do pobrania")

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

# test transkrypcji
import yt_dlp
import os
import random
import webvtt
import time
import glob
from youtubesearchpython import *
import requests
import webvtt
from youtube_transcript_api import YouTubeTranscriptApi

try:
    kompendium = {}
    URLS = []
    Ids = []

    def download_playlist_audio(playlist_url, output_path, download):
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
                output_path, "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s"
            ),
            "ignoreerrors": True,
            "n_threads": 4,
        }

        playlistVideos = Playlist.getVideos(playlist_url)

        # wyodrębnianie url
        for key in playlistVideos:
            value = playlistVideos[key]
            # print(value)

        for video in value:
            url = video["link"]
            URLS.append(str(url))

        # pobieranie
        if download == True:
            if len(URLS) > 0:
                for i in URLS:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        if len(glob.glob(output_path + "*.wav")) != len(URLS):
                            ydl.download(i)
                            delay = random.uniform(5, 10)
                            time.sleep(delay)
                        else:
                            break
                        print("Pobrano wszystkie pliki")
                        break
                URLS.remove(i)
            else:
                print("Brak URLS do pobrania")
        else:
            # print(URLS)
            pass

    def extracting_id():
        for info in URLS:
            videoInfo = Video.getInfo(info, mode=ResultMode.json)
            # print(videoInfo)
            value = videoInfo["id"]
            Ids.append(value)
        # print(str(Ids))

    def download_transcription():
        for key in kompendium.keys():
            try:
                # print(key)  # debug
                transcript_list = YouTubeTranscriptApi.list_transcripts(key)
                transcript = transcript_list.find_manually_created_transcript(["pl"])
                if transcript is not None:
                    print(str(transcript))
                else:
                    print("Brak dostępnej transkrypcji")
                    continue
            except Exception as e:
                print(str(e))

    def combining_all():
        global kompendium
        kompendium = dict(zip(Ids, URLS))
        return kompendium

except Exception as e:
    print(str(e))
finally:
    playlist_url = (
        "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt"
    )
    output_path = (
        "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy/Nagrania"  # dysk lokalny
    )
    # output_path = "/mnt/w01/praktyki/30-stopni-w-cieniu/Nagrania"  # serwer ZPS
    output_file = "transcript.txt"
    download_playlist_audio(
        playlist_url, output_path, False
    )  # argument boolean determinuje czy pobieramy czy tylko ekstrahujemy linki
    extracting_id()
    combining_all()
    print(combining_all())
    download_transcription()
