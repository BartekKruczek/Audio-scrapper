from YTScrapper import *
from Process import *
from ip_tester_2_0 import *
from gp_operations import *

playlist_urls = ["playlist_url_example", "playlist_url_example_2"]
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

cur_valid_path = "txt_storage/valid_ip_list.txt"
cur_raw_path = "txt_storage/raw_ip_list.txt"
cur_agents_path = "txt_storage/static_agents_list.txt"
storage_path = "/storage_path/"
overwrite = True

validator = ip_validator(cur_valid_path, cur_raw_path, overwrite)
gp_op = gp_operator(cur_valid_path, cur_agents_path, storage_path, True, True)

validator.ip_validate()
gp_op.audio_extraction()
