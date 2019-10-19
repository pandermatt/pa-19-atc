import csv
import os
from collections import defaultdict

import pandas as pd

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
        if row[2] not in text:
            log.info(f'{row[2]} -> {text}')
            error_airline_dict[row[2]] += 1

    with open(output_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['Airline', 'Total', 'Error', 'Error/Total'])
        for airline, total in count_airline_dict.items():
            error = error_airline_dict[airline]
            log.info(f'{airline} -> {error * 1.0 / total}')
            writer.writerow([airline, total, error, error * 1.0 / total])


if __name__ == '__main__':
    file = os.path.join(config.keyword_dir(), 'result_keyword_sorted.csv')
    df_keywords = pd.read_csv(file, sep=",", header=None)

    check_error(df_keywords)
