import ast
import os
from os.path import join

import pandas as pd

from config import config
from util.logger import log


def determine_accuracy():
    df = pd.read_csv(join(config.language_understanding_result_csv_dir(), 'result.csv'),
                     sep=";",  # as we use ; instead of ,
                     names=['filename', 'query', 'intent', 'airline_name', 'flight_number', 'flight_level'])
    overall_score = 0
    count = 0

    df = df.fillna('')
    for idx, row in df.iterrows():
        path = join(config.language_understanding_result_dir(suffix='_UK_EN_keyword2'),
                    row["filename"].replace('.json', '.txt'))
        if not os.path.exists(path):
            continue

        json_content = open(path, 'r').read()
        content = ast.literal_eval(json_content)

        entities = {entity.get('type'): entity.get('entity') for entity in content.get('entities', [])}
        score = 0
        rating = 0.25

        if row['intent'] == content['topScoringIntent']['intent']:
            score += rating
        else:
            log.info(f"Intend: \t\t {str(row['intent'])} --> {content['topScoringIntent']['intent']}")

        if row['airline_name'] == entities.get('airline_name', ''):
            score += rating
        else:
            log.info(f"Airline Name: \t {str(row['airline_name'])} --> {entities.get('airline_name', '')}")

        if row['flight_number'] == entities.get('flight_number', ''):
            score += rating
        else:
            log.info(f"Flight No.: \t {str(row['flight_number'])} --> {entities.get('flight_number', '')}")

        if row['flight_level'] == entities.get('flight_level', ''):
            score += rating
        else:
            log.info(f"Flight Level.:  {str(row['flight_level'])} --> {entities.get('flight_level', '')}")

        overall_score += score
        count += 1
    log.info(f"Success Rate: {1.0 * overall_score / count}")


if __name__ == '__main__':
    determine_accuracy()
