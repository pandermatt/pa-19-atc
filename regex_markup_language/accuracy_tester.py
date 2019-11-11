import xml.etree.ElementTree as XML
from os.path import join, basename, exists

from config import config
from language_understanding.accuracy_tester import determine_accuracy
from util.logger import log


def find_or_default(child, param):
    attr = child.find(param)
    if attr is not None:
        return attr.text
    return None


def convert_rml_and_determine_accuracy(suffix="", override=False):
    tree = XML.parse(join(config.regex_markup_language_dir(), f'result{suffix}.xml'))
    root = tree.getroot()

    for child in root:
        filename = find_or_default(child, 'filename')
        if filename is None:
            continue

        result_file_path = join(config.language_understanding_result_dir(suffix='_RML' + suffix),
                                basename(filename))

        if not override and exists(result_file_path):
            log.info(f'already exists... skipping:\t {result_file_path}')
            continue

        entity = []
        airline = find_or_default(child, 'airline')
        flight_level = find_or_default(child, 'flightLevel')
        flight_number = find_or_default(child, 'flightnumber')
        intent = find_or_default(child, 'action')

        if airline is not None:
            entity.append({'entity': airline, 'type': 'airline_name'})

        if flight_level is not None:
            entity.append({'entity': flight_level, 'type': 'airline_name'})

        if flight_number is not None:
            entity.append({'entity': flight_number, 'type': 'airline_name'})

        if intent in ['climb to', 'climb']:
            intent = 'FlightClimb'

        if intent in ['descend']:
            intent = 'FlightDescend'

        if intent in ['maintain']:
            intent = 'FlightMaintain'

        data = {'query': '',
                'topScoringIntent': {'intent': intent},
                'entities': entity}
        open(result_file_path, 'w+').write(str(data))

        log.info("File written: %s" % result_file_path)

    # Run LUIS Accuracy Check
    determine_accuracy(suffix="_RML" + suffix)


if __name__ == '__main__':
    convert_rml_and_determine_accuracy(override=True)
