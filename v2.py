import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.signal import butter, filtfilt, iirnotch
from scipy.io import wavfile
import noisereduce as nr
import os
import tkinter as tk
from tkinter import filedialog

# ==============================
# SETTINGS
# ==============================

LOWCUT = 10
HIGHCUT = 2500

# ==============================
# FOLDER PICKERS
# ==============================

def select_input_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Input Folder (WAV files)")

def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Output Folder")

input_folder = select_input_folder()
output_folder = select_output_folder()

if not input_folder or not output_folder:
    print("Folder selection cancelled.")
    exit()

# ==============================
# FILTER FUNCTIONS
# ==============================

def notch_filter(data, freq, fs, Q=30):
    b, a = iirnotch(freq, Q, fs)
    return filtfilt(b, a, data)

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# ==============================
# PROCESS EACH FILE
# ==============================

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".wav"):
        input_path = os.path.join(input_folder, filename)

        print(f"\nProcessing: {filename}")

        # Load audio
        y, sr = librosa.load(input_path, sr=None)

        # ==============================
        # REMOVE 50Hz HUM
        # ==============================
        filtered = y
        for f in [50, 100, 150]:
            filtered = notch_filter(filtered, f, sr)

        # ==============================
        # BANDPASS FILTER
        # ==============================
        filtered = bandpass_filter(filtered, LOWCUT, HIGHCUT, sr)

        # ==============================
        # NOISE REDUCTION
        # ==============================
        clean_audio = nr.reduce_noise(y=filtered, sr=sr)

        # ==============================
        # OUTPUT FILE NAME
        # ==============================
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_cleaned.wav"
        output_path = os.path.join(output_folder, output_filename)

        # ==============================
        # SAVE FILE
        # ==============================
        wavfile.write(output_path, sr, clean_audio.astype(np.float32))

        print(f"Saved: {output_filename}")

print("\n✅ All files processed successfully.")