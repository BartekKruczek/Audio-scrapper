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
    URLS = []
    Ids = []
    Titles = []
    Playlists_id = []

    def extracting_info(playlist_urls):
        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url, mode=json)
            playlist_info = Playlist.getInfo(playlist_url, mode=json)
            print(playlist_info)

            for key in playlistVideos:
                value = playlistVideos[key]

                for video in value:
                    URLS.append(video["link"])
                    Ids.append(video["id"])

            playlist_id = playlist_info["id"]
            Playlists_id.append(playlist_id)

        print(Playlists_id)
        global kompendium
        kompendium = {}
        for i in range(len(Ids)):
            video_id = Ids[i]
            url = URLS[i]
            kompendium[video_id] = url

        # print(kompendium)

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
            for playlist_url in playlist_urls:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([playlist_url])
                    delay = random.uniform(5, 10)
                    time.sleep(delay)

            print("Pobrano wszystkie pliki")
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
        "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq",
        "https://youtube.com/playlist?list=PL6-nym1-0TdULhklxX-97X28UXiKiUYop",
    ]
    output_path = "C:/Users/krucz/Documents/Praktyki"  # dysk lokalny

    os.makedirs(os.path.join(output_path, "Nagrania"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "Transkrypcja"), exist_ok=True)

    extracting_info(playlist_urls)
    download_playlist_audio(output_path, False)
    download_transcription(output_path)
