from django.db import models

# Create your models here.
import json
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
import vosk
import sys
import wave

def record_sound(duration = 5, fs=8000 , channels = 1):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait for the recording to complete
    print("Recording finished")
    filename = 'static/recoded.wav'
    sf.write(filename, recording, fs)
    return recording

def recognize_speech(audio_file = 'static/recoded.wav', model_path = "static/vosk-model-small-en-in-0.4"):
    model = vosk.Model(model_path)
    wf = wave.open(audio_file, 'rb')

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != 'NONE':
        print("Audio file must be WAV format mono PCM.")
        exit(1)
    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(result)
    result = rec.FinalResult()
    return result

def _response(data, url="http://localhost:11434/api/generate"):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response_text = response.text
        response_lines = response_text.splitlines()
        print(response_lines[0])
        response_json = json.loads(response_lines[0])
        return response_lines[0]
    else:
        return "Error:", response.status_code
