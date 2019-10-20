import csv
import glob
import os
from os.path import join, basename

import pandas as pd

from config import config
from util.logger import log

IGNORE = ['As', 'L', 'THREE']


def extract_airline(airlines, airports):
    file = os.path.join(config.keyword_dir(), 'result_keyword.csv')
    with open(file, 'a') as f:
        writer = csv.writer(f)
        for text_path in glob.glob(join(config.original_keyword_dir(), '*.txt')):
            text = open(text_path, "r").read()

            found_airlines = []
            found_airports = []

            for airline in airlines:
                if airline.lower() in text:
                    if airline in IGNORE:
                        continue
                    found_airlines.append(airline)

            for airport in airports:
                if airport.lower() in text:
                    found_airports.append(airport)

            log.info(f'{text_path} -> {str(found_airlines)} -> {str(found_airports)} ')
            first_airline = ''
            if len(found_airlines) != 0:
                first_airline = found_airlines[0]

            first_airport = ''
            if len(found_airports) != 0:
                first_airport = found_airports[0]

            writer.writerow([basename(text_path), text,
                             first_airline, str(found_airlines),
                             first_airport, str(found_airports)])


if __name__ == '__main__':
    df_airlines = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat',
                              sep=",",
                              header=None)
    airlines = []
    for idx, row in df_airlines.iterrows():
        airlines.append(row[1])

    df_airports = pd.read_csv(
        'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat',
        sep=",",
        header=None)
    airports = []
    for idx, row in df_airports.iterrows():
        airports.append(row[1])
        airports.append(str(row[2]))
        airports.append(str(row[3]))

    extract_airline(airlines, airports)
