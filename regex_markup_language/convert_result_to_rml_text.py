import glob
import os
from os.path import exists, basename, join

from config import config
from util.logger import log


def convert_result_to_rml(folder=""):
    file = os.path.join(config.regex_markup_language_dir(), f'rml_input_{folder}.txt')
    i = 0
    while exists(file):
        i += 1
        file = os.path.join(config.regex_markup_language_dir(), f'rml_input_{folder}_({i}).txt')

    log.info(f'Write {file}')
    with open(file, 'w+') as f:
        for text_file in glob.glob(join(config.test_data_cleaned_text_dir(suffix="-" + folder), '*.txt')):
            f.write(f"{basename(text_file)}\t{open(text_file, 'r').read()}\n")
    log.info('Done')


if __name__ == '__main__':
    convert_result_to_rml(folder="UK-keyword2")
