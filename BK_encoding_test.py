import os
import chardet

folder_path = "C:/Users/krucz/Documents/Praktyki/Nagrania/7 metrów pod ziemią – SEZON 1 (2017-2020)/"

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
            print(f"File: {filename}, Encoding: {encoding}")
