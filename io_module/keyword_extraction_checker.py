import csv
import os
from collections import defaultdict
from shutil import copyfile

import pandas as pd
from pydub import AudioSegment
from pydub.silence import split_on_silence

from config import config
from util.logger import log


def check_error(df_keywords):
    error_airline_dict = defaultdict(int)
    count_airline_dict = defaultdict(int)
    output_file = os.path.join(config.keyword_dir(), 'result_keyword_error_rate.csv')

    if os.path.exists(output_file):
        log.info(f'already exists... {output_file}')
        return

    for index, row in df_keywords.iterrows():
        if pd.isnull(row[2]):
            continue

        compare_file = os.path.join(config.compare_keyword_dir(), row[0])
        text = open(compare_file, "r").read()

        count_airline_dict[row[2]] += 1
        if row[2].lower() not in text.lower():
            log.info(f'{row[2]} -> {text}')
            error_airline_dict[row[2]] += 1

    with open(output_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['Airline', 'Total', 'Error', 'Error/Total'])
        for airline, total in count_airline_dict.items():
            error = error_airline_dict[airline]
            log.info(f'{airline} -> {error * 1.0 / total}')
            writer.writerow([airline, total, error, error * 1.0 / total])


def prepare_audio(df_keywords):
    airline_to_prepare = ['Airfrans', 'Swissair', 'Speedbird', 'Hapag Lloyd', 'Tarom']
    output_file = os.path.join(config.keyword_dir(), 'Trans.txt')
    count_airline_dict = defaultdict(int)

    if os.path.exists(output_file):
        log.info(f'already exists... {output_file}')
        return

    for index, row in df_keywords.iterrows():
        if pd.isnull(row[2]):
            continue

        if row[2] not in airline_to_prepare:
            continue

        count_airline_dict[row[2]] += 1
        if count_airline_dict[row[2]] > 5:
            continue

        audio_file = os.path.basename(row[0]).replace('.txt', '.wav')

        copyfile(os.path.join(config.clean_data_audio_dir(), audio_file),
                 os.path.join(config.audio_keyword_dir(), audio_file))
        with open(output_file, "a") as file:
            file.write(f'{row[0]}\t{row[2]}\n')

        sound_file = AudioSegment.from_wav(os.path.join(config.clean_data_audio_dir(), audio_file))
        audio_chunks = split_on_silence(sound_file,
                                        # must be silent for at least half a second
                                        min_silence_len=250,
                                        # consider it silent if quieter than -16 dBFS
                                        silence_thresh=-30
                                        )
        for i, chunk in enumerate(audio_chunks):
            out_file = f'{audio_file}chunk{i}.wav'
            out_path = os.path.join(config.audio_keyword_dir(), out_file)
            chunk.export(out_path, format="wav")


if __name__ == '__main__':
    file = os.path.join(config.keyword_dir(), 'result_keyword_sorted.csv')
    df_keywords = pd.read_csv(file, sep=",", header=None)

    check_error(df_keywords)
    prepare_audio(df_keywords)
