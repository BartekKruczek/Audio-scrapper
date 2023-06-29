from YTScrapper import *
from Process import *

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

processor = Process()
processor.transcribe_folder(output_path,whisper_model_size='base', preferred_device='cpu',language_detection=False)
processor.split_to_words_folder(output_path,whisper_model_size='base', preferred_device='cpu')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# gp_operator part

cur_valid_path = "Python_scripts/valid_ip_list.txt"
cur_raw_path = "Python_scripts/raw_ip_list.txt"
cur_agents_path = "Python_scripts/static_agents_list.txt"
storage_path = "/mnt/s01/praktyki/"
overwrite = True

validator = ip_validator(cur_valid_path, cur_raw_path, overwrite)
gp_op = gp_operator(cur_valid_path, cur_agents_path, storage_path, True, True)

validator.ip_validate()
gp_op.audio_extraction()
