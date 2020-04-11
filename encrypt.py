import pyaudio
import wave
from numpy import sin
import struct
import bz2

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
IN_FILENAME = "in.pdf"
WAVE_OUTPUT_FILENAME = "out.wav"

data_byte = b''
with open(IN_FILENAME, "rb") as f:
    print("COMPRESSING")
    data_byte = bz2.compress(f.read(), compresslevel=9)
w = len(data_byte)
data = []
i = 0
a = RATE / 440
for S in data_byte:
    b = i / a
    c = b * 3.14159 * 2
    d = sin(c)*28670
    e = int(d)
    f = e + (S - 128)*16
    data.append(f)

    i += 1
    if w >= 50:
        if i % (w//50) == 0:
            print(str(i*100//w)+"%")

print("WRITE")

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
wf.setframerate(RATE)
datalen = str(len(data))
wf.writeframes(struct.pack(datalen + 'h', *data))
wf.close()
print("FINISHED")