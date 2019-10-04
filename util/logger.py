"""
Author: Pascal Andermatt and Jennifer Schürch
"""

import logging


def get_logger():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    return logging.getLogger(__name__)


def log_exit(message):
    log.warning(message)
    log.warning("Exiting program with code 1")
    exit(1)


_log = get_logger()
_log.exit = log_exit

log = _log
