import requests
from pydub import AudioSegment
from pydub.playback import play

textToSpeak = "hello suprabho how are you your account balance is 400k now tell me a joke ha ha ha"
urlPiper = "http://localhost:5000"
outputFilename = "output.wav"

payload = {'text': textToSpeak}

# Make HTTP GET Request
r = requests.get(urlPiper, params=payload)

# Save Response to File
with open(outputFilename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

# Load Audio File
audio = AudioSegment.from_file(outputFilename, format="wav")

# Play Audio
play(audio)
