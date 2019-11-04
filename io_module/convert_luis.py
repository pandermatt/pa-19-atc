import glob
from os.path import exists, basename, join

from config import config
from language_understanding.recognition_to_text import analyse_text
from util.logger import log


def language_recognition_save_to_file():
    for clean_file_path in glob.glob(join(config.test_data_cleaned_text_dir(), '*.txt')):
        result_file_path = join(config.language_understanding_result_dir(),
                                basename(clean_file_path))

        if exists(result_file_path):
            log.info(f'already exists... skipping:\t {result_file_path}')
            continue

        content = open(clean_file_path).read()
        long, short = analyse_text(content)

        if long.get('error'):
            log.warning(f'error occurred... skipping:\t {result_file_path}')
            continue

        long = str(long)
        short = str(short)

        open(result_file_path, 'w+').write(long)
        open(join(config.language_understanding_dir(), 'result.txt'), 'a').write(long + '\n')

        log.info("File written: %s" % result_file_path)
        log.info("Cleaned Text: %s" % short)


if __name__ == '__main__':
    language_recognition_save_to_file()
