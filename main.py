from pathlib import Path

import numpy as np
from scipy import signal
import dearpygui.dearpygui as dpg

from player import AudioPlayer
from sadie import get_hrtf
from util import read_audio


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
    binaural_left, binaural_right = (
        binaural_left[len(left) :],
        binaural_right[len(right) :],
    )
    return binaural_left, binaural_right


test_audio = read_audio(Path("test.mp3"), 1)[:,0]
player = AudioPlayer()

az = 0
el = 0
r = 2

dpg.create_context()
dpg.create_viewport(title="Binaural Audio")
dpg.setup_dearpygui()

with dpg.window(tag="primary", no_resize=True):
    az_slider = dpg.add_slider_float(
        label="azimuth", default_value=az, min_value=0, max_value=360
    )
    el_slider = dpg.add_slider_float(
        label="elevation", default_value=el, min_value=-90, max_value=90
    )
    r_slider = dpg.add_slider_float(
        label="radius", default_value=r, min_value=1, max_value=10
    )

    seek = dpg.add_slider_float(
        label="seek", default_value=0, min_value=0, max_value=len(test_audio)
    )

dpg.set_primary_window("primary", True)

dpg.show_viewport()

# CHUNK_SIZE = 44100 // 10
CHUNK_SIZE = 2048
FFT_SIZE = 8192
i = 0
player.start()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

    az = dpg.get_value(az_slider)
    el = dpg.get_value(el_slider)
    r = dpg.get_value(r_slider)

    if i >= len(test_audio):
        break

    i = int(dpg.get_value(seek))

    if player.len_pending() < 1:
        # print(i, az, el, r)
        audio = test_audio[i : i + FFT_SIZE]
        # left, right = audio, audio
        left, right = make_binaural(audio, az, el, r)
        assert len(left) == len(right)
        left, right = left[:CHUNK_SIZE], right[:CHUNK_SIZE]
        player.add_chunk(np.column_stack((left, right)))
        i += CHUNK_SIZE
        dpg.set_value(seek, i)


player.stop()
dpg.destroy_context()
