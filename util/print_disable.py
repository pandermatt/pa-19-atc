"""
Based on code take from Bachelors Thesis by Leandro Kuster and Emanuele Mazzotta
Author: Pascal Andermatt and Jennifer Schürch
"""

import os
import sys


class PrintDisabled:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
