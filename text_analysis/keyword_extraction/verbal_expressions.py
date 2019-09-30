from logger import log
from text_analysis.keyword_extraction.recognition_pattern import create_recognition_pattern
from text_analysis.keyword_extraction.text_cleanup import apply_replace_map


def keyword_extraction(text):
    replaced_text = apply_replace_map(text)
    log.info("Replaced Transcript: %s" % replaced_text)
    atc_pattern = create_recognition_pattern()

    match_result = atc_pattern.match(replaced_text)
    if match_result:
        for k, v in match_result.groupdict().items():
            log.info(f'{k}: {v}')
    else:
        log.warning("No Match")


if __name__ == '__main__':
    keyword_extraction("Swiss 660 Romeo contact Marseille want to 5 decimal 85 goodbye")
    keyword_extraction("bonjour topswiss four five seven eight climb to flight level three one zero")
