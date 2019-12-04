from config import config
from language_understanding.accuracy_tester import determine_accuracy
from regex_markup_language.convert_rml import convert_rml
from util.logger import log


def convert_rml_and_determine_accuracy(suffix="", override=False):
    log.info(suffix)
    convert_rml(config.language_understanding_result_dir(suffix='_RML' + suffix),
                suffix=suffix,
                override=override)

    # Run LUIS Accuracy Check
    determine_accuracy(suffix="_RML" + suffix)


if __name__ == '__main__':
    # convert_rml_and_determine_accuracy(override=False, suffix="_UK-keyword2")
    convert_rml_and_determine_accuracy(override=False, suffix="_UK-keyword2-Fuzzy0.25")
    convert_rml_and_determine_accuracy(override=False, suffix="_UK-keyword2-Fuzzy0.5")
    convert_rml_and_determine_accuracy(override=False, suffix="_UK-keyword2-Fuzzy0.75")
    convert_rml_and_determine_accuracy(override=False, suffix="_UK-keyword2-Fuzzy1")
