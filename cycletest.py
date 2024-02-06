import easy_scpi as scpi 
import time, os, logging
from datetime import datetime

#def logconfig():
#logging.basicConfig(filename='aaa.log', encoding='utf-8', level=logging.INFO)


# SCPI Verbindung Herstellen


def read_cycle():
    print("Reading cycle data...")
    with open("D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/cycle/1Ah Zyklus WLTP.CSV", 'r') as file:
        data = [float(row.replace(',', '.')) for row in file]
    return data

def datastr():
    data = str(inst.query('MEAS:VOLT?;MEAS:CURR?;MEAS:POW?')).split(";")
    print(data)
    
    
# def test_watt_cycle(watt):
#     for x in range(0,1):
#         for item in watt:
#             if float(item) < 0:
#                 print("Positiv " + str(item))
#                 inst.write('VOLT 41' + ';POW ' + str(item))
#                 datastr()
#             else:
#                 print("Negativ " + str(item))
#                 inst.write('VOLT 48' + ';POW ' + str(item))
#                 datastr()

#         print("Zyklus Durchlauf " + str(x) + " abgeschlossen")
#     return "Watt Zyklus beendet"

# test_watt_cycle(read_cycle())   
inst = scpi.Instrument('COM6')
inst.connect()
inst.write('SYST:LOCK ON') # AYBABTU https://www.youtube.com/watch?v=ynQdJe48bkE

inst.write('SINK:POW 27.81495')
# Verbindung beenden
inst.disconnect()



    
    