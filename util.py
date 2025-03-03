from pathlib import Path
import numpy as np
import wave


def read_mono_wav(path: Path):
    out = read_stereo_wav(path)
    assert out.shape[1] == 1
    return out[:, 0]


def read_stereo_wav(path: Path):
    with wave.open(path.open("rb")) as wav:
        channels = wav.getnchannels()
        assert wav.getsampwidth() == 2
        assert wav.getframerate() == 44100

        data = wav.readframes(wav.getnframes())
        data = np.frombuffer(data, dtype=np.int16)
        data = data.reshape(-1, channels)
        return data / 32768.0
