"""
Author: Leandro Kuster and Emanuele Mazzotta
"""

import glob
from os import makedirs
from os.path import exists, join, basename

from config import config
from util.logger import log
from util.text_cleanup import clean_up_text


def clean_text_save_to_file():
    if not exists(config.clean_data_cleaned_text_dir()):
        makedirs(config.clean_data_cleaned_text_dir())
        log.info("Creating Clean Data Cleaned Text Dir")

    for text_file_path in glob.glob(join(config.clean_data_text_dir(), '*.txt')):
        clean_file_path = join(config.clean_data_cleaned_text_dir(),
                               basename(text_file_path))

        if exists(clean_file_path):
            continue

        text = clean_up_text(open(text_file_path).read())
        if not text:
            continue

        open(clean_file_path, 'w+').write(text)
        log.info("File written: %s" % text_file_path)
        log.info("Cleaned Text: %s" % text)


if __name__ == '__main__':
    clean_text_save_to_file()
