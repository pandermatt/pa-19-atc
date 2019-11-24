import ast
import os
from os.path import join

import pandas as pd

from config import config
from util.logger import log


def determine_accuracy(suffix=""):
    df = pd.read_csv(join(config.language_understanding_result_csv_dir(), 'result.csv'),
                     sep=";",  # as we use ; instead of ,
                     names=['filename', 'query', 'intent', 'airline_name', 'flight_number', 'flight_level'])
    overall_score = 0
    overall_wer = 0
    overall_wer_intent = 0
    overall_wer_airline_name = 0
    overall_wer_flight_number = 0
    overall_wer_flight_level = 0
    count = 0

    df = df.fillna('')
    for idx, row in df.iterrows():
        path = join(config.language_understanding_result_dir(suffix=suffix),
                    row["filename"].replace('.json', '.txt'))
        if not os.path.exists(path):
            continue

        json_content = open(path, 'r').read()
        content = ast.literal_eval(json_content)

        entities = {entity.get('type'): entity.get('entity') for entity in content.get('entities', [])}
        score = 0
        rating = 0.25

        from word_error_rate.word_error_rate import word_error_rate
        overall_wer += (word_error_rate(row['intent'], content['topScoringIntent']['intent']) +
                        word_error_rate(row['airline_name'], entities.get('airline_name', '')) +
                        word_error_rate(row['flight_number'], entities.get('flight_number', '')) +
                        word_error_rate(row['flight_level'], entities.get('flight_level', ''))) / 4

        overall_wer_intent += word_error_rate(row['intent'], content['topScoringIntent']['intent'])
        overall_wer_airline_name += word_error_rate(row['airline_name'], entities.get('airline_name', ''))
        overall_wer_flight_number += word_error_rate(row['flight_number'], entities.get('flight_number', ''))
        overall_wer_flight_level += word_error_rate(row['flight_level'], entities.get('flight_level', ''))

        if row['intent'].lower() == content['topScoringIntent']['intent'].lower():
            score += rating

        if row['airline_name'].lower() == entities.get('airline_name', '').lower():
            score += rating

        if row['flight_number'].lower() == entities.get('flight_number', '').lower():
            score += rating

        if row['flight_level'].lower() == entities.get('flight_level', '').lower():
            score += rating

        overall_score += score
        count += 1
    log.info(f"Success Rate: {100.0 * overall_score / count}")
    log.info(f"KEYWORD ERROR RATE (KER): {100 - (100.0 * overall_score / count)}")
    log.info(f"WER: {1.0 * overall_wer / count}")
    log.info(f"WER overall_wer_intent: {1.0 * overall_wer_intent / count}")
    log.info(f"WER overall_wer_airline_name: {1.0 * overall_wer_airline_name / count}")
    log.info(f"WER overall_wer_flight_number: {1.0 * overall_wer_flight_number / count}")
    log.info(f"WER overall_wer_flight_level: {1.0 * overall_wer_flight_level / count}")


if __name__ == '__main__':
    folders = ['original',
               'more_keywords_original',
               'more_2x_original',
               'UK_EN_keyword2',
               'more_keywords_UK_EN_keyword2',
               'more_2x_UK-keyword2']
    for folder in folders:
        log.info("Determine Accuracy " + folder)
        determine_accuracy(suffix="_" + folder)
        log.info("------------------------")
