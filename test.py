import pyaudio
import wave

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024
RECORD_SECONDS = 5

# Create an instance of PyAudio
pa = pyaudio.PyAudio()

# Open the microphone for recording
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                 input=True, frames_per_buffer=CHUNK_SIZE)

print("Recording...")

# Record audio for RECORD_SECONDS
frames = []
for i in range(0, int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
    data = stream.read(CHUNK_SIZE)
    frames.append(data)

print("Finished recording.")

# Stop the microphone recording
stream.stop_stream()
stream.close()

# Save the recorded audio as a WAV file
wf = wave.open("recorded_audio.wav", "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(pa.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()

# Open the saved WAV file for playback
wf = wave.open("recorded_audio.wav", "rb")

# Create an instance of PyAudio for playback
stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(),
                 rate=wf.getframerate(),
                 output=True)

print("Playing recorded audio...")

# Play the recorded audio from the WAV file
data = wf.readframes(CHUNK_SIZE)
while data:
    stream.write(data)
    data = wf.readframes(CHUNK_SIZE)

print("Finished playing recorded audio.")

# Stop the audio playback
stream.stop_stream()
stream.close()

# Terminate the PyAudio instance
pa.terminate()
