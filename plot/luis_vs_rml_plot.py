import matplotlib.pyplot as plt
import numpy as np

# data to plot
n_groups = 6
c_groups = 2

RML = (22.12, 20.64, 9.13, 31.21, 31.93, 10.29)
LUIS = (19.86, 17.38, 4.52, 36.17, 23.84, 4.98)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 1 / (c_groups + 0.5)
opacity = 0.8

plt.bar(index, LUIS, bar_width,
        alpha=opacity,
        label='LUIS')
plt.bar(index + bar_width, RML, bar_width,
        alpha=opacity,
        label='RML')

# plt.xlabel('Schwellenwerte für die Unscharfe Suche')
plt.ylabel('Error Rate in %')
# plt.ylim(0, 355)
plt.title('Vergleich LUIS und RML')
plt.xticks(index - 0.2 + bar_width, ('KER', 'WER',
                                     'WER bei Intents',
                                     'WER bei Airline Name',
                                     'WER bei Flugnummer',
                                     'WER bei Fluglevel'))
plt.legend()
plt.setp(ax.get_xticklabels(), ha="right", rotation=20)


plt.tight_layout()
plt.savefig('result.pdf')
plt.show()
