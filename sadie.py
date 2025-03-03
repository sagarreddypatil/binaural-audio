import os
import re
from pathlib import Path
from functools import cache
from util import read_stereo_wav

hrtf_dir = Path("./data/sadie-d1/D1_HRIR_WAV/44K_16bit/")

pat = re.compile(r"azi_(-?\d+),(\d+)_ele_(-?\d+),(\d+)\.wav")
azels = []
for file in os.listdir(hrtf_dir):
    match = pat.match(file)
    assert match is not None
    azi, azi_frac, ele, ele_frac = match.groups()
    az = float(f"{azi}.{azi_frac}")
    el = float(f"{ele}.{ele_frac}")
    azels.append((az, el, file))


@cache
def get_hrtf(az, el):
    azel = min(azels, key=lambda x: abs(x[0] - az) + abs(x[1] - el))
    az, el, fn = azel
    path = hrtf_dir / fn

    audio = read_stereo_wav(path)
    left, right = audio[:, 0], audio[:, 1]
    return left, right


# get_hrtf(32.5, 105)
