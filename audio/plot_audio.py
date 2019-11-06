# import the pyplot and wavfile modules
import os

import matplotlib.pyplot as plot
import numpy as np
from scipy.io import wavfile

from config import config

if __name__ == '__main__':
    # samplingFrequency, signalData = wavfile.read(os.path.join(config.test_data_dir(), "audio_speed-1.3/gf1_01_002_speed-1.3.wav"))
    # samplingFrequency, signalData = wavfile.read(os.path.join(config.test_data_dir(), "audio_speed-1.1-normal/gf1_01_002_speed-1.1-normal.wav"))
    samplingFrequency, signalData = wavfile.read(os.path.join(config.test_data_dir(), "audio_noise-0.03/gf1_01_002_noise-0.03.wav"))
    plot.subplot(211)
    plot.title('Spektogramm einer WAV Datei')
    plot.plot(signalData / np.max(np.abs(signalData)))
    plot.ylim([-1, 1])
    plot.xlabel('Sample')
    plot.ylabel('Amplitude')
    plot.subplot(212)
    plot.specgram(signalData / np.max(np.abs(signalData)), Fs=samplingFrequency)
    plot.xlabel('Zeit')
    plot.ylabel('Frequenz')
    plot.show()
