import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import signal

# Define the URL of the HTTP live stream
url = 'http://192.167.189.254:5123'

# Define the size of each audio chunk (in seconds)
chunk_size = 0.1

# Define the sampling rate and number of samples per chunk
sampling_rate = 22050
samples_per_chunk = int(sampling_rate * chunk_size)

# Create a figure with three subplots for the amplitude, frequency, and spectrogram plots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Set the x and y limits for each plot
ax1.set_ylim(-1, 1)
ax2.set_xlim(0, sampling_rate/2)
ax3.set_xlim(0, chunk_size)
ax3.set_ylim(0, sampling_rate/2)

# Create arrays to store the amplitude, frequency, and spectrogram data for each chunk
amplitude_data = np.zeros((samples_per_chunk,))
frequency_data = np.zeros((samples_per_chunk,))
spectrogram_data = np.zeros((samples_per_chunk, int(sampling_rate/2)))

# Define a function to retrieve the next chunk of audio data from the HTTP live stream
def get_audio_chunk():
    response = requests.get(url, stream=True)
    chunks = response.iter_content(chunk_size=samples_per_chunk*2, decode_unicode=True)
    for chunk in chunks:
        # audio = np.fromstring(chunk, dtype=np.int16)
        audio = np.frombuffer(chunk, dtype=np.int16)
        yield audio

# Define a function to update the plots with the latest chunk of data
def update_plots(frame):
    # Retrieve the next chunk of audio data
    audio_chunk = next(get_audio_chunk())

    # Calculate the amplitude and frequency data for the chunk
    amplitude_data[:] = audio_chunk / 32767
    frequency_data, _ = signal.welch(audio_chunk, fs=sampling_rate, nperseg=samples_per_chunk)

    # Calculate the spectrogram data for the chunk
    f, t, Sxx = signal.spectrogram(audio_chunk, fs=sampling_rate, nperseg=samples_per_chunk)
    spectrogram_data[:, :-1] = spectrogram_data[:, 1:]
    spectrogram_data[:, -1] = Sxx.flatten()

    # Update the plots with the latest data
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax1.plot(amplitude_data)
    ax2.plot(frequency_data)
    ax3.imshow(spectrogram_data, aspect='auto', origin='lower')

# Use FuncAnimation to update the plots at a regular interval
ani = FuncAnimation(fig, update_plots, interval=chunk_size*1000)

# Display the live plots
plt.show()
