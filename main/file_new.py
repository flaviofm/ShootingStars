import numpy as np
import pydub

CHUNK_SIZE = 1024
SAMPLE_RATE = 22050

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
    print("Amplitude: {}, Frequency: {}".format(amplitude, max_freq))

# Load the audio file using pydub
audio_file = pydub.AudioSegment.from_file("audiofile.m4a")

# Set up the audio data in the format required by process_audio function
audio_data = audio_file.raw_data

# Create an index to read audio data from
start_idx = 0
import pyaudio
p = pyaudio.PyAudio()
stream_out = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True)

# Continuously process audio chunks
while start_idx < len(audio_data):
    # Get the next 1024-byte chunk of audio data
    data = audio_data[start_idx:start_idx+CHUNK_SIZE]

    # Process the audio chunk
    process_audio(data)
    audio_array = np.frombuffer(data, dtype=np.int16)
    stream_out.write(data)

    # Update the index to the next chunk
    start_idx += CHUNK_SIZE
