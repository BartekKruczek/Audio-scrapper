import yt_dlp
import os
import random
import time
import glob
from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

try:
    kompendium = {}
    URLS = []
    Ids = []

    def download_playlist_audio(playlist_urls, output_path, download):
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
                output_path,
                "Nagrania",
                "%(playlist)s",
                "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s",
            ),
            "ignoreerrors": True,
            "n_threads": 4,
        }

        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url)

            for key in playlistVideos:
                value = playlistVideos[key]

            for video in value:
                url = video["link"]
                URLS.append(str(url))

        if download == True:
            if len(URLS) > 0:
                for i in URLS:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        if len(
                            glob.glob(
                                os.path.join(output_path, "Nagrania", "*", "*.wav")
                            )
                        ) != len(URLS):
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

    def download_transcription(output_path):
        transcripts_folder = os.path.join(output_path, "Transkrypcja")
        os.makedirs(transcripts_folder, exist_ok=True)

        for video_id in kompendium.keys():
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_manually_created_transcript(["pl"])

                if transcript is not None:
                    lines = []
                    for line in transcript.fetch():
                        text = line["text"]
                        start = line["start"]
                        duration = line["duration"]

                        line_with_timestamp = f"[{duration}] [{start}] {text}"
                        lines.append(line_with_timestamp)

                    text_formatted = "\n".join(lines)

                    with open(
                        os.path.join(transcripts_folder, f"{video_id}_transcript.txt"),
                        "w",
                        encoding="utf-8",
                    ) as text_file:
                        text_file.write(text_formatted)

                    print(f"Transkrypcja dla video ID {video_id} została zapisana.")
            except TranscriptsDisabled:
                pass

    def combining_all():
        global kompendium
        kompendium = dict(zip(Ids, URLS))
        return kompendium

except Exception as e:
    print(str(e))
finally:
    playlist_urls = [
        "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt",
        "https://youtube.com/playlist?list=PLUWDBVpNIE52-QW1DuVyQu-QWLCtIGgJX",
    ]
    output_path = "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy"  # dysk lokalny
    # output_path = "/mnt/w01/praktyki/30-stopni-w-cieniu"  # serwer ZPS

    # Sprawdzenie i utworzenie ścieżki, jeśli nie istnieje
    os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

    download_playlist_audio(
        playlist_urls, output_path, False
    )  # argument boolean determinuje czy pobieramy czy tylko ekstrahujemy linki
    extracting_id()
    combining_all()
    print(combining_all())
    download_transcription(output_path)

# wersja 2
# import yt_dlp
# import os
# import random
# import time
# import glob
# from youtubesearchpython import *
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api._errors import TranscriptsDisabled

# try:
#     kompendium = {}
#     URLS = []
#     Ids = []

#     def download_playlist_audio(playlist_urls, output_path, download):
#         ydl_opts = {
#             "format": "m4a/bestaudio/best",
#             "postprocessors": [
#                 {
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "wav",
#                     "preferredquality": "192",
#                 }
#             ],
#             "outtmpl": os.path.join(
#                 output_path,
#                 "Nagrania",
#                 "%(playlist)s",
#                 "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s",
#             ),
#             "ignoreerrors": True,
#             "n_threads": 4,
#         }

#         for playlist_url in playlist_urls:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info_dict = ydl.extract_info(playlist_url, download=False)
#                 playlist_name = info_dict.get("title", "")
#                 playlist_name = sanitize_title(
#                     playlist_name
#                 )  # Usuwanie niedozwolonych znaków

#                 playlistVideos = Playlist.getVideos(playlist_url)
#                 for key in playlistVideos:
#                     value = playlistVideos[key]

#                 for video in value:
#                     url = video["link"]
#                     URLS.append((url, playlist_name))

#         if download == True:
#             if len(URLS) > 0:
#                 for url, playlist_name in URLS:
#                     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                         if len(
#                             glob.glob(
#                                 os.path.join(
#                                     output_path, "Nagrania", playlist_name, "*.wav"
#                                 )
#                             )
#                         ) != len(URLS):
#                             ydl.download([url])
#                             delay = random.uniform(5, 10)
#                             time.sleep(delay)
#                         else:
#                             break
#                 print("Pobrano wszystkie pliki")
#                 URLS = [
#                     url for url in URLS if url[0] != url
#                 ]  # Usunięcie już pobranych URLi
#             else:
#                 print("Brak URLS do pobrania")
#         else:
#             # print(URLS)
#             pass

#     def extracting_id():
#         for info in URLS:
#             url, _ = info
#             videoInfo = Video.getInfo(url, mode=ResultMode.json)
#             # print(videoInfo)
#             value = videoInfo["id"]
#             Ids.append(value)
#         # print(str(Ids))

#     def download_transcription(output_path):
#         transcripts_folder = os.path.join(output_path, "Transkrypcja")
#         os.makedirs(transcripts_folder, exist_ok=True)

#         for video_id, playlist_name in kompendium.items():
#             try:
#                 transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#                 transcript = transcript_list.find_manually_created_transcript(["pl"])

