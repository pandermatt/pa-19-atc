from os.path import join, basename, exists
from xml.etree import ElementTree as XML

from config import config
from util.logger import log


def _find_or_default(child, param):
    attr = child.find(param)
    if attr is not None:
        return attr.text
    return None


def convert_rml(out_folder, suffix="", override=False):
    tree = XML.parse(join(config.regex_markup_language_dir(), f'result{suffix}.xml'))
    root = tree.getroot()

    for child in root:
        filename = _find_or_default(child, 'filename')
        if filename is None:
            continue

        result_file_path = join(out_folder, basename(filename))

        if not override and exists(result_file_path):
            continue

        entity = []
        airline = _find_or_default(child, 'airline')
        flight_level = _find_or_default(child, 'flightLevelNumber')
        flight_number = _find_or_default(child, 'flightnumber')
        intent = _find_or_default(child, 'action')

        if airline is not None:
            entity.append({'entity': airline, 'type': 'airline_name'})

        if flight_level is not None:
            entity.append({'entity': flight_level, 'type': 'flight_level'})

        if flight_number is not None:
            entity.append({'entity': flight_number, 'type': 'flight_number'})

        if intent in ['climb to', 'climb']:
            intent = 'FlightClimb'

        if intent in ['descend']:
            intent = 'FlightDescend'

        if intent in ['maintain']:
            intent = 'FlightMaintain'

        data = {'query': '',
                'topScoringIntent': {'intent': intent if intent is not None else "None"},
                'entities': entity}
        open(result_file_path, 'w+').write(str(data))

        log.info("File written: %s" % result_file_path)
