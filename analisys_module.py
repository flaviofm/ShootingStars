import numpy as np
import struct
import curses
from scipy.fft import fft, ifft, fftfreq


# TARA = 1.6357235764734
TARA = 0.016357235764734
TARA = 0.0016357235764734
# TARA_OVERFLOW = 36
# win = curses.initscr()



def format_data(data, CHUNK):
    return np.array(struct.unpack(str(CHUNK) + "B", data), dtype="b")

def format_data_array(data, CHUNK):
    tot = 0
    for e in data:
        d = np.array(struct.unpack(str(CHUNK) + "B", e), dtype="b")
        tot += np.mean(d)
    tot /= len(data)
    print(str(tot))
    return np.mean(tot)

# def analyse_data(data, CHUNK):
#     data = format_data(data, CHUNK)
#     m = np.mean(data)
#     # print(f'Signal: ' + str(m))
#     win.clear()
#     # win.refresh()
#     # n = m//TARA
#     win.addstr('Signal: ' + str(m))
#     if(m > TARA or m < -TARA):
#         win.addstr('\n[★]')
#         win.refresh()
#         win.refresh()
#         return True
#     win.addstr('\n[☆]')
#     win.refresh()
#     return False

# def callback(in_data, frame_count, time_info, status):
#     analyse_data(in_data)
#     return (in_data, pyaudio.paContinue)

def setup_output_callback(cb):
    global output_callback
    output_callback = cb
    print("OUTPUT CALLBACK SETTED")


# def currentCallback(in_data, size):
#     global output_callback
#     if not output_callback:
#         print("No output callback")
#         return False
#     data = format_data(in_data, size)
#     print("callback", data)
#     m = np.mean(data)
#     if(m > TARA or m < -TARA):
#         output_callback(True, m)
#     output_callback(False, m)

def currentCallback(in_data, size):
    global output_callback
    if not output_callback:
        print("No output callback")
        return False
    # data = np.frombuffer(in_data, np.int32)
    data = format_data(in_data, size)
    # print(d)

    # # Number of sample points
    # N = 600
    # # sample spacing
    # T = 1.0 / 800.0
    # yf = fft(data)
    # xf = fftfreq(N, T)[:N//2]
    # import matplotlib.pyplot as plt
    # plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
    # plt.grid()
    # plt.show()

    # print("callback", data)
    # d = fft(data)
    m = np.mean(data)
    if(m.all() > TARA or m.all() < -TARA):
    # if(m > TARA_OVERFLOW or m < -TARA_OVERFLOW):
        output_callback(True, m)
    output_callback(False, m)

def arrayCallback(in_data, size):
    global output_callback
    if not output_callback:
        print("No output callback")
        return False
    # data = np.frombuffer(in_data, np.int32)
    m = format_data_array(in_data, size)
    # for c in in_data:
    #     d = np.array(struct.unpack(str(size) + "B", c), dtype="b")
    #     m = np.mean(d)
    #     if(m > TARA_OVERFLOW or m < -TARA_OVERFLOW):
    #         output_callback(True, m)
    #     output_callback(False, m)
    if(m > -TARA and m < TARA):
        output_callback(True, m)
    output_callback(False, m)



print("4/4 ANALISYS MODULE LOADED")
