import numpy

"""
This code is copied from: https://github.com/zszyellow/WER-in-python/blob/master/wer.py
"""


def word_error_rate(reference, hypothesis):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split())
    """
    if len(reference) == 0:
        return 0 if len(hypothesis) == 0 else 100
    return float(word_distance(reference, hypothesis)[len(reference)][len(hypothesis)]) / len(reference) * 100


def word_distance(reference, hypothesis):
    """
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.
    Main algorithm used is dynamic programming.
    Attributes:
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    """
    d = numpy.zeros((len(reference) + 1) * (len(hypothesis) + 1), dtype=numpy.uint8).reshape(
        (len(reference) + 1, len(hypothesis) + 1)
    )
    for i in range(len(reference) + 1):
        for j in range(len(hypothesis) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    for i in range(1, len(reference) + 1):
        for j in range(1, len(hypothesis) + 1):
            if reference[i - 1] == hypothesis[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitute = d[i - 1][j - 1] + 1
                insert = d[i][j - 1] + 1
                delete = d[i - 1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d
