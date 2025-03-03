from pathlib import Path
import ffmpeg
import numpy as np


def read_audio(path: Path | str, ch=1):
    if isinstance(path, str):
        path = Path(path)

    stream = ffmpeg.input(str(path.absolute()))
    stream = stream.output("-", format="s16le", acodec="pcm_s16le", ac=ch, ar="44100")

    try:
        data, err = stream.run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print(f"Error occurred: {e.stderr.decode()}")
        raise

    data = np.frombuffer(data, dtype=np.int16)
    data = data.reshape(-1, ch)
    data = data / 32768.0

    return data
