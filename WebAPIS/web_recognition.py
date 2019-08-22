import sys
from subprocess import call
from pathlib import Path

import numpy as np
from scipy.io import wavfile

import speech_recognition as sr

from homophone import text_to_num


r = sr.Recognizer()

audio_dir = Path('../BookingCapchaGenerator/res/')

# setup your path to sox here:
SOX_PATH = '/usr/local/bin/sox'
if not Path.exists(Path(SOX_PATH)):
    print('install sox or setup path to sox properly')
    sys.exit(1)

command = SOX_PATH + ' {} -r 44100 {}'

audio_path = audio_dir / '0_8.wav'
sox_out_path = str(audio_path).replace('.wav', '_sox.wav')

call(command.format(audio_path, sox_out_path), shell=True)

data_file = wavfile.read(sox_out_path)
# Convert `data` to 32 bit integers:
data = data_file[1]
data = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
wavfile.write(sox_out_path, 44100, data)

out_audio = sr.AudioFile(sox_out_path)
with out_audio as source:
    audio = r.record(source)

print('Sphinx:')
sph = r.recognize_sphinx(audio)
sph_nums = [text_to_num(num) for num in sph.split()]
print(' '.join(sph_nums))

print('Google:')
goo = r.recognize_google(audio)
goo_nums = [text_to_num(num) for num in goo.split()]
print(goo_nums)

print('Houndify:')
HOUNDIFY_CLIENT_ID = " "  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = " "

hou = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID,client_key=HOUNDIFY_CLIENT_KEY)
hou_nums = [text_to_num(num) for num in hou.split()]
print(hou_nums)

print('Wit.ai:')
WIT_AI_KEY = " "
wit = r.recognize_wit(audio, key=WIT_AI_KEY)
wit_nums = [text_to_num(num) for num in wit.split()]
print(wit_nums)