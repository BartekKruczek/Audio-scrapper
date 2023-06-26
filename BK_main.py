"""
Z tego poziomu odpalamy wszystkie skrypty
"""
import subprocess

# Uruchomienie pierwszego skryptu i sprawdzenie, czy zakończył się sukcesem
try:
    subprocess.run(["python", "BK_yt_audio_transcript.py"], check=True)
except subprocess.CalledProcessError:
    print("Błąd: Pierwszy skrypt nie został wykonany poprawnie")

# Uruchomienie drugiego skryptu
subprocess.run(["python", "BK_whisper.py"])
