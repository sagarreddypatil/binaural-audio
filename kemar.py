import os
from pathlib import Path
from functools import cache
from util import read_mono_wav

hrtf_dir = Path("./kemar-full")


@cache
def get_hrtf(el, az):
    elevs = range(-40, 91, 10)
    el = min(elevs, key=lambda x: abs(x - el))
    el = f"{el:02d}"
    if el == "00":
        el = "0"

    eldir = hrtf_dir / f"elev{el}"
    azs = os.listdir(eldir)
    azs = [int(az[2 + len(el) : -5]) for az in azs]
    az = min(azs, key=lambda x: abs(x - az))
    az = f"{az:03d}"

    print("get_hrtf", el, az)

    left_path = eldir / f"L{el}e{az}a.wav"
    right_path = eldir / f"R{el}e{az}a.wav"

    left = read_mono_wav(left_path)
    right = read_mono_wav(right_path)
    assert len(left) == len(right)
    return left, right