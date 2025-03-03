from pathlib import Path
import numpy as np
import wave


def read_mono_wav(path: Path):
    with wave.open(path.open("rb")) as wav:
        assert wav.getnchannels() == 1
        assert wav.getsampwidth() == 2
        assert wav.getframerate() == 44100

        data = wav.readframes(wav.getnframes())
        data = np.frombuffer(data, dtype=np.int16)
        return data / 32768.0
