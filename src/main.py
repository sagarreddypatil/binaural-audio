import click

import numpy as np
import dearpygui.dearpygui as dpg

from binaural import make_binaural
from player import AudioPlayer
from util import read_audio


@click.command()
@click.argument("input_file")
def main(input_file: str):
    test_audio = read_audio(input_file, 1)[:, 0]
    player = AudioPlayer()

    az = 0
    el = 0
    r = 2

    dpg.create_context()
    dpg.create_viewport(title="Binaural Audio")
    dpg.setup_dearpygui()

    with dpg.window(tag="primary", no_resize=True):
        az_slider = dpg.add_slider_float(label="azimuth", default_value=az, min_value=0, max_value=360)
        el_slider = dpg.add_slider_float(label="elevation", default_value=el, min_value=-90, max_value=90)
        r_slider = dpg.add_slider_float(label="radius", default_value=r, min_value=1, max_value=10)

        seek = dpg.add_slider_float(label="seek", default_value=0, min_value=0, max_value=len(test_audio))

    dpg.set_primary_window("primary", True)

    dpg.show_viewport()

    CHUNK_SIZE = 2048
    FFT_SIZE = 4096 - 512
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
            ei = i + CHUNK_SIZE
            si = max(ei - FFT_SIZE, 0)
            audio = test_audio[si:ei]
            # left, right = audio, audio
            left, right = make_binaural(audio, az, el, r)
            assert len(left) == len(right)
            left, right = left[-CHUNK_SIZE:], right[-CHUNK_SIZE:]
            player.add_chunk(np.column_stack((left, right)))
            i += CHUNK_SIZE
            dpg.set_value(seek, i)

    player.stop()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
