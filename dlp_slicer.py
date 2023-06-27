import yt_dlp
import subprocess
import pydub
import os
import numpy as np
import requests
import time
#import pycld2 as cld2

import whisper
from faster_whisper import WhisperModel

from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import db_to_float

URL='https://www.youtube.com/watch?v=i-NVAhJXw44' # plik bez napisów
#URL='https://www.youtube.com/watch?v=_SCSSLGZcSE' # plik posiadający napisy autora
#URL='https://www.youtube.com/watch?v=S2Ww3rX-piw' # plik z tłem

path=os.getcwd()+"\\nagrania\\"

#model = WhisperModel("medium",device='cpu', compute_type="int8")
model = whisper.load_model("small",device='cuda')

def cleaning_wavs(path):
    for fileName in os.listdir(Path(path)):
        if fileName.endswith('.wav') or fileName.endswith('.txt'):
            os.remove(Path(path +"\\"+ fileName))

def filename_ext(path):
    for fileName in os.listdir(Path(path)):
        if fileName.endswith('.wav'):
            return fileName
        
        
if os.path.isdir(path)==True:
    cleaning_wavs(path)


ydl_opts = {
    'format': 'wav/bestaudio/best',
    'outtmpl': path+'%(title)s.%(ext)s',
    #'proxy': '139.144.24.46:8080',
    #'proxy': '82.145.46.190:3128',
    #'proxy': '20.219.111.119:8080',
    #'proxy': '20.219.108.109:8080',
    #'proxy': '95.217.167.241:8080',
    #'proxy': '165.232.114.200:8080',
    #'proxy': '95.56.254.139:3128',
    #'proxy': '4.193.164.48:3128',
    #'proxy': '47.88.29.108:8084',
    #'socket_timeout': '20',
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URL)

filename=filename_ext(path)

# print(requests.get('https://ident.me').text)

# proxies = {
#      'http': 'socks5h://localhost:9150',
#      'https': 'socks5h://localhost:9150'
# }

# headers = { 'User-Agent': UserAgent().random }
# with Controller.from_port(port = 9051) as c:
#             c.authenticate()
#             c.signal(Signal.NEWNYM)
#             print(f"Your IP is : {requests.get('https://ident.me', proxies=proxies, headers=headers).text}  ||  User Agent is : {headers['User-Agent']}")

# # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# #     error_code = ydl.download(URL)

# if os.path.isdir(Path(path+'splits_'+ filename.strip('.wav')))==False:
#     os.mkdir(Path(path+'splits_'+filename.strip('.wav')))
# else :
#     cleaning_wavs(path+'splits_'+filename.strip('.wav')) 


sound_file = AudioSegment.from_wav(Path(path+filename))
sound_file = sound_file.split_to_mono()
sound_file=sound_file[0]
sound_file.export(Path(path+filename),format='wav')
audio_chunks = split_on_silence(sound_file, 

    min_silence_len=200,

    silence_thresh=40 * np.log10(abs(sound_file.rms)/32768)
)
# for i, chunk in enumerate(audio_chunks):

#     out_file = path+"splits_"+ filename.strip('.wav')+"\split{0}.wav".format(i)
#     print("exporting "+ out_file)
#     chunk.export(Path(out_file), format="wav")
    #audio=whisper.load_audio(Path(out_file))
    #audio=whisper.pad_or_trim(audio)
    #mel = whisper.log_mel_spectrogram(audio).to(model.device)
    #lang_dic=model.detect_language(mel)[1]
    #audio_lang_value=max(lang_dic.values())
    #audio_lang=list(lang_dic.keys())[list(lang_dic.values()).index(audio_lang_value)]
    #print(audio_lang)
# results,info = model.transcribe(path+filename, beam_size=5)
result=model.transcribe(path+filename,word_timestamps=True)
audio=whisper.load_audio(Path(path+filename))
audio=whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)
lang_dic=model.detect_language(mel)[1]
audio_lang_value=max(lang_dic.values())
audio_lang=list(lang_dic.keys())[list(lang_dic.values()).index(audio_lang_value)]
print(audio_lang)
with open(Path(path+filename.strip('.wav')+'.txt'), 'w') as f:
    for segment in result['segments']:
        for word in segment['words']:
            f.write(f"{word['start']}_{word['end']}_{word['word']}\n")
    f.close()
# for result in results:
#     with open(Path(path+filename.strip('.wav')+'.txt'), 'w') as f:
#              f.write(f"{result.start},{result.end},{result.text}\n")
# f.close()
    # if audio_lang=='pl':
    #     with open(Path(out_file.strip('.wav')+'.txt'), 'w') as f:
    #         f.write(result["text"])
    #         f.close()

os.remove(Path(path + filename))   


