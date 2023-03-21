import time


import wave
import sys

import pyaudio

import socket

sock = socket.socket()
sock.connect(('localhost', 5050))

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
# RATE = 10000
RECORD_SECONDS = 5

with wave.open('output.wav', 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=1)

    print('Recording...')
    # for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
    #     # print(int.from_bytes(stream.read(CHUNK),"little", signed=True))
    #     wf.writeframes(stream.read(CHUNK))
    sock.send("server<~$4<~$gag<~$".encode())
    while True:
        try:
            # wf.writeframes(stream.read(CHUNK))
            sound = stream.read(CHUNK)
            sock.send(sound)
        except:
            break
    print('Done')
    sock.send("server<~$4<~$gag<~$".encode())

    stream.close()
    p.terminate()
    time.sleep(0.5)
    sock.close()
