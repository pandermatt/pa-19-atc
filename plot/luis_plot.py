import matplotlib.pyplot as plt
import numpy as np

# data to plot
n_groups = 3
c_groups = 6
# Original Data
# KER = (23.77, 11.48, 8.35)
# WER = (53.64, 15.21, 8.92)
# WER_intent = (186.20, 26.20, 5.52)
# WER_airline_name = (16.97, 19.52, 14.14)
# WER_flight_number = (9.70, 13.29, 14.18)
# WER_flight_level = (1.70, 1.84, 1.84)

# UK EN
KER = (42.27, 24.76, 19.86)
WER = (70.89, 26.34, 17.38)
WER_intent = (195.68, 30.73, 4.52)
WER_airline_name = (45.32, 40.00, 36.17)
WER_flight_number = (37.70, 29.64, 23.84)
WER_flight_level = (4.84, 4.98, 4.98)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 1 / (c_groups + 0.5)
opacity = 0.8

plt.bar(index, KER, bar_width,
        alpha=opacity,
        label='Keyword Error Rate')
plt.bar(index + bar_width, WER, bar_width,
        alpha=opacity,
        label='Word Error Rate')
plt.bar(index + 2 * bar_width, WER_intent, bar_width,
        alpha=opacity,
        label='Word Error Rate bei Intents')
plt.bar(index + 3 * bar_width, WER_airline_name, bar_width,
        alpha=opacity,
        label='Word Error Rate bei Airline Name')
plt.bar(index + 4 * bar_width, WER_flight_number, bar_width,
        alpha=opacity,
        label='Word Error Rate bei Flugnummer')
plt.bar(index + 5 * bar_width, WER_flight_level, bar_width,
        alpha=opacity,
        label='Word Error Rate bei Fluglevel')

plt.xlabel('Äusserungen pro Intents')
plt.ylabel('Error Rate in %')
plt.ylim(0, 100)
plt.title('Auswertung LUIS')
plt.xticks(index + bar_width, ('10', '15', '20'))
plt.legend()

plt.tight_layout()
plt.savefig('result.pdf')
plt.show()
