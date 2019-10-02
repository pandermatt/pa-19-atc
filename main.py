"""
Author: Pascal Andermatt and Jennifer Schürch
"""

import glob
from os.path import join

from config import config
from language_recognition.recognition_to_text import analyse_text
from speech.speech_to_text import speech_to_text
from text_analysis.text_cleanup import clean_up_text
from util.logger import log


def main():
    for audio_file_path in glob.glob(join(config.clean_data_audio_dir(), '*.wav')):
        spoken_text = speech_to_text(audio_file_path)
        clean_text = clean_up_text(spoken_text)
        flight_data = analyse_text(clean_text)
        log.info(flight_data)


if __name__ == '__main__':
    main()
