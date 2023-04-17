import pyaudio
import numpy as np
import pyroomacoustics as pra

# Audio parameters
RATE = 44100
CHANNELS = 1
CHUNK_SIZE = 1024

# Create instances of PyAudio
pa = pyaudio.PyAudio()
stream1 = pa.open(format=pyaudio.paFloat32, channels=CHANNELS, rate=RATE,
                  input=True, input_device_index=0, frames_per_buffer=CHUNK_SIZE)
stream2 = pa.open(format=pyaudio.paFloat32, channels=CHANNELS, rate=RATE,
                  input=True, input_device_index=1, frames_per_buffer=CHUNK_SIZE)

# Create a microphone array instance
mic_array = pra.MicrophoneArray(np.array([[0, 0], [0.1, 0]]).T, RATE)

while True:
    # Read audio data from the two microphones
    data1 = stream1.read(CHUNK_SIZE)
    data2 = stream2.read(CHUNK_SIZE)

    # Convert the audio data to a numpy array
    x = np.frombuffer(data1, dtype=np.float32)
    y = np.frombuffer(data2, dtype=np.float32)

    # Stack the audio data from both channels into a 2D array
    X = np.column_stack((x, y))

    # Compute the direction of arrival of the sound
    doa = mic_array.locate_sources(X, fs=RATE, num_src=1)[0][0]

    # Print the direction of arrival in degrees
    print('DOA:', np.rad2deg(doa))
