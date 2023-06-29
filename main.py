from YTScrapper import *

playlist_urls = [
    "https://youtube.com/playlist?list=PLUWDBVpNIE52-QW1DuVyQu-QWLCtIGgJX",
    "https://youtube.com/playlist?list=PLUWDBVpNIE51lQ96yID-oF-IKppUNrpay",
    "https://youtube.com/playlist?list=PLUWDBVpNIE51d-kaYJyIOIE9fm7RNqI8C",
    "https://youtube.com/playlist?list=PLTld5jYla5hbtbhnUNXCrD7p-w-wWI2xP",
    "https://youtube.com/playlist?list=PL6-nym1-0TdWnICiAzd6CUXCg2crQ18Yq",
    "https://youtube.com/playlist?list=PL6-nym1-0TdULhklxX-97X28UXiKiUYop",
    "https://youtube.com/playlist?list=PL6-nym1-0TdUD0t7tbGEjs6lQcvuicoQH",
]
output_path = "your_path"
proxy_path = "your_proxy_path.txt"

scrapper = YTScrapper()
scrapper.extracting_info(output_path, playlist_urls, proxy_path)
scrapper.download_playlist_audio(output_path, False)
scrapper.download_transcription(output_path, False)
