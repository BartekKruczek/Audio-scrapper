import os
import whisper
import time

model = whisper.load_model("tiny")

folder_path = "C:/Users/krucz/Documents/Praktyki/Nagrania/7 metrów pod ziemią – SEZON 1 (2017-2020)"
output_folder = os.path.join(folder_path, "Transcripts")
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(folder_path):
    if filename.endswith(".wav"):
        file_path = os.path.join(folder_path, filename)
        output_file = os.path.join(
            output_folder, f"{os.path.splitext(filename)[0]}.txt"
        )

        start = time.time()
        result = model.transcribe(file_path)
        end = time.time()
        transcription_time = end - start
        transcription_text = result["text"]

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(transcription_text)

        print(f"Transcription for {filename} saved to: {output_file}")
        print(f"Transcription time: {transcription_time} seconds")
