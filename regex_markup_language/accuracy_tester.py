import xml.etree.ElementTree as XML
from os.path import join, basename, exists

from config import config
from language_understanding.accuracy_tester import determine_accuracy
from util.logger import log


def convert_rml_and_determine_accuracy(suffix="", override=False):
    tree = XML.parse(join(config.regex_markup_language_dir(), f'result{suffix}.xml'))
    root = tree.getroot()

    for child in root:
        filename = child.find('filename').text
        result_file_path = join(config.language_understanding_result_dir(suffix='_RML' + suffix),
                                basename(filename))

        if not override and exists(result_file_path):
            log.info(f'already exists... skipping:\t {result_file_path}')
            continue

        data = {'query': '',
                'topScoringIntent': {'intent': child.find('action').text},
                'entities': [
                    {'entity': child.find('airline').text, 'type': 'airline_name'},
                    {'entity': child.find('flightLevel').text, 'type': 'flight_level'},
                    {'entity': child.find('flightnumber').text, 'type': 'flight_number'}]}
        open(result_file_path, 'w+').write(str(data))

        log.info("File written: %s" % result_file_path)

    # Run LUIS Accuracy Check
    determine_accuracy(suffix="_RML" + suffix)


if __name__ == '__main__':
    convert_rml_and_determine_accuracy(override=False)
