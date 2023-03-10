# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JpFK6xLOvJzmv2V08DscHDmis-NA1xp6
"""

!pip install librosa
import librosa

file_path="/content/Audio Semester Project.wav"
samples,sampling_rate=librosa.load(file_path,sr=None, mono= True,offset=0.0,duration= None)
len(samples),sampling_rate

duration_of_sound=len(samples)/sampling_rate
print(duration_of_sound,"second")

from IPython.display import Audio
Audio(file_path)

import matplotlib.pyplot as plt
from librosa import display
plt.figure()
librosa.display.waveplot(y=samples,sr=sampling_rate)
plt.xlabel("Time (seconds)-->")
plt.ylabel("Amplitude")
plt.show()

import numpy as np
def spectrogram(samples, sample_rate, stride_ms = 10.0, 
                          window_ms = 20.0, max_freq = None, eps = 1e-14):

    stride_size = int(0.001 * sample_rate * stride_ms)
    window_size = int(0.001 * sample_rate * window_ms)

    # Extract strided windows
    truncate_size = (len(samples) - window_size) % stride_size
    samples = samples[:len(samples) - truncate_size]
    nshape = (window_size, (len(samples) - window_size) // stride_size + 1)
    nstrides = (samples.strides[0], samples.strides[0] * stride_size)
    windows = np.lib.stride_tricks.as_strided(samples, 
                                          shape = nshape, strides = nstrides)
    
    assert np.all(windows[:, 1] == samples[stride_size:(stride_size + window_size)])

    # Window weighting, squared Fast Fourier Transform (fft), scaling
    weighting = np.hanning(window_size)[:, None]
    
    fft = np.fft.rfft(windows * weighting, axis=0)
    fft = np.absolute(fft)
    fft = fft**2
    
    scale = np.sum(weighting**2) * sample_rate
    fft[1:-1, :] *= (2.0 / scale)
    fft[(0, -1), :] /= scale
    
    # Prepare fft frequency list
    freqs = float(sample_rate) / window_size * np.arange(fft.shape[0])
    
    # Compute spectrogram feature
    ind = np.where(int(freqs) <= int(max_freq))[0][-1]+1
    specgram = np.log(fft[:ind, :] + eps)
    return specgram

import os
import matplotlib.pyplot as plt

#for loading and visualizing audio files
import librosa
import librosa.display

#to play audio
import IPython.display as ipd

audio_fpath = "/content/drive/MyDrive/SNS project"
audio_clips = os.listdir(audio_fpath)
print("No. of .wav files in audio folder = ",len(audio_clips))

x, sr = librosa.load(audio_fpath+audio_clips[0], sr=44100)

print(type(x), type(sr))
print(x.shape, sr)

