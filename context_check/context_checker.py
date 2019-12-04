import ast
import glob
import json
from os.path import join, basename

from config import config
from regex_markup_language.convert_rml import convert_rml
from util.logger import log

FILES_IN_CONTEXT = [
    'gf1_01_031.txt',
    'gf1_01_144.txt',
    'gm1_01_008.txt',
    'gm1_02_004.txt',
    'gm1_02_023.txt',
    'gm1_02_133.txt',
    'gm2_01_047.txt',
    'gm2_01_060.txt',
    'gm2_02_022.txt',
    'gm2_02_142.txt',
    'sm1_01_004.txt',
    'sm1_01_061.txt',
    'sm1_01_113.txt',
    'sm1_01_126.txt',
    'sm1_01_161.txt'
]

FILES_NOT_IN_CONTEXT = [
    'zf3_02_152.txt',
    'zf1_06_081.txt',
    'zf3_02_131.txt',
    'gm2_02_021.txt',
    'gf1_01_005.txt'
]

FILES_TO_CHECK = FILES_IN_CONTEXT + FILES_NOT_IN_CONTEXT

CONTEXT_DIR = config.context_dir()
SCENARIO = 'szenario.json'


def check_context_for(is_rml=False, suffix=""):
    log.info(suffix)
    if is_rml:
        context_dir = config.language_understanding_result_dir(suffix='_RML' + suffix)
        convert_rml(context_dir, suffix=suffix, override=False)
    else:
        context_dir = config.language_understanding_result_dir(suffix)

    total_correct_recognised = 0

    for file_path in glob.glob(join(context_dir, '*.txt')):
        if basename(file_path) not in FILES_TO_CHECK:
            continue
        json_content = open(file_path, 'r').read()
        content = ast.literal_eval(json_content)

        entities = {entity.get('type'): entity.get('entity') for entity in content.get('entities', [])}

        context = json.loads(open(join(CONTEXT_DIR, SCENARIO), 'r').read())
        in_context = False
        for flight in context['current_flights']:
            if flight['airline'] == entities.get('airline_name', '') \
                    and str(flight['flight_number']) == entities.get('flight_number', ''):
                if basename(file_path) in FILES_IN_CONTEXT:
                    total_correct_recognised += 1
                in_context = True
                continue

        if not in_context:
            if basename(file_path) in FILES_NOT_IN_CONTEXT:
                total_correct_recognised += 1
            else:
                print(entities)

    log.info(f"Recognised {total_correct_recognised} of total {len(FILES_TO_CHECK)}")
    log.info(f"Error rate: {1 - total_correct_recognised / len(FILES_TO_CHECK)}%")


if __name__ == '__main__':
    # check_context_for(is_rml=True)
    check_context_for(is_rml=True, suffix='_UK-keyword2-Fuzzy0.5-context')
    check_context_for(is_rml=True, suffix='_UK-keyword2-Fuzzy0.5-context-with-flight-nr')
    # check_context_for(is_rml=False, suffix='_more_2x_UK-keyword2')