#                 if transcript is not None:
#                     lines = []
#                     for line in transcript.fetch():
#                         text = line["text"]
#                         start = line["start"]
#                         duration = line["duration"]

#                         line_with_timestamp = f"[{duration}] [{start}] {text}"
#                         lines.append(line_with_timestamp)

#                     text_formatted = "\n".join(lines)

#                     with open(
#                         os.path.join(
#                             transcripts_folder,
#                             playlist_name,
#                             f"{video_id}_transcript.txt",
#                         ),
#                         "w",
#                         encoding="utf-8",
#                     ) as text_file:
#                         text_file.write(text_formatted)

#                     print(f"Transkrypcja dla video ID {video_id} została zapisana.")
#             except TranscriptsDisabled:
#                 pass

#     def combining_all():
#         global kompendium
#         kompendium = dict(zip(Ids, [url for url, _ in URLS]))
#         return kompendium

#     def sanitize_title(title):
#         # Usuwanie niedozwolonych znaków w nazwie folderu
#         forbidden_chars = r'<>:"/\|?*'
#         sanitized_title = "".join([c for c in title if c not in forbidden_chars])
#         return sanitized_title.strip()

# except Exception as e:
#     print(str(e))
# finally:
#     playlist_urls = [
#         "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt",
#         "https://youtube.com/playlist?list=PL1234567890",
#     ]
#     output_path = "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy"  # dysk lokalny
#     # output_path = "/mnt/w01/praktyki/30-stopni-w-cieniu"  # serwer ZPS

#     # Sprawdzenie i utworzenie ścieżki, jeśli nie istnieje
#     os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
#     os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

#     download_playlist_audio(
#         playlist_urls, output_path, False
#     )  # argument boolean determinuje czy pobieramy czy tylko ekstrahujemy linki
#     extracting_id()
#     combining_all()
#     print(combining_all())
#     download_transcription(output_path)

# wersja 3
# import yt_dlp
# import os
# import random
# import time
# import glob
# from youtubesearchpython import *
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api._errors import TranscriptsDisabled

# try:
#     kompendium = {}
#     URLS = []
#     Ids = []

#     def download_playlist_audio(playlist_urls, output_path, download):
#         ydl_opts = {
#             "format": "m4a/bestaudio/best",
#             "postprocessors": [
#                 {
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "wav",
#                     "preferredquality": "192",
#                 }
#             ],
#             "outtmpl": os.path.join(
#                 output_path,
#                 "Nagrania",
#                 "%(playlist)s",
#                 "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s",
#             ),
#             "ignoreerrors": True,
#             "n_threads": 4,
#         }

#         for playlist_url in playlist_urls:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info_dict = ydl.extract_info(playlist_url, download=False)
#                 playlist_name = info_dict.get("title", "")
#                 playlist_name = sanitize_title(
#                     playlist_name
#                 )  # Usuwanie niedozwolonych znaków

#                 playlistVideos = Playlist.getVideos(playlist_url)
#                 for key in playlistVideos:
#                     value = playlistVideos[key]

#                 for video in value:
#                     url = video["link"]
#                     URLS.append((url, playlist_name))

#         if download:
#             if len(URLS) > 0:
#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     for url, playlist_name in URLS:
#                         if len(
#                             glob.glob(
#                                 os.path.join(
#                                     output_path, "Nagrania", playlist_name, "*.wav"
#                                 )
#                             )
#                         ) != len(URLS):
#                             ydl.download([url])
#                             delay = random.uniform(5, 10)
#                             time.sleep(delay)
#                         else:
#                             break
#                 print("Pobrano wszystkie pliki")
#                 URLS.clear()  # Usunięcie już pobranych URLi
#             else:
#                 print("Brak URLS do pobrania")
#         else:
#             # print(URLS)
#             pass

#     def extracting_id():
#         for info in URLS:
#             url, _ = info
#             videoInfo = Video.getInfo(url, mode=ResultMode.json)
#             # print(videoInfo)
#             value = videoInfo["id"]
#             Ids.append(value)
#         # print(str(Ids))

#     def download_transcription(output_path):
#         transcripts_folder = os.path.join(output_path, "Transkrypcja")
#         os.makedirs(transcripts_folder, exist_ok=True)

#         for video_id, playlist_name in kompendium.items():
#             try:
#                 transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#                 transcript = transcript_list.find_manually_created_transcript(["pl"])

#                 if transcript is not None:
#                     lines = []
#                     for line in transcript.fetch():
#                         text = line["text"]
#                         start = line["start"]
#                         duration = line["duration"]

#                         line_with_timestamp = f"[{duration}] [{start}] {text}"
#                         lines.append(line_with_timestamp)

#                     text_formatted = "\n".join(lines)

#                     with open(
#                         os.path.join(
#                             transcripts_folder,
#                             playlist_name,
#                             f"{video_id}_transcript.txt",
#                         ),
#                         "w",
#                         encoding="utf-8",
#                     ) as text_file:
#                         text_file.write(text_formatted)

#                     print(f"Transkrypcja dla video ID {video_id} została zapisana.")
#             except TranscriptsDisabled:
#                 pass

