import time
import os
import torch
from faster_whisper import WhisperModel

model_size = "large-v2"
model = WhisperModel(model_size, device="cuda", compute_type="float32")

start = time.time()
segments, info = model.transcribe("tester.wav", beam_size=5)
end = time.time()
print("Transcription time : " + str(end-start))

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

os.chdir("transcript")
iter = 0
with open('tester-lv2-cuda-faster', 'w') as f:
    for segment in segments:
        iter += 1
        print("Segment : " + str(iter))
        f.write(str(segment.text))
#    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
end2 = time.time()
print("Whole time : " + str(end2 - start))
os.chdir('..')
