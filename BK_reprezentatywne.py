import yt_dlp
import os
import random
import webvtt
import time

try:

    def download_playlist_audio(playlist_url, output_path):
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "writesubtitles": True,  # pobieranie transkrypcji
            "writeautomaticsub": False,  # pobieranie automatycznie generowanej transkrypcji
            "subtitleslangs": ["pl"],  # Wybór języka transkrypcji
            "outtmpl": os.path.join(
                output_path, "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s"
            ),
            "ignoreerrors": True,
            "n_threads": 4,
        }

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

                # żywcem mnie nie wezmą!
                delay = random.uniform(5, 10)
                time.sleep(delay)

                # zamiana plików .vtt z transkrypcją na pliki .txx + usuwanie tych pierwszych
                vtt_filename = os.path.join(output_path, f"{video_title}.vtt")
                txt_filename = os.path.join(output_path, f"{video_title}.txt")

                if os.path.exists(vtt_filename):
                    captions = webvtt.read(vtt_filename)
                    captions.save(txt_filename, format="txt")

                # Usunięcie pliku .vtt
                if os.path.exists(vtt_filename):
                    os.remove(vtt_filename)

except Exception as e:
    print(str(e))
finally:
    # Przykładowe użycie funkcji dla playlisty na YouTube
    # playlist_url = "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt"
    playlist_url = "https://www.youtube.com/watch?v=Ofo8ULP-6cI&list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq&index=5&ab_channel=Astrofaza"
    output_path = (
        "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"  # dysk lokalny
    )
    # output_path = "/home/praktyki/workspace/30-stopni-w-cieniu/C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"  # serwer ZPS
    download_playlist_audio(playlist_url, output_path)
