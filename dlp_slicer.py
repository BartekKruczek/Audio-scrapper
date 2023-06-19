import yt_dlp
import subprocess
import pydub
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence

URL='https://www.youtube.com/watch?v=i-NVAhJXw44' # plik bez napisów
#URL='https://www.youtube.com/watch?v=_SCSSLGZcSE' # plik posiadający napisy autora

ydl_opts = {
    'format': 'wav/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URL)

filename='Nowciax： Mam żal do Friza [i-NVAhJXw44].wav'

if os.path.isdir('splits_'+ filename)==False:
    os.mkdir('splits_'+ filename)

sound_file = AudioSegment.from_wav(filename)
audio_chunks = split_on_silence(sound_file, 
    # must be silent for at least half a second
    min_silence_len=200,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-24
)

for i, chunk in enumerate(audio_chunks):

    out_file = "./splits_"+ filename+"/split{0}.wav".format(i)
    print("exporting "+ out_file)
    chunk.export(out_file, format="wav")
