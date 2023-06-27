import os
import whisper
import time
import warnings

try:
    model = whisper.load_model("tiny")

    # folder_path = "/mnt/s01/praktyki/storage/Nagrania"
    # output_path = "/mnt/s01/praktyki/storage"
    folder_path = "C:/Users/krucz/Documents/Praktyki/Nagrania"
    output_path = "C:/Users/krucz/Documents/Praktyki"
    output_folder = os.path.join(output_path, "Transkrypcja_Whisper")
    os.makedirs(output_folder, exist_ok=True)

    # Ignorowanie ostrzeżenia dotyczącego precyzji FP16 na CPU
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".wav"):
                file_path = os.path.join(root, filename)
                output_subfolder = os.path.join(output_folder, os.path.basename(root))
                os.makedirs(output_subfolder, exist_ok=True)
                output_file = os.path.join(
                    output_subfolder, f"{os.path.splitext(filename)[0]}.txt"
                )
                print("Tłumaczę plik...")
                start = time.time()
                result = model.transcribe(file_path)
                end = time.time()
                transcription_time = end - start
                transcription_text = result["text"]

                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(transcription_text)

                print(f"Transcription for {filename} saved to: {output_file}")
                print(f"Transcription time: {transcription_time} seconds")

    # Przywracanie pierwotnych ustawień ostrzeżeń
    warnings.filterwarnings("default")
except Exception as e:
    print(str(e))
