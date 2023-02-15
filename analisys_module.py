import numpy as np
import struct
import curses
from scipy.fft import fft, ifft, fftfreq
from scipy import signal
import matplotlib.pyplot as plt



# TARA = 1.6357235764734
# TARA = 0.016357235764734
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
    print("data")
    print(in_data)
    # for c in in_data:
    #     d = np.array(struct.unpack(str(size) + "B", c), dtype="b")
    #     m = np.mean(d)
    #     if(m > TARA_OVERFLOW or m < -TARA_OVERFLOW):
    #         output_callback(True, m)
    #     output_callback(False, m)
    plot_spectrogram(in_data, 44100)
    # if(m > -TARA and m < TARA):
    #     output_callback(True, m)
    # output_callback(False, m)

def spectral_properties(y: np.ndarray, fs: int) -> dict:
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1 / fs)
    spec = np.abs(spec)
    amp = spec / spec.sum()
    mean = (freq * amp).sum()
    sd = np.sqrt(np.sum(amp * ((freq - mean) ** 2)))
    amp_cumsum = np.cumsum(amp)
    median = freq[len(amp_cumsum[amp_cumsum <= 0.5]) + 1]
    mode = freq[amp.argmax()]
    Q25 = freq[len(amp_cumsum[amp_cumsum <= 0.25]) + 1]
    Q75 = freq[len(amp_cumsum[amp_cumsum <= 0.75]) + 1]
    IQR = Q75 - Q25
    z = amp - amp.mean()
    w = amp.std()
    skew = ((z ** 3).sum() / (len(spec) - 1)) / w ** 3
    kurt = ((z ** 4).sum() / (len(spec) - 1)) / w ** 4

    result_d = {
        'mean': mean,
        'sd': sd,
        'median': median,
        'mode': mode,
        'Q25': Q25,
        'Q75': Q75,
        'IQR': IQR,
        'skew': skew,
        'kurt': kurt
    }

    return result_d

def plot_spectrogram(samples, sample_rate):
    print("spectro")
    # print(len(np.array(samples)))
    # d = np.array(struct.unpack("B", np.array(samples[0])), dtype="b")
    # d = np.frombuffer(samples[0], dtype="b")
    # print(d)
    frequencies, times, spectrogram = signal.spectrogram(np.frombuffer(samples[0], dtype="b"), sample_rate)
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]') 
    plt.show()



print("4/4 ANALISYS MODULE LOADED")
