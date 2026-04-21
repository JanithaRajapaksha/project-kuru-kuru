# Audio Cleaning Script

A Python script that processes audio files to remove noise and filter unwanted frequencies.

## Features

- **Bandpass Filter**: Filters audio to the RPW frequency range (10Hz - 3500Hz)
- **Noise Reduction**: Removes background noise from audio signals
- **Spectrogram Visualization**: Displays before/after spectrograms for comparison
- **WAV Format Support**: Reads and writes standard WAV files

## Requirements

- numpy
- matplotlib
- librosa
- scipy
- noisereduce

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your audio file in the `raw data/` directory
2. Update the `input_file` path in `main.py` to match your file
3. Run: `python main.py`
4. Cleaned audio will be saved to `output/` directory

## Configuration

Edit these settings in `main.py`:
- `LOWCUT`: Minimum frequency (Hz) - default 10
- `HIGHCUT`: Maximum frequency (Hz) - default 2200
- `input_file`: Path to your audio file
- `output_file`: Path for cleaned audio output

## Output

- Cleaned WAV file with filtered and denoised audio
- Comparison spectrograms showing original vs. cleaned audio
