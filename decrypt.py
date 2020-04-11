import pyaudio
import wave
from numpy import sin
import struct
import bz2

RATE = 48000
FILE_OUTPUT_FILENAME = "out.pdf"
WAVE_INPUT_FILENAME = "out.wav"

wf = wave.open(WAVE_INPUT_FILENAME, 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data0 = []
data = wf.readframes(1)
i = 0
a = rate / 440
while data:
    stream.write(data)
    f = struct.unpack("h", data)[0]
    b = i / a
    c = b * 3.14159 * 2
    d = sin(c)*28670
    e = int(d)
    S = (f - e)//16 + 128
    data0.append(S)
    i += 1
    data = wf.readframes(1)
    if i % RATE == 0:
        print(i)

stream.stop_stream()
stream.close()
p.terminate()
print("read")

data0 = b''.join([bytes.fromhex("%02X"%i) for i in data0])
print("Decompress")
data0 = bz2.decompress(data0)
with open(FILE_OUTPUT_FILENAME, "wb") as f:
    f.write(data0)
