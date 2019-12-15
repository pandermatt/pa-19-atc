"""
Author: Leandro Kuster and Emanuele Mazzotta
"""

from os.path import join, exists

import pylab

from config import config
from util.logger import log

import speech.accuracy_tester as acc_tester


def plot(values, prefix='', title_suffix=''):
    h = sorted(values)

    x_max = 100
    y_max = 700
    x_step = 10
    y_step = 100

    data_interval = range(0, 101, 1)
    x_label_interval = range(0, x_max + 1, x_step)
    y_label_interval = range(0, y_max + 1, y_step)

    x_axis_label = {
        'de': 'Word Error Rate (WER) pro Transkription',
        'en': 'Word error rate per transcription'
    }

    y_axis_label = {
        'de': 'Anzahl Transkriptionen',
        'en': 'Number of transcriptions'
    }

    title = {
        'microsoft_custom_speech': f'Auswertung Microsoft Custom Speech'+title_suffix,
    }

    pylab.figure(num=None, figsize=(10, 7), dpi=300, facecolor='white', edgecolor='black')
    pylab.figure(num=None, figsize=(10, 6), dpi=300, facecolor='white', edgecolor='black')
    pylab.rcParams.update({'font.size': 18})
    pylab.hist(x=h, histtype='bar', bins=data_interval, rwidth=0.95)
    pylab.title(title.get(config.provider()))
    pylab.xticks(x_label_interval, [f'{x_label}%' for x_label in x_label_interval])
    pylab.yticks(y_label_interval)
    pylab.xlabel(x_axis_label.get("de"))
    pylab.ylabel(y_axis_label.get("de"))
    pylab.legend([f'n = {len(h)}'], loc='upper right')

    # save figure
    pylab.savefig(join(config.accuracy_dir(), f'{config.provider(prefix)}_result.png'))
    pylab.show()


def calculate_accuracy(prefix=''):
    if not exists(config.provider_accuracy_file(prefix)):
        log.exit(f'Accuracy file does not exist: {config.provider_accuracy_file(prefix)}')

    accuracy_content = open(config.provider_accuracy_file(prefix), 'r+').readlines()
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
    try:
        f = open(config.provider_accuracy_average_file(prefix), "w")
    except IOError:
        print("Cannot open file " + config.provider_accuracy_average_file(prefix))
    else:
        with f:
            data = f'Total files tested: {len(accuracy_map)}\n{result_distribution}\nAverage word error rate: {avg_accuracy}'
            f.write(data)

    printWERThreshold(accuracy_map);

    return accuracy_map

def printWERThreshold(accuracy_map):
    h = sorted(accuracy_map.values())
    log.info("\nWER (%)"
        + "\n0        %d" % (len([x for x in h if x == 0]))
        + "\n>0-20    %d" % (len([x for x in h if x > 0 and x <= 20]))
        + "\n>20-40   %d" % (len([x for x in h if x > 20 and x <= 40]))
        + "\n>40-60   %d" % (len([x for x in h if x > 40 and x <= 60]))
        + "\n>60-80   %d" % (len([x for x in h if x > 60 and x <= 80]))
        + "\n>80-100  %d" % (len([x for x in h if x > 80 and x <= 100]))
        + "\n>80      %d" % (len([x for x in h if x > 80])))

if __name__ == '__main__':
    cleanup = True
    outputprefix = ''
    if cleanup:
        outputprefix = 'cleanup_'
    for trans in acc_tester.transcripts:
        prefix = outputprefix + trans["prefix"]
        log.info(prefix)
        plot(calculate_accuracy(prefix).values(), prefix, trans['title_suffix'])
