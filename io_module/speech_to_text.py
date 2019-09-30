import glob
from os import makedirs
from os.path import exists, join, basename

from util.config import config
from util.logger import log
from speech.speech_to_text import speech_to_text


def speech_to_text_save_to_file():
    if not exists(config.provider_accuracy_dir()):
        makedirs(config.provider_accuracy_dir())
        log.info("Creating Provider Accuracy Dir")

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
