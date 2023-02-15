import pyaudio
import numpy as np
#OUTPUT
import datetime
import importlib.util
import random

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
    print("GPIO imported")
except ImportError:
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """

    import FakeRPi.GPIO as GPIO
    print("FAKE GPIO imported")


def led_waiting_time():
    return random.uniform(0.8, 3)
last_led_time = False
led_on = False
LED_PIN = 40

LED = False

#setup
# win = curses.initscr()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
print("OUTPUT FOUND")

import time
LAST_CALL = None

MIN_SECS = 1.5

def output(s):
    global LAST_CALL
    if LAST_CALL is None and s:
        LAST_CALL = time.time()
        led(True)
        return

    if LAST_CALL is not None:
        if not s:
            if (time.time() - LAST_CALL) > MIN_SECS:
                led(False)
                LAST_CALL = None
        else:
            LAST_CALL = time.time()

# def output(s):
#     global LAST_CALL
#     if s:
#         LAST_CALL = LAST_CALL or time.time()
#         led(True)
#     elif LAST_CALL and time.time() - LAST_CALL > MIN_SECS:
#         LAST_CALL, _ = (led(False), None)

def led(s):
    # print(s)
    if s:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

print("1/2 OUTPUT MODULE LOADED")

CHUNK_SIZE = 1024
SAMPLE_RATE = 22050

# THRESHOLD_AMP = 900
# THRESHOLD_FRQ = 1300
THRESHOLD_AMP = 450
THRESHOLD_FRQ = 650

def process_audio(data):
    # Convert the raw audio data to a NumPy array
    audio_array = np.frombuffer(data, dtype=np.int16)

    # Calculate the amplitude of the audio chunk
    amplitude = np.max(np.abs(audio_array))

    # Apply a fast Fourier transform (FFT) to the audio chunk
    freq_domain = np.fft.fft(audio_array)

    # Convert the frequency domain data to real values
    freq_domain = np.abs(freq_domain)

    # Get the frequency bins for the FFT output
    freq_bins = np.fft.fftfreq(CHUNK_SIZE, 1/SAMPLE_RATE)

    # Find the index of the highest frequency peak
    max_freq_index = np.argmax(freq_domain)

    # Get the frequency value corresponding to the highest peak
    max_freq = freq_bins[max_freq_index]

    # Print the amplitude and frequency of the audio chunk
    # print("Amplitude: {}, Frequency: {}".format(amplitude, max_freq))
    if(amplitude > THRESHOLD_AMP and max_freq > THRESHOLD_FRQ):
        output(True)
    else: 
        output(False)


# Set up the PyAudio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)
print("2/2 STREAMING READY")

# Continuously process audio chunks
while True:
    data = stream.read(CHUNK_SIZE)
    if not data:
        print("NO")
    process_audio(data)