#     def combining_all():
#         global kompendium
#         kompendium = dict(zip(Ids, [url for url, _ in URLS]))
#         return kompendium

#     def sanitize_title(title):
#         # Usuwanie niedozwolonych znaków w nazwie folderu
#         forbidden_chars = r'<>:"/\|?*'
#         sanitized_title = "".join([c for c in title if c not in forbidden_chars])
#         return sanitized_title.strip()

# except Exception as e:
#     print(str(e))
# finally:
#     playlist_urls = [
#         "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt",
#         "https://youtube.com/playlist?list=PL1234567890",
#     ]
#     output_path = "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy"  # dysk lokalny
#     # output_path = "/mnt/w01/praktyki/30-stopni-w-cieniu"  # serwer ZPS

#     # Sprawdzenie i utworzenie ścieżki, jeśli nie istnieje
#     os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
#     os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

#     download_playlist_audio(
#         playlist_urls, output_path, False
#     )  # argument boolean determinuje czy pobieramy czy tylko ekstrahujemy linki
#     extracting_id()
#     combining_all()
#     print(combining_all())
#     download_transcription(output_path)

# 4.0
# import yt_dlp
# import os
# import random
# import time
# import glob
# from youtubesearchpython import *
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api._errors import TranscriptsDisabled

# try:
#     kompendium = {}
#     URLS = []
#     Ids = []

#     def download_playlist_audio(playlist_urls, output_path, download):
#         ydl_opts = {
#             "format": "m4a/bestaudio/best",
#             "postprocessors": [
#                 {
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "wav",
#                     "preferredquality": "192",
#                 }
#             ],
#             "outtmpl": os.path.join(
#                 output_path,
#                 "Nagrania",
#                 "%(playlist)s",
#                 "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s",
#             ),
#             "ignoreerrors": True,
#             "n_threads": 4,
#         }

#         for playlist_url in playlist_urls:
#             playlistVideos = Playlist.getVideos(playlist_url)

#             for key in playlistVideos:
#                 value = playlistVideos[key]

#             for video in value:
#                 url = video["link"]
#                 URLS.append(str(url))

#         if download == True:
#             if len(URLS) > 0:
#                 for i in URLS:
#                     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                         if len(
#                             glob.glob(
#                                 os.path.join(output_path, "Nagrania", "*", "*.wav")
#                             )
#                         ) != len(URLS):
#                             ydl.download(i)
#                             delay = random.uniform(5, 10)
#                             time.sleep(delay)
#                         else:
#                             break
#                         print("Pobrano wszystkie pliki")
#                         break
#                 URLS.remove(i)
#             else:
#                 print("Brak URLS do pobrania")
#         else:
#             # print(URLS)
#             pass

#     def extracting_id():
#         for info in URLS:
#             videoInfo = Video.getInfo(info, mode=ResultMode.json)
#             # print(videoInfo)
#             value = videoInfo["id"]
#             Ids.append(value)
#         # print(str(Ids))

#     def download_transcription(output_path):
#         transcripts_folder = os.path.join(output_path, "Transkrypcja")
#         os.makedirs(transcripts_folder, exist_ok=True)

#         for video_id, playlist_url in kompendium.items():
#             try:
#                 if "playlist?list=" not in playlist_url:
#                     continue

#                 playlist_id = playlist_url.split("playlist?list=")[1]
#                 playlist_folder = os.path.join(transcripts_folder, playlist_id)
#                 os.makedirs(playlist_folder, exist_ok=True)

#                 transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#                 transcript = transcript_list.find_manually_created_transcript(["pl"])

#                 if transcript is not None:
#                     lines = []
#                     for line in transcript.fetch():
#                         text = line["text"]
#                         start = line["start"]
#                         duration = line["duration"]

#                         line_with_timestamp = f"[{duration}] [{start}] {text}"
#                         lines.append(line_with_timestamp)

#                     text_formatted = "\n".join(lines)

#                     with open(
#                         os.path.join(playlist_folder, f"{video_id}_transcript.txt"),
#                         "w",
#                         encoding="utf-8",
#                     ) as text_file:
#                         text_file.write(text_formatted)

#                     print(f"Transkrypcja dla video ID {video_id} została zapisana.")
#             except TranscriptsDisabled:
#                 pass

#     def combining_all():
#         global kompendium
#         kompendium = dict(zip(Ids, URLS))
#         return kompendium

# except Exception as e:
#     print(str(e))
# finally:
#     playlist_urls = [
#         "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt",
#         "https://youtube.com/playlist?list=PLUWDBVpNIE52-QW1DuVyQu-QWLCtIGgJX",
#     ]
#     output_path = "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy"  # dysk lokalny
#     # output_path = "/mnt/w01/praktyki/30-stopni-w-cieniu"  # serwer ZPS

#     # Sprawdzenie i utworzenie ścieżki, jeśli nie istnieje
#     os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
#     os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

#     download_playlist_audio(
#         playlist_urls, output_path, False
#     )  # argument boolean determinuje czy pobieramy czy tylko ekstrahujemy linki
#     extracting_id()
#     combining_all()
#     print(combining_all())
#     download_transcription(output_path)
