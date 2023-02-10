#IMPORTS
from chunk import Chunk
import pyaudio
import numpy as np
# import custom modules
import output_module as OM
# import wifi_module as WM
# import stream_module as SM
import analisys_module as AM
import request_module as RM

# import stream_analysis_module as SAM
##VARIABLES
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = CHUNK

# def analysis(in_data, frame_count, time_info, flag):
#     audio_data = np.fromstring(in_data, dtype=np.float32)
#     print(audio_data)
#     return None, pyaudio.paContinue

#START
print("Booting up Shooting Stars")
##OUTPUT SETUP
OM.output_setup()

##WIFI
# if(not WM.wifi_scan()):
#     print("Cannot connect to wifi")
#     sys.exit()
# else:
#     print("WIFI CONNECTED")

# ##ANALISYS
# AM.setup_output_callback(OM.output_led)
AM.setup_output_callback(OM.output_full)

##STREAM
# SM.channel_setup(FORMAT, CHANNELS, RATE, CHUNK)
# SM.stream_setup()

RM.setup_stream()
print("END2")

RM.start_reading(AM.arrayCallback)
print("END3")

# ##ANALISYS
# # print(f'[]', end='\r')
# data = SM.read_data(CHUNK)
# while data:
#     res = AM.analyse_data(data, CHUNK)
#     OM.output_led(res)
#     data = SM.read_data(CHUNK)
#     # time.sleep(.5)
# SM.close_stream()

# SAM.setup()
# SAM.start_streaming()




##END
# print("Stopping Shooting Stars")
# time.sleep(1000)
