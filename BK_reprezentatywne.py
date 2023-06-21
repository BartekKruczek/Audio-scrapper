import yt_dlp
import os


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
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
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


# Przykładowe użycie funkcji dla playlisty na YouTube
playlist_url = "https://youtube.com/playlist?list=PLIM2IXHjLzGMA1NjX1-_mizbkiNhaydHt"
output_path = "C:/Users/krucz/Documents/Projekty/Anonimowi-Akustycy/Nagrania"
download_playlist_audio(playlist_url, output_path)
