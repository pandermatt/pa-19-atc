#!/usr/bin/env python3
# coding=utf-8

import glob
from os import makedirs
from os.path import join, exists, basename

from config import Config

from speech.microsoft.microsoft_speech2text import transcribe_microsoft_custom_speech


def speech_to_text():
    if not exists(Config.accuracy_dir()):
        makedirs(Config.accuracy_dir())
    if not exists(Config.provider_accuracy_dir()):
        makedirs(Config.provider_accuracy_dir())

    for audio_file_path in glob.glob(join(Config.clean_data_audio_dir(), '*.wav')):
        text_file_path = join(Config.provider_accuracy_dir(),
                              basename(audio_file_path).replace('.wav', '.txt'))

        if exists(text_file_path):
            continue

        text = transcribe_microsoft_custom_speech(audio_file_path)
        if not text:
            continue

        open(text_file_path, 'w+').write(text)


TRANSCRIPTION_FUNCTION_MAP = {
    'microsoft_custom_speech': transcribe_microsoft_custom_speech
}

if __name__ == '__main__':
    speech_to_text()
