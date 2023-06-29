"""
README!

How it works? In the variable 'kompendium' are the most important information tha you will need. It's organized as followed:

kompendium = {video_id: (link_to_video, playlist_id)}

In shorts, kompendium is dictionary with tuple inside as value representation. Link_to_video is direct link to video, playlist_id represent its' playlist id
"""


import yt_dlp
import os
import random
import time
import time
from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from youtubesearchpython import PlaylistsSearch
import json

try:

    def extracting_info(playlist_urls):
        global kompendium
        kompendium = {}

        global proxies
        proxies = []

        proxy_file_path = "valid_prox.txt"  # Ścieżka do pliku tekstowego z proxy
        with open(proxy_file_path, "r") as file:
            for line in file:
                line = (
                    line.strip()
                )  # Usuwanie białych znaków z początku i końca linijki
                proxies.append(line)

        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url, mode=json)
            playlist_info = Playlist.getInfo(playlist_url, mode=json)

            playlist_id = playlist_info["id"]

            for key in playlistVideos:
                value = playlistVideos[key]

                for video in value:
                    video_id = video["id"]
                    url = video["link"]
                    kompendium[video_id] = (url, playlist_id)
        print(len(kompendium))

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
            for video_id, (url, playlist_id) in kompendium.items():
                audio_path = os.path.join(
                    output_path, "Nagrania", playlist_id, f"{video_id}.wav"
                )
                if os.path.exists(audio_path):
                    print(
                        f"Plik audio dla video ID {video_id} już istnieje. Pomijam pobieranie."
                    )
                    continue

                if len(proxies) == 0:
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
                    for proxy in proxies:
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

    def download_transcription(output_path, download):
        if download:
            transcripts_folder = os.path.join(output_path, "Transkrypcja")
            os.makedirs(transcripts_folder, exist_ok=True)

            if len(proxies) == 0:
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
                for proxy in proxies:
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

    def search_youtube_playlists(*queries, limit=10):
        for query in queries:
            playlists_search = PlaylistsSearch(
                query, limit=limit, language="pl"
            )  # Ograniczamy do 10 wyników
            result = playlists_search.result()

            for playlist in result["result"]:
                title = playlist["title"]
                link = playlist["link"]
                print(f"Title: {title}")
                print(f"Link: {link}")
                print()

                playlist_id = playlist["id"]
                playlist_url = playlist["link"]

                # Sprawdzanie filmów w playlistach
                playlist_items = Playlist.getVideos(playlist_url, mode=json)

                for key in playlist_items:
                    value = playlist_items[key]

                    for video in value:
                        video_id = video["id"]
                        url = video["link"]

                        # Sprawdzanie dostępności transkrypcji dla polskiego języka
                        try:
                            transcript_list = YouTubeTranscriptApi.list_transcripts(
                                video_id
                            )
                            transcript = (
                                transcript_list.find_manually_created_transcript(["pl"])
                            )

                            if transcript is not None:
                                # Dodawanie informacji do kompendium
                                kompendium[video_id] = (url, playlist_id)
                        except Exception:
                            pass

except Exception as e:
    print(str(e))
finally:
    playlist_urls = [
        "https://youtube.com/playlist?list=PLUWDBVpNIE52-QW1DuVyQu-QWLCtIGgJX",
        "https://youtube.com/playlist?list=PLUWDBVpNIE51lQ96yID-oF-IKppUNrpay",
        "https://youtube.com/playlist?list=PLUWDBVpNIE51d-kaYJyIOIE9fm7RNqI8C",
        "https://youtube.com/playlist?list=PLTld5jYla5hbtbhnUNXCrD7p-w-wWI2xP",
        "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq",
        "https://youtube.com/playlist?list=PL6-nym1-0TdULhklxX-97X28UXiKiUYop",
        "https://youtube.com/playlist?list=PL6-nym1-0TdUD0t7tbGEjs6lQcvuicoQH",
    ]
    output_path = "C:/Users/krucz/Documents/Praktyki"  # dysk lokalny
    # output_path = "/mnt/s01/praktyki/StorageYT"  # dysk ZPS

    os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

    extracting_info(playlist_urls)
    search_youtube_playlists(
        "podcasty", "historie", "nauka", "wywiady", "rozmowy", limit=50
    )
    download_playlist_audio(output_path, False)
    download_transcription(output_path, True)
