"""
Z tego poziomu odpalamy wszystkie skrypty
"""
import subprocess

subprocess.run(["python", "BK_yt_audio_transcript.py"])

subprocess.run(["python", "BK_whisper.py"])
