import scipy
from scipy import fft
import numpy
import matplotlib.pyplot as plt
import pyaudio
import struct

# Settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

p = pyaudio.PyAudio()
stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

fig,ax = plt.subplots()
x = numpy.arange(0,2*CHUNK,2)
line, = ax.plot(x, numpy.random.rand(CHUNK),'r')
ax.set_ylim(-32770,32770)
ax.ser_xlim = (0,CHUNK)
fig.show()

while 1:
    data = stream.read(CHUNK, exception_on_overflow = False)
    spectrum = fft.fft( numpy.fromstring(data, dtype=numpy.float16))
    # freq = fft.fftfreq(len(spectrum))
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    line.set_ydata(spectrum)
    print(spectrum)
    fig.canvas.draw()
    fig.canvas.flush_events()