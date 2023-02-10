import urllib.request
import time

# def callback(in_data):
#     data = numpy.frombuffer(in_data, numpy.int32)
#     print("callback", data)

reading = False

def setup_stream():
    global response
    try:
        response = urllib.request.urlopen('http://192.167.189.254:5123')
        print("END")
    except Exception as e:
        print("exception", e)

def start_reading(callback):
    global reading, response
    if not response:
        print("RESPONSE ERROR")
        return False
    reading = True
    print("STARTING READING")
    while reading:
        chunk = response.read(512)
        if not chunk:
            reading = False
            break
        callback(chunk)
        # time.sleep(.1)
    print("LOOP BREAK")


def stop_reading():
    global reading
    reading = False
    print("STOPPING READING")

