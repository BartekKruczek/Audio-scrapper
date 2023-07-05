import whisper
import time

model = whisper.load_model("medium", device="cpu")
start = time.time()
result = model.transcribe("/mnt/s01/praktyki/gp_storage/8:10/00 [00].wav")
end = time.time()
print(end-start)
print(result['text'])
