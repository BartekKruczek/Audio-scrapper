import yt_dlp
import subprocess
import pydub
import os
import numpy as np
import time
import whisper

from pathlib import Path
from pydub import AudioSegment

class Process:

    def __init__(self):
        pass

    def cleaning_wavs(path):
        for fileName in os.listdir(Path(path)):
            if fileName.endswith('.wav') or fileName.endswith('.txt'):
                os.remove(Path(path +"\\"+ fileName))

    def filename_ext(path):
        for fileName in os.listdir(Path(path)):
            if fileName.endswith('.wav'):
                return fileName
            
    def transcribe_whole(self,path, whisper_model_size='base', preferred_device='cpu',language_detection='False'):
        model== whisper.load_model(whisper_model_size,device=preferred_device)
        transcription= model.transcribe(path+filename)

        if language_detection==True:
            audio=whisper.load_audio(Path(out_file))
            audio=whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            lang_dic=model.detect_language(mel)[1]
            audio_lang_value=max(lang_dic.values())
            audio_lang=list(lang_dic.keys())[list(lang_dic.values()).index(audio_lang_value)]
            return [audio_lang,transcription]
        else:
            return transcription
    
    def transcribe_words(self,path,filename=None,whisper_model_size='base', preferred_device='cpu'):
        model== whisper.load_model(whisper_model_size,device=preferred_device)
        transcription= model.transcribe(path+filename,word_timestamps=True)

        transcription_list=[]
        for segment in transcription['segments']:
            for word in segment['words']:
                transcription_list.append([word['start']*1000,word['end']*1000,word['word']])

        if filename is not None:
            with open(filename, 'w') as f:
                f.write(transcription_list)
                f.close()
            
        return transcription_list
    
    #def split_to_words(self,):

        

        





        
    





