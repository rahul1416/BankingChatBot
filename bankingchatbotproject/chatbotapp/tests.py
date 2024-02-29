from django.test import TestCase
import requests
from pydub import AudioSegment
from pydub.playback import play


def tts(textToSpeak,urlPiper="http://localhost:5000"):
    outputFilename = "output.wav"
    payload = {'text': textToSpeak}
    r = requests.get(urlPiper, params=payload)
    with open(outputFilename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    audio = AudioSegment.from_file(outputFilename, format="wav")
    play(audio)
tts("Wecome suprabho saha chithambram to trio group your account number is three and you have 1415 rs in your bank")