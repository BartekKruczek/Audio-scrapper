import time
from faster_whisper import WhisperModel

model_size = "large-v2"
model = WhisperModel(model_size, device="cpu", compute_type="float32")

start = time.time()
segments, info = model.transcribe("/mnt/s01/praktyki/gp_storage/8:10/00 [00].wav", beam_size=5)
end = time.time()
print(end-start)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))