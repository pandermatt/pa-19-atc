"""
Author: Leandro Kuster and Emanuele Mazzotta
"""

import glob
import re
from os.path import join, exists, basename

import jiwer

from config import config
from util.logger import log
from word_error_rate.word_error_rate import word_error_rate

REPLACE_MAP = {
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    'ok': 'okay',
    'good bye': 'goodbye'
}

STOP_WORDS = ['', 'ah']


def determine_accuracy():
    if not exists(config.provider_accuracy_dir()):
        log.exit(f'Provider data does not exist: {config.provider_accuracy_dir()}')

    accuracy_info = []
    log.info(f'Determining accuracy for {config.provider()}...')

    custom_files = glob.glob(join(config.provider_accuracy_dir(), '*.txt'))
    i = 0
    for custom_text_file_path in custom_files:
        if i % 1000 == 0:
            log.info(f'{i}/{len(custom_files)}')
        i += 1
        original_text_file_path = join(config.clean_data_text_dir(), basename(custom_text_file_path))

        original_words = extract_clean_words(open(original_text_file_path, 'r').read())
        custom_words = extract_clean_words(open(custom_text_file_path, 'r').read())

        accuracy_info.append(f'{basename(custom_text_file_path)}\t{word_error_rate(original_words, custom_words)}')
        log.info(f'{basename(custom_text_file_path)}\t{jiwer.wer(original_words, custom_words, standardize=True)}')
    return accuracy_info


def build_accuracy(accuracy_line):
    separator_index = accuracy_line.index('\t')
    eol_index = accuracy_line.index('\n')
    return f'' \
           f'{accuracy_line[:separator_index]}' \
           f'\t' \
           f'{accuracy_line[separator_index + 1:eol_index]}'


def load_accuracy_info(accuracy_file_path):
    return [
        build_accuracy(line)
        for line
        in open(accuracy_file_path, 'r+').readlines()
    ]


def extract_clean_words(text):
    text = text.lower()

    for k, v in REPLACE_MAP.items():
        text = text.replace(k, f' {v} ')

    # Remove non alphanumeric-or-space characters
    text = re.sub(r'[^\w\s]+', '', text)

    # Multiple spaces to one
    text = re.sub(r'\s+', ' ', text)

    text = text.strip()

    return [word for word in text.split(' ') if word not in STOP_WORDS]


# Meant for Demo purposes
def find_5_results_per_percentage_step():
    accuracy_file_path = join(config.accuracy_dir(), f'{config.provider()}_accuracy.txt')
    accuracy_info = load_accuracy_info(accuracy_file_path)

    interesting_results = {}

    log.info("Looking for some test data results...")

    for line in accuracy_info:
        file_name = line[:line.index('\t')]
        result = float(line[line.index('\t') + 1:].replace('\n', ''))

        original_text_file_path = join(config.clean_data_text_dir(), file_name)
        custom_text_file_path = join(config.provider_accuracy_dir(), file_name)

        original_words = extract_clean_words(open(original_text_file_path, 'r').read())
        custom_words = extract_clean_words(open(custom_text_file_path, 'r').read())

        for error_rate in range(0, 101, 5):
            if result == error_rate and len([x for x in interesting_results.values() if x == result]) < 5:
                interesting_results.update({f'{" ".join(original_words)}\n{" ".join(custom_words)}': result})

    for k, v in sorted(interesting_results.items(), key=lambda x: x[1]):
        log.info(f'{v}% word error rate:\n{k}\n')


def write_to_accuracy_file(accuracy_info):
    accuracy_file_path = join(config.accuracy_dir(), f'{config.provider()}_accuracy.txt')
    open(accuracy_file_path, 'w+').writelines('\n'.join(accuracy_info))
    open(accuracy_file_path, 'a+').write('\n')


if __name__ == '__main__':
    write_to_accuracy_file(determine_accuracy())
