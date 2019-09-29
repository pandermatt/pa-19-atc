import glob
from os import makedirs
from os.path import join, exists, basename

from config import config
from logger import log
from speech.microsoft.microsoft_speech2text import transcribe_microsoft_custom_speech
from text_analysis.keyword_extraction.verbal_expressions import keyword_extraction


def speech_to_text():
    if not exists(config.provider_accuracy_dir()):
        makedirs(config.provider_accuracy_dir())
        log.info("Creating Provider Accuracy Dir")

    for audio_file_path in glob.glob(join(config.clean_data_audio_dir(), '*.wav')):
        text_file_path = join(config.provider_accuracy_dir(),
                              basename(audio_file_path).replace('.wav', '.txt'))

        if exists(text_file_path):
            continue

        text = transcribe_microsoft_custom_speech(audio_file_path)
        if not text:
            continue

        open(text_file_path, 'w+').write(text)
        keyword_extraction(text)
