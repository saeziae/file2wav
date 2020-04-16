import wave
from math import sin
import struct
import bz2
from tqdm import tqdm
import sys


if len(sys.argv) == 3:
    WAVE_INPUT_FILENAME = sys.argv[1]
    FILE_OUTPUT_FILENAME = sys.argv[2]
elif len(sys.argv) == 2:
    WAVE_INPUT_FILENAME = sys.argv[1]
    FILE_OUTPUT_FILENAME = sys.argv[1][:-4]
else:
    print("format: <in file> [<out file>]")
    sys.exit()


wf = wave.open(WAVE_INPUT_FILENAME, 'rb')

data0 = []
frames = wf.getnframes()
data = wf.readframes(frames)
i = 0
a = wf.getframerate() / 440
b = struct.unpack(str(frames)+"h", data)

for f in tqdm(b):
    b = i / a
    c = b * 3.14159 * 2
    d = sin(c)*28670
    e = int(d)
    S = (f - e)//16 + 128
    data0.append(S)
    i += 1


print("already read")
print("Decompressing")
data1 = b''
bz = bz2.BZ2Decompressor()
for i in tqdm(data0):
    data1 += bz.decompress(bytes().fromhex("%02X" % i), max_length=-1)

with open(FILE_OUTPUT_FILENAME, "wb") as f:
    f.write(data1)
