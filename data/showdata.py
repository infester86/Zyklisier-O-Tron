import pandas as pd
import matplotlib.pyplot as plt

# Daten einlesen
df = pd.read_csv('WattOvernighter.csv', sep=';', names=['timestamp', 'voltage', 'current', 'capacity'], parse_dates=['timestamp'])

# Daten visualisieren
plt.figure(figsize=(12, 6))

plt.subplot(311)
plt.plot(df['timestamp'], df['voltage'], label='Voltage')
plt.legend()