import pyaudio
import numpy as np
from scipy import signal
from pathlib import Path
from threading import Thread
import dearpygui.dearpygui as dpg
from kemar import get_hrtf
from util import read_mono_wav


def make_binaural(audio: np.ndarray, el: float, az: float, r: float):
    attenuation = 1.0 / (r**2)
    audio = audio * attenuation
    left, right = get_hrtf(el, az)
    binaural_left = signal.fftconvolve(audio, left)
    binaural_right = signal.fftconvolve(audio, right)

    binaural_left = binaural_left[: len(audio)]
    binaural_right = binaural_right[: len(audio)]
    return binaural_left, binaural_right


test_audio = read_mono_wav(Path("test.wav"))

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True)


def write_to_stream(left: np.ndarray, right: np.ndarray):
    assert len(left) == len(right)
    audio = np.column_stack((left, right))
    audio = (audio * 32767).astype(np.int16).tobytes()
    stream.write(audio)


chunks = []


def writer():
    global chunks
    while len(chunks) == 0:
        pass

    while True:
        if len(chunks) > 0:
            write_to_stream(*chunks.pop(0))
        else:
            print("stalled")


writer_thr = Thread(target=writer, daemon=True)
writer_thr.start()

az = 0
el = 0
r = 2

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Binaural"):
    az_slider = dpg.add_slider_float(
        label="azimuth", default_value=az, min_value=0, max_value=360
    )
    el_slider = dpg.add_slider_float(
        label="elevation", default_value=el, min_value=-40, max_value=90
    )
    r_slider = dpg.add_slider_float(
        label="radius", default_value=r, min_value=1, max_value=10
    )

dpg.show_viewport()

# CHUNK_SIZE = 44100 // 10
CHUNK_SIZE = 8192
i = 0
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

    az = dpg.get_value(az_slider)
    el = dpg.get_value(el_slider)
    r = dpg.get_value(r_slider)

    if i >= len(test_audio):
        break
    if len(chunks) <= 1:
        # print(i, az, el, r)
        audio = test_audio[i : i + CHUNK_SIZE]
        # left, right = audio, audio
        left, right = make_binaural(audio, el, az, r)
        assert len(left) == len(right)
        assert len(left) == CHUNK_SIZE
        chunks.append((left, right))
        i += CHUNK_SIZE

dpg.destroy_context()
