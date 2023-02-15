#OUTPUT
import datetime
import importlib.util

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


led_waiting_time = 3
last_led_time = False
led_on = False
LED_PIN = 40

#setup
# win = curses.initscr()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
print("OUTPUT FOUND")

def output(b, m=0):
    global last_led_time, led_waiting_time, led_on
    # print(b)
    now = datetime.datetime.now()
    if last_led_time:
        if((now - last_led_time).seconds < led_waiting_time):
            return
        else:
            if(b):
                last_led_time = now
                GPIO.output(LED_PIN, GPIO.HIGH)
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
    else:
        if(b):
            last_led_time = now

print("1/3 OUTPUT MODULE LOADED")
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
