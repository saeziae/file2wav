import pyaudio
import wave
from math import sin
import struct
import bz2
from tqdm import tqdm, trange
import sys


if len(sys.argv) == 3:
    IN_FILENAME = sys.argv[1]
    WAVE_OUTPUT_FILENAME = sys.argv[2]
elif len(sys.argv) == 2:
    IN_FILENAME = sys.argv[1]
    WAVE_OUTPUT_FILENAME = sys.argv[1]+'.wav'
else:
    print("format: <in file> [<out file>]")
    sys.exit()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000


def readPart():
    with open(IN_FILENAME, "rb") as f:
        f.seek(0, 2)
        t = f.tell()
        f.seek(0, 0)
        for _ in trange(t):
            yield f.read(1)


data_byte = b''
bz = bz2.BZ2Compressor(9)
for i in readPart():
    data_byte += bz.compress(i)
data_byte += bz.flush()

data = []
i = 0
a = RATE / 440
for S in tqdm(data_byte):
    b = i / a
    c = b * 3.14159 * 2
    d = sin(c)*28670
    e = int(d)
    f = e + (S - 128)*16
    data.append(f)
    i += 1

print("WRITE")

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
wf.setframerate(RATE)
datalen = str(len(data))
wf.writeframes(struct.pack(datalen + 'h', *data))
wf.close()
print("FINISHED")
