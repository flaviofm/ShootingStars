import requests
import io
import time
import wave
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import tempfile

# Replace the URL with your audio stream URL
url = 'http://192.167.189.254:5123'

# Set the sampling rate and duration of each audio clip
sample_rate = 22050
clip_duration = 5

# Create a buffer to store the audio data and header
audio_buffer = io.BytesIO()
wav_header = None

while True:
    # Make a GET request to the audio stream URL
    r = requests.get(url, stream=True)

    # Read the audio stream in chunks and write it to the buffer
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            audio_buffer.write(chunk)

            # If there's enough data in the buffer for a clip, process it
            if audio_buffer.tell() >= sample_rate * clip_duration * 2:
                # Reset the buffer position to the beginning
                audio_buffer.seek(0)

                # Create a WAV file from the audio buffer and header
                with tempfile.NamedTemporaryFile() as temp_file:
                    if wav_header is None:
                        # Read the WAV header and store it separately
                        wav_header = audio_buffer.read(44)
                    temp_file.write(wav_header)
                    temp_file.write(audio_buffer.getbuffer())
                    wav_file = wave.open(temp_file.name, 'rb')
                    wav_file.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))

                    # Read the WAV file and convert the data to a NumPy array
                    n_frames = wav_file.getnframes()
                    audio_data = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)

                    # Reshape the data to 1 channel and extract the current clip
                    n_channels = wav_file.getnchannels()
                    audio_data = np.reshape(audio_data, (-1, n_channels))
                    clip_data = audio_data[-sample_rate * clip_duration:, :]

                    # Compute the spectrogram of the clip
                    f, t, Sxx = signal.spectrogram(clip_data[:, 0], sample_rate)

                    # Display the spectrogram
                    plt.pcolormesh(t, f, 10 * np.log10(Sxx))
                    plt.ylabel('Frequency [Hz]')
                    plt.xlabel('Time [sec]')
                    plt.show()

                    # Close the WAV file
                    wav_file.close()

                # Reset the buffer to remove the processed data
                audio_buffer.seek(0)
                audio_buffer.truncate()

    # Wait for a short period before requesting the next chunk of data
    time.sleep(0.1)
