import yt_dlp
import os
import random
import time
import time
from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import json


class YTScrapper:
    def __init__(self) -> None:
        self.kompendium = {}
        self.proxies = []

    def __repr__(self) -> str:
        return "Class created to help scrapping YT playlists."

    def extracting_info(self, output_path, playlist_urls, proxy_file_path):
        os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
        os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

        with open(proxy_file_path, "r") as file:
            for line in file:
                line = (
                    line.strip()
                )  # Usuwanie białych znaków z początku i końca linijki
                self.proxies.append(line)

        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url, mode=json)
            playlist_info = Playlist.getInfo(playlist_url, mode=json)

            playlist_id = playlist_info["id"]

            for key in playlistVideos:
                value = playlistVideos[key]

                for video in value:
                    video_id = video["id"]
                    url = video["link"]
                    self.kompendium[video_id] = (url, playlist_id)

    def download_playlist_audio(self, output_path, download):
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
                "%(playlist_id)s",
                "%(id)s.%(ext)s",
            ),
            "ignoreerrors": True,
            "n_threads": 4,
            "encoding": "utf-8",
            "proxy": None,
            "sleep_interval_requests": 3,
            "sleep_interval_subtitles": 2,
            "ratelimit": 5000000000,
            "throttledratelimit": 10,
            "sleep_interval": 1,
            "max_sleep_interval": 10,
        }

        if download:
            for video_id, (url, playlist_id) in self.kompendium.items():
                audio_path = os.path.join(
                    output_path, "Nagrania", playlist_id, f"{video_id}.wav"
                )
                if os.path.exists(audio_path):
                    print(
                        f"Plik audio dla video ID {video_id} już istnieje. Pomijam pobieranie."
                    )
                    continue

                if len(self.proxies) == 0:
                    print("Pobieram plik o ID:", video_id)
                    start_time = time.time()
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
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
                            break
                        except Exception as e:
                            print(
                                f"Wystąpił błąd podczas pobierania z proxy {proxy}: {str(e)}"
                            )
                            continue
                else:
                    for proxy in self.proxies:
                        ydl_opts["proxy"] = proxy
                        print("Pobieram plik o ID:", video_id)
                        print(
                            "Pobieranie z wykorzystaniem proxy: {}".format(
                                str(ydl_opts["proxy"])
                            )
                        )
                        start_time = time.time()

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            try:
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
                                break
                            except Exception as e:
                                print(
                                    f"Wystąpił błąd podczas pobierania z proxy {proxy}: {str(e)}"
                                )
                                continue

            print("Pobrano wszystkie pliki")
        else:
            print("Understandable, have a great day!")

    def download_transcription(self, output_path, download):
        if download:
            transcripts_folder = os.path.join(output_path, "Transkrypcja")
            os.makedirs(transcripts_folder, exist_ok=True)

            if len(self.proxies) == 0:
                for video_id, (url, playlist_id) in self.kompendium.items():
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
                        transcript_list = YouTubeTranscriptApi.list_transcripts(
                            video_id
                        )
                        transcript = transcript_list.find_manually_created_transcript(
                            ["pl"]
                        )

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
                                transcript_path, "w", encoding="utf-8"
                            ) as text_file:
                                text_file.write(text_formatted)

                            print(
                                f"Transkrypcja dla video ID {video_id} została zapisana."
                            )
                    except TranscriptsDisabled:
                        print("Brak dostępnej transkrypcji dla pliku.")
            else:
                for proxy in self.proxies:
                    for video_id, (url, playlist_id) in self.kompendium.items():
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
                            transcript_list = YouTubeTranscriptApi.list_transcripts(
                                video_id, proxies={"http": proxy, "https": proxy}
                            )
                            transcript = (
                                transcript_list.find_manually_created_transcript(["pl"])
                            )

                            if transcript is not None:
                                lines = []
                                for line in transcript.fetch():
                                    text = line["text"]
                                    start = line["start"]
                                    duration = line["duration"]

                                    line_with_timestamp = (
                                        f"[{duration}] [{start}] {text}"
                                    )
                                    lines.append(line_with_timestamp)

                                text_formatted = "\n".join(lines)

                                with open(
                                    transcript_path, "w", encoding="utf-8"
                                ) as text_file:
                                    text_file.write(text_formatted)

                                print(
                                    f"Transkrypcja dla video ID {video_id} została zapisana."
                                )
                        except TranscriptsDisabled:
                            print("Brak dostępnej transkrypcji dla pliku.")
        else:
            print("Understandable, have a great day!")
