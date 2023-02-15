
# Load audio file to match against
y, sr = librosa.load('audiofile.m4a')
mfccs = librosa.feature.mfcc(y=y, sr=sr)
mfccs_delta = librosa.feature.delta(mfccs)
mfccs_delta2 = librosa.feature.delta(mfccs, order=2)
audio_embedding = np.vstack([mfccs, mfccs_delta, mfccs_delta2])

response = requests.get(URL, stream=True)
for chunk in response.iter_content(chunk_size=CHUNK*sr):
    y = np.frombuffer(chunk, dtype=np.int16) / 32768.0
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    mfccs_delta = librosa.feature.delta(mfccs)
    mfccs_delta2 = librosa.feature.delta(mfccs, order=2)
    chunk_embedding = np.vstack([mfccs, mfccs_delta, mfccs_delta2])

    # Compute distance metric between chunk embedding and audio embedding
    distance = 1 - np.dot(chunk_embedding, audio_embedding.T) / (
            np.linalg.norm(chunk_embedding, axis=1) * np.linalg.norm(audio_embedding, axis=1))
    similarity = np.mean(distance)
    print(distance)
    print(similarity)