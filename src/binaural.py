import numpy as np
from sadie import get_hrtf
from scipy import fft


def make_binaural(audio: np.ndarray, az: float, el: float, r: float):
    attenuation = 1.0 / (r**2)
    audio = audio * attenuation
    left, right = get_hrtf(az, el)
    assert len(left) == len(right)

    N = len(audio) + len(left) - 1
    N_opt = int(2**(np.ceil(np.log2(N))))

    audio_fft = fft.rfft(audio, N_opt)
    left_fft = fft.rfft(left, N_opt)
    right_fft = fft.rfft(right, N_opt)

    binaural_left = fft.irfft(audio_fft * left_fft, N_opt)[: len(audio)]
    binaural_right = fft.irfft(audio_fft * right_fft, N_opt)[: len(audio)]

    return binaural_left, binaural_right


if __name__ == "__main__":
    import sys
    from util import read_audio

    fn = sys.argv[1]
    audio = read_audio(fn)[:, 0]

    left, right = make_binaural(audio[:8192], 0, 0, 1)
