"""
Author: Leandro Kuster and Emanuele Mazzotta
"""

from os.path import join, exists

import pylab

from config import config
from util.logger import log


def plot(values):
    h = sorted(values)

    x_max = 100
    y_max = 1401
    x_step = 10
    y_step = 100

    data_interval = range(0, 101, 1)
    x_label_interval = range(0, x_max + 1, x_step)
    y_label_interval = range(0, y_max + 1, y_step)

    x_axis_label = {
        'de': 'Wortfehlerrate pro Transkription',
        'en': 'Word error rate per transcription'
    }

    y_axis_label = {
        'de': 'Anzahl Transkriptionen',
        'en': 'Number of transcriptions'
    }

    title = {
        'microsoft_custom_speech': f'Evaluation Microsoft Custom Speech',
        'microsoft_un_trained': f'Evaluation Microsoft Pre-Built Model',
        'amazon_un_trained': f'Evaluation Amazon Pre-Built Model',
        'google_un_trained': f'Evaluation Google Pre-Built Model',
    }

    pylab.figure(num=None, figsize=(10, 7), dpi=300, facecolor='white', edgecolor='black')
    pylab.rcParams.update({'font.size': 18})
    pylab.hist(x=h, histtype='bar', bins=data_interval, rwidth=0.95)
    pylab.title(title.get(config.provider()))
    pylab.xticks(x_label_interval, [f'{x_label}%' for x_label in x_label_interval])
    pylab.yticks(y_label_interval)
    pylab.xlabel(x_axis_label.get("de"))
    pylab.ylabel(y_axis_label.get("de"))
    pylab.legend([f'n = {len(h)}'], loc='upper right')

    # save figure
    pylab.savefig(join(config.accuracy_dir(), f'result_{config.provider()}.png'))
    pylab.show()


def calculate_accuracy():
    if not exists(config.provider_accuracy_file()):
        log.exit(f'Accuracy file does not exist: {config.provider_accuracy_file()}')

    accuracy_content = open(config.provider_accuracy_file(), 'r+').readlines()
    accuracy_map = {}

    result_distribution = {k: 0 for k in range(0, 101, 20)}

    for accuracy_line in accuracy_content:
        text_name = accuracy_line[:accuracy_line.index('\t')]
        accuracy = float(accuracy_line[accuracy_line.index('\t') + 1:accuracy_line.index('\n')])
        for k in result_distribution.keys():
            if accuracy <= k:
                result_distribution[k] += 1
                break
        accuracy_map[text_name] = accuracy

    log.info(f'Total files tested: {len(accuracy_map)}')
    log.info(result_distribution)
    avg_accuracy = sum(accuracy_map.values()) / len(accuracy_map)
    log.info(f'Average word error rate: {avg_accuracy}')
    return accuracy_map


if __name__ == '__main__':
    plot(calculate_accuracy().values())
