import pandas as pd
from pandasgui import show
import tkinter as tk
from tkinter import filedialog

# Öffnet einen Dateiauswahldialog
root = tk.Tk()
root.withdraw()  # Versteckt das Hauptfenster von tkinter
file_path = filedialog.askopenfilename()

# Wenn ein Dateipfad ausgewählt wurde
if file_path:
    # Liest die Datei mit Pandas
    df = pd.read_csv(file_path, sep=';')
    df.columns = ['Zeitstempel', 'StromSoll','StromIST','Spannung','Temp','SOC','Spalte', 'Spalte2', 'Spalte3','Dateiname']
    
    # Zeigt den DataFrame in PandasGUI
    show(df)
