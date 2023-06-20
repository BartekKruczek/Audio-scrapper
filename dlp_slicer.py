import yt_dlp
import subprocess
import pydub
import os
import numpy as np

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import db_to_float

URL='https://www.youtube.com/watch?v=i-NVAhJXw44' # plik bez napisów
#URL='https://www.youtube.com/watch?v=_SCSSLGZcSE' # plik posiadający napisy autora
#URL='https://www.youtube.com/watch?v=S2Ww3rX-piw' # plik z tłem

path=os.getcwd()
print(path)
def cleaning_wavs(path):
    for fileName in os.listdir(path):
        if fileName.endswith('.wav'):
            os.remove(path + '\\' + fileName)

cleaning_wavs(path)

ydl_opts = {
    'format': 'wav/bestaudio/best',
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URL)

filename='Nowciax： Mam żal do Friza [i-NVAhJXw44]'

if os.path.isdir('splits_'+ filename)==False:
    os.mkdir('splits_'+ filename)

sound_file = AudioSegment.from_wav(filename+'.wav')
sound_file = sound_file.split_to_mono()
sound_file=sound_file[0]
sound_file.export(filename+'.wav',format='wav')
audio_chunks = split_on_silence(sound_file, 

    min_silence_len=200,

    silence_thresh=40 * np.log10(abs(sound_file.rms)/32768)
)
for i, chunk in enumerate(audio_chunks):

    out_file = "./splits_"+ filename+"/split{0}.wav".format(i)
    print("exporting "+ out_file)
    chunk.export(out_file, format="wav")
