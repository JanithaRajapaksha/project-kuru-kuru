import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.signal import butter, filtfilt, iirnotch
from scipy.io import wavfile
import noisereduce as nr

# ==============================
# SETTINGS
# ==============================

input_file = "raw data/20260325_091236.wav"          # your recorded file
output_file = "output/k1.wav"                 # cleaned output file

LOWCUT = 10                      # RPW minimum frequency
HIGHCUT = 2200                    # RPW maximum frequency

# ==============================
# LOAD AUDIO
# ==============================

y, sr = librosa.load(input_file, sr=None)

print("Sampling rate:", sr)
print("Duration:", len(y)/sr, "seconds")

# ==============================
# ORIGINAL SPECTROGRAM
# ==============================

plt.figure(figsize=(10,4))
S = librosa.stft(y)
librosa.display.specshow(librosa.amplitude_to_db(abs(S)),
                         sr=sr,
                         x_axis='time',
                         y_axis='hz')
plt.title("Original Audio Spectrogram")
plt.colorbar()
plt.show()

# ==============================
# REMOVE 50Hz EM HUM
# ==============================

def notch_filter(data, freq, fs, Q=30):
    b, a = iirnotch(freq, Q, fs)
    return filtfilt(b, a, data)

filtered = y

# # remove 50Hz and harmonics
# for f in [50, 100, 150]:
#     filtered = notch_filter(filtered, f, sr)

# ==============================
# BANDPASS FILTER (700-2500Hz)
# ==============================

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

filtered = bandpass_filter(filtered, LOWCUT, HIGHCUT, sr)

# ==============================
# NOISE REDUCTION
# ==============================

clean_audio = nr.reduce_noise(y=filtered, sr=sr)

# ==============================
# SAVE CLEAN AUDIO
# ==============================

wavfile.write(output_file, sr, clean_audio.astype(np.float32))

print("Filtered RPW audio saved as:", output_file)

# ==============================
# CLEANED SPECTROGRAM
# ==============================

plt.figure(figsize=(10,4))
S_clean = librosa.stft(clean_audio)

librosa.display.specshow(librosa.amplitude_to_db(abs(S_clean)),
                         sr=sr,
                         x_axis='time',
                         y_axis='hz')

plt.title("Cleaned Audio Spectrogram (RPW Range)")
plt.colorbar()
plt.show()