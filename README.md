# Binaural Audio

## Screenshot

![](images/screen.png)

## Description

A simple Python script to generate binaural audio using Scipy's `fftconvolve` and
HRTFs from the [SADIE database](https://www.york.ac.uk/sadie-project/database.html)

## Dependencies

[uv package manager](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

portaudio (pyaudio doesn't install without it)
```bash
brew install portaudio # macOS
sudo apt install python3-pyaudio # Debian-based
# no need to install portaudio on Windows
```

## Usage

```bash
./download.sh # download HRTFs, saved to data/
uv run main.py /path/to/file.mp3 # doesn't have to be mp3, any audio format works
```
