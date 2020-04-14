#import pyaudio
import wave
from numpy import sin
import struct
import bz2
from tqdm import trange
import sys


if len(sys.argv) == 3:
    WAVE_INPUT_FILENAME = sys.argv[1]
    FILE_OUTPUT_FILENAME = sys.argv[2]
elif len(sys.argv) == 2:
    WAVE_INPUT_FILENAME = sys.argv[1]
    FILE_OUTPUT_FILENAME = sys.argv[1]+'.bin'
else:
    print("format: <in file> [<out file>]")
    sys.exit()


wf = wave.open(WAVE_INPUT_FILENAME, 'rb')

#p = pyaudio.PyAudio()

#stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                channels=wf.getnchannels(),
#                rate=wf.getframerate(),
#                output=True)

data0 = []
frames = wf.getnframes()
#data = wf.readframes(1)
i = 0
a = wf.getframerate() / 440

for _ in trange(frames):
    data = wf.readframes(1)
    #stream.write(data)
    f = struct.unpack("h", data)[0]
    b = i / a
    c = b * 3.14159 * 2
    d = sin(c)*28670
    e = int(d)
    S = (f - e)//16 + 128
    data0.append(S)
    i += 1
    

#stream.stop_stream()
#stream.close()
#p.terminate()
print("read")

data0 = b''.join([bytes.fromhex("%02X" % i) for i in data0])
print("Decompress")
data0 = bz2.decompress(data0)
with open(FILE_OUTPUT_FILENAME, "wb") as f:
    f.write(data0)
