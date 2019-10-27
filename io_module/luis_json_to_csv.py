import csv
import glob
import json
import os
from os.path import basename

from config import config
from util.logger import log


def convert_json_to_csv():
    file = os.path.join(config.language_understanding_dir(), 'result.csv')
    log.info(f'Write {file}')
    with open(file, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Query", "Intent", "Airline Name", "Flight Number", "Fligh Level"])
        for json_file in glob.glob(os.path.join(config.language_understanding_result_json_dir(), '*.json')):
            text = json.loads(open(json_file, 'r').read())
            entities = {entity.get('type'): entity.get('entity') for entity in text.get('entities', [])}
            writer.writerow([basename(json_file), text['query'],
                             text['topScoringIntent']['intent'],
                             entities.get('airline_name', ''),
                             entities.get('flight_number', ''),
                             entities.get('flight_level', '')])
    log.info('Done')


if __name__ == '__main__':
    convert_json_to_csv()
