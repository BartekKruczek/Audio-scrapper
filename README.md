# Audio-scrapper

Audio-scrapper is a tool that enables downloading a large amount of audio data from the internet while maintaining anonymity. Currently, it is based on two platforms: **Google Podcasts** and **YouTube**. The obtained files are used for further translation purposes and as training data for a neural model.

## Setup

The entire source code has been written in Python. All the necessary libraries can be installed from the *requirements.txt* file.

```text
pip install -r requirements.txt
```

## Description

### YouTube scrapper

The file [YTScrapper.py](YTScrapper.py) provides the ability to download audio from manually added playlists or automatically searched ones. The implementation of the code primarily relies on the libraries [youtube-search-python](https://pypi.org/project/youtube-search-python/) and [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/).

### Google Podcasts scrapper

## Python usage

All scripts can be executed from the [main.py](main.py) level by creating appropriate class instances and then calling individual functions with desired arguments.

### Example of calling [YTScrapper](YTScrapper.py) from [main.py](main.py) level

```python
from YTScrapper import *

playlist_urls = ['example_playlist_url']
output_path = "your_output_path"
proxy_path = "your_proxy_path.txt"

scrapper = YTScrapper()
scrapper.extracting_info(output_path, playlist_urls, proxy_path)
scrapper.download_playlist_audio(output_path, True)
scrapper.download_transcription(output_path, True)
```

The arguments in the ```playlist``` variable must be passed in the *string* format. The boolean argument in the ```scrapper.download_playlist_audio``` function of the scrapper determines whether the audio should be downloaded or only the information about it should be saved. The same applies to the ```scrapper.download_transcription```. By declaring the `output_path` variable, a folder is chosen where the corresponding subfolders, namely `Audio` and `Transcription`, will be created. Within each of these subfolders, further subfolders will be automatically created to represent each downloaded playlist.

### Downloading items using [yt-dlp](https://github.com/yt-dlp/yt-dlp) library

Below is an example code that demonstrates the usage of yt-dlp library for downloading videos from YouTube.

```python
    ydl_opts = {
                "format": "audio_format",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "wav",
                        "preferredquality": "192",
                    }
                ],
                "outtmpl": "uotput_path",
                "ignoreerrors": bool,
                "n_threads": int,
                "encoding": str,
                "proxy": None,
                "sleep_interval_requests": 3,
                "sleep_interval_subtitles": 2,
                "ratelimit": 5000000000,
                "throttledratelimit": 10,
                "sleep_interval": 1,
                "max_sleep_interval": 10,
    }
```

This is just a demonstration example, and every user of this tool should modify it according to their needs. Some variables have intentionally been changed. You can find more options [here](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py).

### Example of calling [Process](Process.py) from [main.py](main.py) level

```python
from Process import *

output_path = "scraper_output_path" 

processor = Process()
processor.transcribe_folder(output_path,whisper_model_size='base', preferred_device='cpu',language_detection=False)
processor.split_to_words_folder(output_path,whisper_model_size='base', preferred_device='cpu')
```

```Process``` class contains functions for transcribing and splitting (according to words timestamps) acquired audio files. For performing such actions, Whisper model is used.

Every function contains at least 3 arguments. All of them are described in [Process](Process.py), in form of comments.

## More information

The earliest version of the repository, dated June 30, 2023, was created by [JKChojnacki](https://github.com/JKChojnacki), [JacobeCode](https://github.com/JacobeCode) and [BartekKruczek](https://github.com/BartekKruczek) under the guidance of [stachu86](https://github.com/stachu86). Feel free to use this software. We wish you a great time :raised_hands:

## License

The repository operates under the [MIT](LICENSE) license.
