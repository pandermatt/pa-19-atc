import matplotlib.pyplot as plt
import numpy as np

# data to plot
n_groups = 4
c_groups = 4

KER = (23.15, 22.12, 22.16, 22.93)
WER = (22.18, 20.64, 20.61, 21.37)
WER_airline_name = (36.85, 31.21, 30.31, 33.32)
WER_flight_number = (32.51, 31.93, 32.72, 32.72)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 1 / (c_groups + 0.5)
opacity = 0.8

# csfont = {'fontname':'CMU Serif'}
# hfont = {'fontname':'CMU Serif'}

plt.title('title',**csfont)
plt.xlabel('xlabel', **hfont)

plt.bar(index, KER, bar_width,
        alpha=opacity,
        label='Keyword Error Rate')
plt.bar(index + bar_width, WER, bar_width,
        alpha=opacity,
        label='Word Error Rate')
plt.bar(index + 2 * bar_width, WER_airline_name, bar_width,
        alpha=opacity,
        label='Word Error Rate bei Airline Name')
plt.bar(index + 3 * bar_width, WER_flight_number, bar_width,
        alpha=opacity,
        label='Word Error Rate bei Flugnummer')

plt.xlabel('Schwellenwerte für die Unscharfe Suche')
plt.ylabel('Error Rate in %')
plt.ylim(10, 50)
plt.title('Auswertung RML mit Unscharfe Suche')
plt.xticks(index + bar_width, ('0.25', '0.5', '0.75', '1'))
plt.legend()

plt.tight_layout()
plt.savefig('result.pdf')
plt.show()
