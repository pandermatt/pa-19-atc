import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# data to plot
n_groups = 6
c_groups = 8

no_noise = (616, 670, 420, 151, 39, 22)
noise_001 = (428, 646, 511, 201, 62, 75)
noise_002 = (281, 517, 523, 304, 146, 162)
noise_003 = (174, 340, 521, 346, 218, 334)
noise_005 = (64, 163, 278, 320, 320, 788)
noise_007 = (27, 65,  176, 228, 274, 1163)
noise_009 = (13, 25,  96,  151, 228, 1420)
noise_01 = (8, 22, 55, 118, 181, 1549)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 1 / (c_groups + 0.5)
opacity = 0.8

csfont = {'fontname':'CMU Serif'}
hfont = {'fontname':'CMU Serif'}


plt.title('title',**csfont)
plt.xlabel('xlabel', **hfont)

plt.rc('axes', titlesize=14)

plt.bar(index, no_noise, bar_width,
        alpha=opacity,
        color='#1b1b1b',
        label='Original')
plt.bar(index + bar_width, noise_001, bar_width,
        alpha=opacity,
        label='1% Rauschen')
plt.bar(index + 2 * bar_width, noise_002, bar_width,
        alpha=opacity,
        label='2% Rauschen')
plt.bar(index + 3 * bar_width, noise_003, bar_width,
        alpha=opacity,
        label='3% Rauschen')
plt.bar(index + 4 * bar_width, noise_005, bar_width,
        alpha=opacity,
        label='5% Rauschen')
plt.bar(index + 5 * bar_width, noise_007, bar_width,
        alpha=opacity,
        color='#9467bd',
        label='7% Rauschen')
plt.bar(index + 6 * bar_width, noise_009, bar_width,
        alpha=opacity,
        color='#60342b',
        label='9% Rauschen')
plt.bar(index + 7 * bar_width, noise_01, bar_width,
        alpha=opacity,
        color='#7f7f7f',
        label='10% Rauschen')

plt.xlabel('Word Error Rate (WER) Bereiche')
plt.ylabel('Anzahl Transkriptionen')
plt.ylim(0, 1600)
plt.title('Auswertung Microsoft Custom Speech\nEvaluierung mit verrauschten Testdaten')
plt.xticks(index + 3.5*bar_width, ('0%', '>0-20%', '>20-40%', '>40-60%', '>60-80%', '>80-100%',))
plt.setp(ax.get_xticklabels(), ha="right", rotation=35)
plt.legend()

plt.tight_layout()
plt.savefig('result.pdf')
plt.show()


totalTranscripts = 1933
noiselevels = [1, 2, 3, 5, 7, 9, 10]
avgWER = [23.128842489240252,
        32.1401864800706,
        41.53296107707792,
        57.08195216036499,
        67.10299121043565,
        74.64824081791056,
        80.02933022532598]
nonEmptyTranscripts = [1918, 1891, 1810, 1535, 1233, 1001, 915]
for i in range(len(noiselevels)):
        wer = (avgWER[i] * nonEmptyTranscripts[i]
           + 100 * (totalTranscripts-nonEmptyTranscripts[i])) / totalTranscripts
        print("%d Rauschen & %f" % (noiselevels[i], wer))