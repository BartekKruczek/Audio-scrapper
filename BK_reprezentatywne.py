import yt_dlp
import os
import random
import time
import time
from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import subprocess
import json

try:
    # try:
    #     print("Uruchamiam pierwszy skrypt: {}".format(str("prox_tester")))
    #     subprocess.call(["python", "prox_tester.py"])
    # except Exception as e:
    #     print(str(e))
    # finally:
    #     print("Uruchamiam drugi skrypt: reprezentatywny")

    kompendium = {}

    def extracting_info(playlist_urls):
        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url, mode=json)
            playlist_info = Playlist.getInfo(playlist_url, mode=json)

            playlist_id = playlist_info["id"]

            kompendium[playlist_id] = {}  # utwórz słownik dla danego playlist_id

            for key in playlistVideos:
                value = playlistVideos[key]

                for video in value:
                    video_id = video["id"]
                    url = video["link"]
                    kompendium[playlist_id][
                        video_id
                    ] = url  # dodaj url do słownika dla danego video_id

        print(kompendium)

    def download_playlist_audio(output_path, download):
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "ignoreerrors": True,
        }

        if download:
            for playlist_id, videos in kompendium.items():
                playlist_folder = os.path.join(output_path, "Nagrania", playlist_id)
                os.makedirs(playlist_folder, exist_ok=True)

                for video_id, url in videos.items():
                    audio_path = os.path.join(playlist_folder, f"{video_id}.wav")
                    if os.path.exists(audio_path):
                        print(
                            f"Plik audio dla video ID {video_id} już istnieje. Pomijam pobieranie."
                        )
                        continue

                    print("Pobieram plik o ID:", video_id)
                    start_time = time.time()
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.params["outtmpl"] = os.path.join(
                            playlist_folder, f"{video_id}.%(ext)s"
                        )

                        ydl.download([url])
                    elapsed_time = time.time() - start_time
                    print(
                        "Czas oczekiwania dla pliku o ID {}: {:.2f} sekundy".format(
                            video_id, elapsed_time
                        )
                    )
                    delay = random.uniform(5, 10)
                    print(
                        "Opóźnienie przed pobraniem kolejnego pliku: {:.2f} sekundy".format(
                            delay
                        )
                    )
                    time.sleep(delay)

            print("Pobrano wszystkie pliki")
        else:
            pass

    def download_transcription(output_path):
        transcripts_folder = os.path.join(output_path, "Transkrypcja")
        os.makedirs(transcripts_folder, exist_ok=True)

        for video_id, (url, playlist_id) in kompendium.items():
            playlist_folder = os.path.join(transcripts_folder, playlist_id)
            os.makedirs(playlist_folder, exist_ok=True)

            transcript_path = os.path.join(
                playlist_folder, f"{video_id}_transcript.txt"
            )
            if os.path.exists(transcript_path):
                print(
                    f"Transkrypcja dla video ID {video_id} już istnieje. Pomijam pobieranie."
                )
                continue

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

                    with open(transcript_path, "w", encoding="utf-8") as text_file:
                        text_file.write(text_formatted)

                    print(f"Transkrypcja dla video ID {video_id} została zapisana.")
            except TranscriptsDisabled:
                pass

except Exception as e:
    print(str(e))
finally:
    playlist_urls = [
        "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq",
        "https://youtube.com/playlist?list=PL6-nym1-0TdULhklxX-97X28UXiKiUYop",
    ]
    output_path = "C:/Users/krucz/Documents/Praktyki"  # dysk lokalny
    # output_path = "/mnt/s01/praktyki/storage"  # dysk ZPS

    os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

    extracting_info(playlist_urls)
    download_playlist_audio(output_path, True)
    download_transcription(output_path)
