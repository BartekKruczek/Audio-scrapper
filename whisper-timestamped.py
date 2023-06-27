import whisper_timestamped as whisper
import json
import time

audio = whisper.load_audio(
    "C:/Users/krucz/Documents/Praktyki/Nagrania/PLUWDBVpNIE52-QW1DuVyQu-QWLCtIGgJX/_1Hqu_Up3NA.wav"
)

model = whisper.load_model("base", device="cpu")
start = time.time()
result = whisper.transcribe(
    model,
    audio,
    detect_disfluencies=True,
    vad=True,
    language="pl",
    beam_size=5,
    best_of=5,
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
)
end = time.time()
transcription_time = end - start
print(str(transcription_time))
print(json.dumps(result, indent=2, ensure_ascii=False))
