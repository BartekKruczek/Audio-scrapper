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
        self.all_in_one = {}
        self.proxies = []

    def __repr__(self) -> str:
        return "Class created to help scrapping YT playlists and more."

    def extracting_info(self, output_path, playlist_urls, proxy_file_path):
        os.makedirs(os.path.join(output_path, "Audio"), exist_ok=True)
        os.makedirs(os.path.join(output_path, "Transcription"), exist_ok=True)

        with open(proxy_file_path, "r") as file:
            for line in file:
                line = line.strip()
                self.proxies.append(line)

        # extracting info.
        for playlist_url in playlist_urls:
            playlistVideos = Playlist.getVideos(playlist_url, mode=json)
            playlist_info = Playlist.getInfo(playlist_url, mode=json)

            playlist_id = playlist_info["id"]

            for key in playlistVideos:
                value = playlistVideos[key]

                for video in value:
                    video_id = video["id"]
                    url = video["link"]
                    self.all_in_one[video_id] = (url, playlist_id)

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
                "Audio",
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
            for video_id, (url, playlist_id) in self.all_in_one():
                # checking if audio is already downloaded
                audio_path = os.path.join(
                    output_path, "Audio", playlist_id, f"{video_id}.wav"
                )
                if os.path.exists(audio_path):
                    print(f"Video ID {video_id} exists, skipping.")
                    continue

                # if non proxy is valid
                if len(self.proxies) == 0:
                    print("Downloading audio ID:", video_id)
                    start_time = time.time()
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
                            ydl.download([url])
                            elapsed_time = time.time() - start_time
                            print(
                                "Estimated time {}: {:.2f} seconds".format(
                                    video_id, elapsed_time
                                )
                            )
                            delay = random.uniform(5, 10)
                            print(
                                "Delay before next download: {:.2f} seconds".format(
                                    delay
                                )
                            )

                            time.sleep(delay)
                            break
                        except Exception as e:
                            print(f"An error occurred {proxy}: {str(e)}")
                            continue
                else:
                    for proxy in self.proxies:
                        ydl_opts["proxy"] = proxy
                        print("Downloading audio ID:", video_id)
                        print(
                            "Downloading using proxy: {}".format(str(ydl_opts["proxy"]))
                        )
                        start_time = time.time()

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            try:
                                ydl.download([url])
                                elapsed_time = time.time() - start_time
                                print(
                                    "Estimated time {}: {:.2f} seconds".format(
                                        video_id, elapsed_time
                                    )
                                )
                                delay = random.uniform(5, 10)
                                print(
                                    "Delay before next download: {:.2f} seconds".format(
                                        delay
                                    )
                                )

                                time.sleep(delay)
                                break
                            except Exception as e:
                                print(f"An error occurred {proxy}: {str(e)}")
                                continue

            print("All files have been downloaded")
        else:
            pass

    def download_transcription(self, output_path, download):
        if download:
            transcripts_folder = os.path.join(output_path, "Transcription")
            os.makedirs(transcripts_folder, exist_ok=True)

            if len(self.proxies) == 0:
                for video_id, (url, playlist_id) in self.all_in_one():
                    playlist_folder = os.path.join(transcripts_folder, playlist_id)
                    os.makedirs(playlist_folder, exist_ok=True)

                    transcript_path = os.path.join(
                        playlist_folder, f"{video_id}_transcript.txt"
                    )
                    if os.path.exists(transcript_path):
                        print(
                            f"Transcription for video ID {video_id} exists, skipping."
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
                                f"Transcription for video ID {video_id} has been downloaded."
                            )
                    except TranscriptsDisabled:
                        print("No transcript available.")
            else:
                for proxy in self.proxies:
                    for video_id, (url, playlist_id) in self.all_in_one():
                        playlist_folder = os.path.join(transcripts_folder, playlist_id)
                        os.makedirs(playlist_folder, exist_ok=True)

                        transcript_path = os.path.join(
                            playlist_folder, f"{video_id}_transcript.txt"
                        )
                        if os.path.exists(transcript_path):
                            print(
                                f"Transcription for video ID {video_id} exists, skipping."
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
                                    f"Transcription for video ID {video_id} has been downloaded."
                                )
                        except TranscriptsDisabled:
                            print("No transcript available.")
        else:
            pass
