import yt_dlp
import os
import random
import webvtt
import time
import glob
from youtubesearchpython import *

try:

    def download_playlist_audio(playlist_url, output_path):
        URLS = []
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "writesubtitles": False,  # pobieranie transkrypcji
            "writeautomaticsub": False,  # pobieranie automatycznie generowanej transkrypcji
            "subtitleslangs": ["en"],  # Wybór języka transkrypcji
            "outtmpl": os.path.join(
                output_path, "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s"
            ),
            "ignoreerrors": True,
            "n_threads": 4,
        }

        # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #     playlist_info = ydl.extract_info(playlist_url, download=False)
        #     playlist_title = playlist_info["title"]
        #     print(f"Pobieranie audio z playlisty: {playlist_title}")

        #     for video in playlist_info["entries"]:
        #         video_title = video["title"]
        #         video_url = video["url"]

        #         print(f"Pobieranie audio z filmu: {video_title}")

        #         # Pobieranie pliku audio
        #         ydl.download([video_url])

        #         # żywcem mnie nie wezmą!
        #         delay = random.uniform(5, 10)
        #         time.sleep(delay)

        #         # zamiana plików .vtt z transkrypcją na pliki .txx + usuwanie tych pierwszych
        #         vtt_filename = os.path.join(output_path, f"{video_title}.vtt")
        #         txt_filename = os.path.join(output_path, f"{video_title}.txt")

        #         if os.path.exists(vtt_filename):
        #             captions = webvtt.read(vtt_filename)
        #             captions.save(txt_filename, format="txt")

        #         # Usunięcie pliku .vtt
        #         if os.path.exists(vtt_filename):
        #             os.remove(vtt_filename)

        playlistVideos = Playlist.getVideos(playlist_url)

        # wyodrębnianie url
        for key in playlistVideos:
            value = playlistVideos[key]
            # print(value)

        for video in value:
            url = video["link"]
            URLS.append(str(url))

        # pobieranie

        if len(URLS) > 0:
            downloaded_files = []
            while len(URLS) > 0:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    if len(glob.glob(output_path + "*.wav")) != len(downloaded_files):
                        i = URLS[0]  # Pobierz pierwszy URL z listy
                        ydl.download(i)
                        downloaded_files.append(i)
                        URLS.remove(i)  # Usuń pobrany URL z listy URLS
                    else:
                        break
            print("Pobrano wszystkie pliki")
        else:
            print("Brak URLS do pobrania")

except Exception as e:
    print(str(e))
finally:
    playlist_url = (
        "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq"
    )
    output_path = (
        "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy/Nagrania"  # dysk lokalny
    )
    # output_path = "/home/praktyki/workspace/30-stopni-w-cieniu/C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"  # serwer ZPS
    download_playlist_audio(playlist_url, output_path)
