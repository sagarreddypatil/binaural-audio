import numpy as np
from sadie import get_hrtf
from scipy import signal


def make_binaural(audio: np.ndarray, az: float, el: float, r: float):
    attenuation = 1.0 / (r**2)
    audio = audio * attenuation
    left, right = get_hrtf(az, el)
    binaural_left = signal.fftconvolve(audio, left)
    binaural_right = signal.fftconvolve(audio, right)

    binaural_left = binaural_left[: len(audio)]
    binaural_right = binaural_right[: len(audio)]

    # this improves sound quality prolly because
    # fftconvolve does zero padding
    binaural_left = binaural_left[len(left) :]
    binaural_right = binaural_right[len(right) :]

    return binaural_left, binaural_right
