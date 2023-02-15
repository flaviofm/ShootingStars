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


# def led_waiting_time():
#     x = random.uniform(0.2, 1.3)
#     return x

LED_PIN = 40
LED = False

#setup
# win = curses.initscr()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
print("OUTPUT FOUND")

import time

def getStarHold():
    MIN_SECS = 0.6 # minimo durata input
    return MIN_SECS + random.uniform(0.2, 3)

LAST_STAR = None #ultima stella registrata da pin
LAST_CALL = None #ultima chiamata di output
MIN_STAR = 60 #tempo minimo per una stella
MAX_STAR = 30 #attesa minima tra stelle

LED_ON = False

def output(s):
    global LAST_CALL, LED_ON, MIN_STAR, MAX_STAR
    if not LAST_CALL:
        if s:
            LAST_CALL = time.time()
            print("First STAR!")
            pin(True)
        return

    if s:
        if not LED_ON:
            if (time.time() - LAST_CALL) >= MAX_STAR:
                pin(True)
                LAST_CALL = time.time()
            else:
                print("SATELLITE")
    else:
        if not LED_ON:
            if(time.time() - LAST_CALL) >= MIN_STAR:
                output(True) #auto star if not in MIN_STAR TIME
        else:
            if (time.time() - LAST_CALL) > getStarHold():
                pin(False) #minimo durata stella
            # else:
            #     print(MIN_SECS - (time.time() - LAST_CALL))
        return

def pin(t):
    global LAST_STAR, LED_ON
    print("★" if t else "☆")
    if LAST_STAR:
        print("Star lasted {} seconds".format(time.time() - LAST_STAR))
        LAST_STAR = None
    elif t:
        LAST_STAR = time.time()
    GPIO.output(LED_PIN, GPIO.HIGH if t else GPIO.LOW)
    LED_ON = t


# def output(s):
#     global LAST_CALL, LAST_STAR
#     if(s):
#         if not LAST_CALL:
#             led(True)
#         LAST_CALL = time.time()
#     else:
#         if not LAST_CALL:
#             led(False)
#             return
#         x = led_waiting_time()
#         if (time.time() - LAST_CALL) > (MIN_SECS + x):
#             led(False)

# # def output(s):
# #     global LAST_CALL
# #     if s:
# #         LAST_CALL = LAST_CALL or time.time()
# #         led(True)
# #     elif LAST_CALL and time.time() - LAST_CALL > MIN_SECS:
# #         LAST_CALL, _ = (led(False), None)


# def led(s):
#     # print(s)
#     global LAST_STAR

#     if not LAST_STAR and not s:
#         return
    
#     if not LAST_STAR and s:
#         LAST_STAR = time.time()
#         pin(True)
#         return

#     #last star not null
#     if s:
#         LAST_STAR = time.time()
#     else:
#         if (time.time() - LAST_STAR) > 


    # if LAST_STAR and s and (time.time() - LAST_STAR) < MAX_STAR:
    #     print("SATELLITE")
    #     GPIO.output(LED_PIN, GPIO.LOW)
    #     return

    # if s:
    #     LAST_STAR = time.time()

    # if not LAST_STAR:
    #     return
    # if (time.time() - LAST_STAR) > MIN_STAR:
    #     print("CHECK")
    #     GPIO.output(LED_PIN, GPIO.HIGH)
    #     LAST_STAR = time.time()
    #     return



        

print("1/3 OUTPUT MODULE LOADED")

CHUNK_SIZE = 1024
SAMPLE_RATE = 22050
FORMAT = pyaudio.paInt32

# THRESHOLD_AMP = 900
# THRESHOLD_FRQ = 1300
THRESHOLD_AMP = 32727 + 500
THRESHOLD_FRQ = 0.05

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
    # if(amplitude > 32761 + 500 or amplitude < 32761 - 500 ):
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!! Amplitude: {}, Frequency: {}".format(amplitude, max_freq))
    # if(amplitude > THRESHOLD_AMP and max_freq > THRESHOLD_FRQ):
    # print(max_freq)
    if(amplitude > THRESHOLD_AMP and max_freq < THRESHOLD_FRQ):
        output(True)
    else: 
        output(False)





################################################################
#AUDIO
import urllib.request
import numpy as np
import struct


# FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 22050
URL = 'http://192.167.189.254:5123'
SAMPLE_RATE = 5
THRESHOLD = 0.016
# THRESHOLD = 0.05

try:
    response = urllib.request.urlopen(URL)
    print("2/3 STREAMING MODULE LOADED")
except Exception as e:
    print("exception", e)

def format_data(data):
    return np.array(struct.unpack(str(CHUNK) + "B", data), dtype="b")

def analyse(data):
    data = format_data(data)
    m = np.mean(data)
    # print(m)
    if(m < THRESHOLD and m > -THRESHOLD):
    # if(m > TARA_OVERFLOW or m < -TARA_OVERFLOW):
        output(True)
    else:
        output(False)


chunks = []
if not response:
    print("RESPONSE ERROR")
print("3/3 ANALYZE MODULE LOADED")

reading = True
while reading:
    chunk = response.read(CHUNK)
    if not chunk:
        reading = False
    else:
        analyse(chunk)
        # process_audio(chunk)

