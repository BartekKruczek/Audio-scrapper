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
import glob
from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import subprocess
import json

try:
    try:
        print("Uruchamiam pierwszy skrypt {}".format(str("prox_tester")))
        subprocess.call(["python", "prox_tester.py"])
    except Exception as e:
        print(str(e))
    finally:
        print("Uruchamiam drugi skrypt reprezentatywny")

    kompendium = {}
    URLS = []
    Ids = []
    Titles = []
    Playlists_id = []

    def extracting_info(playlist_urls):
        # wyciąganie linków z playlist
        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url)

        # wyciągnie id playlist
        for playlist_url in playlist_urls:
            playlistInfo = Playlist.getInfo(playlist_url, mode=ResultMode.json)
            playlist_data = json.loads(playlistInfo)
            playlist_id = playlist_data["id"]
            Playlists_id.append(str(playlist_id))
        # print(Playlists_id)

        # wyciąganie info z linków
        for key in playlistVideos:
            value = playlistVideos[key]

        for video in value:
            url = video["link"]
            URLS.append(str(url))

        for info in URLS:
            videoInfo = Video.getInfo(info, mode=ResultMode.json)
            value = videoInfo["id"]
            Ids.append(value)

        # łączenie ze sobą wszystkiego w jeden słownik
        global kompendium
        kompendium = dict(zip(Ids, zip(URLS, Playlists_id)))
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
            "outtmpl": os.path.join(
                output_path,
                "Nagrania",
                "%(playlist)s",
                "%(title)s_%(upload_date)s_%(timestamp)s.%(ext)s",
            ),
            "ignoreerrors": True,
        }

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
            pass

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

except Exception as e:
    print(str(e))
finally:
    playlist_urls = [
        "https://youtube.com/playlist?list=PLJYMhYKidccNMcmNVIqpFLkmOAtKgIfu-",
        "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq",
    ]
    output_path = "C:/Users/krucz/Documents/GitHub/Anonimowi-Akustycy"  # dysk lokalny
    # output_path = "/mnt/w01/praktyki/30-stopni-w-cieniu"  # serwer ZPS

    # Sprawdzenie i utworzenie ścieżki, jeśli nie istnieje
    os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

    extracting_info(playlist_urls)
    download_playlist_audio(output_path, False)
    download_transcription(output_path)
