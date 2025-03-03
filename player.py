import time
from threading import Thread, Lock

import pyaudio

p = pyaudio.PyAudio()


class AudioPlayer:
    def __init__(self):
        self.lock = Lock()
        self.pending = []

        self.running = False

    def add_chunk(self, chunk):
        with self.lock:
            self.pending.append(chunk)

    def len_pending(self):
        with self.lock:
            return len(self.pending)

    def pop_chunk(self):
        with self.lock:
            return self.pending.pop(0)

    def run(self):
        while self.running:
            while self.len_pending() == 0 and self.running:
                time.sleep(0.0)

            audio = self.pop_chunk()
            audio = (audio * 32767).astype("int16").tobytes()
            self.stream.write(audio)

    def start(self):
        self.stream = p.open(
            format=pyaudio.paInt16, channels=2, rate=44100, output=True
        )
        self.running = True
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.stream.stop_stream()
