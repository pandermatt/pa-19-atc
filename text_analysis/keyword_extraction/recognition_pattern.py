from verbalexpressions import VerEx

from text_analysis.keyword_extraction.rml import RML


def create_recognition_pattern():
    greeting = VerEx() \
        .maybe('good morning') \
        .maybe('good evening') \
        .maybe('good day') \
        .maybe('hello') \
        .maybe('bonjour')

    airline = VerEx() \
        .add(r'([A-Za-z]+)') \
        .add(r'(\s[A-Za-z]+)?')

    flight_number = VerEx() \
        .add(r'(\d){3,4}')

    action = VerEx() \
        .find('descend') \
        .OR('climb') \
        .OR('set') \
        .OR('report')

    flight_level = VerEx() \
        .add(r'(?P<flight_level>(?<=flight level )(\d){3,4})')

    atc_pattern = RML() \
        .start_of_line() \
        .maybe('greeting', greeting) \
        .maybe_anything() \
        .maybe('airline', airline) \
        .maybe_anything() \
        .maybe('flight_number', flight_number) \
        .maybe_anything() \
        .maybe('action', action) \
        .maybe_anything() \
        .add(flight_level.source()) \
        .maybe_anything()

    return atc_pattern
