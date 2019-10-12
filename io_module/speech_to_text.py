"""
Author: Leandro Kuster and Emanuele Mazzotta
"""

import glob
from os.path import exists, join, basename

from config import config
from speech.speech_to_text import speech_to_text


def speech_to_text_save_to_file():
    for audio_file_path in glob.glob(join(config.clean_data_audio_dir(), '*.wav')):
        text_file_path = join(config.provider_accuracy_dir(),
                              basename(audio_file_path).replace('.wav', '.txt'))

        if exists(text_file_path):
            continue

        text = speech_to_text(audio_file_path)
        if not text:
            continue

        open(text_file_path, 'w+').write(text)


if __name__ == '__main__':
    speech_to_text_save_to_file()
