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

    def cleaning_wavs(self,path): # function for cleaning folder from .wav files
        for fileName in os.listdir(Path(path)):
            if fileName.endswith('.wav') or fileName.endswith('.txt'):
                os.remove(Path(path +"\\"+ fileName))

    def filename_ext(self,path):  # function extracting list of all .wav files in folder
        files_list=[]
        for fileName in os.listdir(Path(path)):
            if fileName.endswith('.wav'):
                files_list.append(fileName)
        return files_list
            
    def transcribe(self,path, whisper_model_size='base', preferred_device='cpu',language_detection=False,filename=None): #function performs one string transcription using Whisper model. Restricted to one file
        """
        Arguments:

        path (required)     - path to  .wav file taht we want to transcribe
        whisper_model_size  - Whisper model preferance. Default value model is 'base'
        preferred_device    - device that we want to perform calculations on. Two available values are 'cpu' (default) and 'cuda'
        language_detection  - option for Whisper language detection, using first 30 seconds of recording. Default value is 'False'
        filename            - preferred transcription .txt file name. With this variable, it is possible to alter file location. Default value is None, which results in no export file

        """
        if path.endswith('.wav')==False:
            print("Error: Path has to point to .wav file! For transcribing whole folder, please use transcribe_folder.")
            return None

        model= whisper.load_model(whisper_model_size,device=preferred_device) #loading Whisper model
        transcription= model.transcribe(path) #performing basic transcription on file

        if filename is not None: #checking exporting option(filename)
            with open(Path(filename), 'w') as f: #opening and writing to file
                f.write(transcription['text'])
                f.close()

        if language_detection==True: #checking language detection option(filename)
            audio=whisper.load_audio(Path(path)) #loading audio in Whisper format
            audio=whisper.pad_or_trim(audio) #trimming audio
            mel = whisper.log_mel_spectrogram(audio).to(model.device) #converting audio to mel-spectrogram
            lang_dic=model.detect_language(mel)[1] #build-in Whisper language detection
            audio_lang_value=max(lang_dic.values()) #extracting highest probability language
            audio_lang=list(lang_dic.keys())[list(lang_dic.values()).index(audio_lang_value)]
            return [audio_lang,transcription]
        else:
            return transcription
    
    def transcribe_words(self,path,whisper_model_size='base', preferred_device='cpu',filename=None): #function performs one string per word transcription, with timestamps, using Whisper model. Restricted to one file
        """
        Arguments:

        path (required)     - path to  .wav file taht we want to transcribe
        whisper_model_size  - Whisper model preferance. Default value model is 'base'
        preferred_device    - device that we want to perform calculations on. Two available values are 'cpu' (default) and 'cuda'
        filename            - preferred transcription .txt file name. With this variable, it is possible to alter file location. Default value is None, which results in no export file
        
        """
        if path.endswith('.wav')==False:
            print("Error: Path has to point to .wav file! For transcribing whole folder, please use transcribe_words_folder.")
            return None

        model= whisper.load_model(whisper_model_size,device=preferred_device) #loading Whisper model
        transcription= model.transcribe(path,word_timestamps=True) #performing basic transcription on file

        transcription_list=[]
        for segment in transcription['segments']: #converting original data structure to easier accesible list
            for word in segment['words']:
                transcription_list.append([word['start']*1000,word['end']*1000,word['word']])

        if filename is not None: #checking exporting option(filename)
            with open(Path(filename), 'w') as f: #opening and writing to file
                for word in transcription_list:
                    f.write(f"{word[0]}_{word[1]}_{word[2]}\n")
                f.close()
            
        return transcription_list
    
    def split_to_words(self,path,whisper_model_size='base', preferred_device='cpu'): #function splits audio file to 30 seconds files according to Whisper word-transcription timestamps. Restricted to one file
        """
        Arguments:

        path (required)     - path to  .wav file taht we want to transcribe
        whisper_model_size  - Whisper model preferance. Default value model is 'base'
        preferred_device    - device that we want to perform calculations on. Two available values are 'cpu' (default) and 'cuda'
        
        """
        print("Note: In case of audio splitiing, the result is not given as variable. It is exported to .wav and .txt files. They are stored in folder, created next to original .wav file.")
        if path.endswith('.wav')==False:
            print("Error: Path has to point to .wav file! For transcribing whole folder, please use split_to_words_folder.")
            return None

        path_for_splits=path.strip(".wav")+"_splits" #creating and cleaning folder for splits
        if os.path.isdir(Path(path_for_splits))==False:
            os.mkdir(Path(path_for_splits))
        else :
            self.cleaning_wavs(path_for_splits)
        
        sound_file = AudioSegment.from_wav(Path(path)) #converting audio to AudioSegment format for processing
        sound_file = sound_file.split_to_mono()
        sound_file=sound_file[0]

        transcription_list=self.transcribe_words(path,whisper_model_size,preferred_device) #list of words with timestamp
        splits_count=0
        start_idx=0
        while True: 
            out_file_wav = path.strip(".wav")+"_splits"+"\split{0}.wav".format(splits_count) #creating path for saving .wav file
            idx=0
            transcription=''
            while transcription_list[idx][1]<transcription_list[start_idx][0]+30000: #checking for duration of split
                if idx>=start_idx:
                    transcription+=transcription_list[idx][2]
                idx+=1
                if idx==len(transcription_list)-1:
                    break
            split=sound_file[transcription_list[start_idx][0]:transcription_list[idx][1]] #trimming audio to 30 seconds split
            split.export(Path(out_file_wav), format="wav") #exporting .wav file
            with open(Path(out_file_wav.strip('.wav')+'.txt'), 'w') as f: #opening and writing to file
                    f.write(transcription)
                    f.close()
            start_idx=idx+1
            splits_count+=1
            if idx==len(transcription_list)-1:
                    break
            
        return
            
    def transcribe_folder(self,path,whisper_model_size='base', preferred_device='cpu',language_detection=False,location=os.getcwd()): # Whole folder version of transcribe function     
        """
        Arguments:

        path (required)     - path to  .wav file taht we want to transcribe
        whisper_model_size  - Whisper model preferance. Default value model is 'base'
        preferred_device    - device that we want to perform calculations on. Two available values are 'cpu' (default) and 'cuda'
        language_detection  - option for Whisper language detection, using first 30 seconds of recording. Default value is 'False'
        location            - path to desired folder, for transcriptions files to be saved
        
        """  
        print("Note: In case of folder transcription, the result is not given as variable. It is stored in .txt file, next to .py file. To specify transcription location, modify location variable.")
        for file in self.filename_ext(path):
            self.transcribe(os.path.join(path,file),whisper_model_size, preferred_device,language_detection,filename=os.path.join(location,file.strip(".wav")+".txt"))
        return None
    
    def transcribe_words_folder(self,path,whisper_model_size='base', preferred_device='cpu',location=os.getcwd()): # Whole folder version of transcribe_words function       
        """
        Arguments:

        path (required)     - path to  .wav file taht we want to transcribe
        whisper_model_size  - Whisper model preferance. Default value model is 'base'
        preferred_device    - device that we want to perform calculations on. Two available values are 'cpu' (default) and 'cuda'
        location            - path to desired folder, for transcriptions files to be saved
        
        """  
        print("Note: In case of folder transcription, the result is not given as variable. It is stored in .txt file, next to .py file. To specify transcription location, modify location variable.")
        for file in self.filename_ext(path):
            self.transcribe_words(os.path.join(path,file),whisper_model_size, preferred_device,filename=os.path.join(location,file.strip(".wav")+".txt"))
        return None
    
    def split_to_words_folder(self,path,whisper_model_size='base', preferred_device='cpu'): # Whole folder version of split_to_words function       
        """
        Arguments:

        path (required)     - path to  .wav file taht we want to transcribe
        whisper_model_size  - Whisper model preferance. Default value model is 'base'
        preferred_device    - device that we want to perform calculations on. Two available values are 'cpu' (default) and 'cuda'
        
        """
        for file in self.filename_ext(path):
            self.split_to_words(os.path.join(path,file),whisper_model_size, preferred_device) 
        return None
