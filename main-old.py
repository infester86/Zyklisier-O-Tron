import easy_scpi as scpi 
import time, os, logging
from datetime import datetime

#def logconfig():
#logging.basicConfig(filename='aaa.log', encoding='utf-8', level=logging.INFO)


# SCPI Verbindung Herstellen
inst = scpi.Instrument('COM6')
inst.connect()

# Befehle
# Output An/Aus: inst.write('OUTP ON') / inst.write('OUTP OFF')
# Messen: inst.query('MEAS:VOLT?;MEAS:CURR?;MEAS:POW?')
# Entladen: inst.write('SINK:CURR ' + str(Curr))
# Laden: inst.write('CURR ' + str(Curr))

# Allgemeine Variabeln
# Abfragen oder aus Datei importieren
version = 0.002

# Globaler Mist den ich nicht besser lösen konnte
cap = 0

# Funktionen
# Speichergeschichten
def createfile(ts):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    csvpath = "data/" + str(createfilename(ts))
    return csvpath

# Dateinamen generieren
def createfilename(dateiname):
    name = str(dateiname) + ".csv"
    return name

# Speichern der Daten
def save(data,csvpath):
    with open(csvpath, "a") as csvfile:# we write row by row and element by element; "a" for append 
                csvfile.write(data + "\n")
# Timestamp                
def gettime():
    dt = datetime.now() #ts = datetime.timestamp(dt)
    return dt

# Formatierungsgeschichten
# Einheit entfernen 
def nounit(data):
    value = str(data).split(" ")
    return float(value[0])

# Neu setzen der Stromstärken beim Laden und Entladen
# Wert verstellt sich durch CV
def setpara(ccurr,dcurr):
    inst.write('SINK:CURR ' + str(dcurr))
    inst.write('CURR ' + str(ccurr))
    
# Datenstring erstellen
def datastr(dateiname,start):
    global cap
    ts = gettime()
    csvpath = createfile(dateiname)
    data = str(inst.query('MEAS:VOLT?;MEAS:CURR?')).split(";")
    v = nounit(data[0])
    i = nounit(data[1])
    cap = cap + i * ((time.time() - start) + 1) / 3600
    
    #print(str(ts) + ";" + str(v) + ";" + str(i) + ";" + str(cap))
    save(str(ts) + ";" + str(v) + ";" + str(i) + ";" + str(cap),csvpath)
    return v,i

# Laden
def charge(maxvolt,ccutoff,dateiname):
    global cap #
    cap = 0
    logging.info("Laden")
    inst.write('VOLT ' + str(maxvolt))
    logging.info("Spannung gesetzt")
    inst.write('OUTP ON')
    logging.info("Output An")
    rest(1)
    while True:
        start = time.time()
        v,i = datastr(dateiname, start)

        if i <= float(ccutoff):
            logging.info("Cut Off Erreicht")
            inst.write('OUTP OFF')
            logging.info("Output OFF")
            return    
        time.sleep(1)
        
# Laden
def rescuecharge(midvolt,ccutoff,dateiname):
    global cap
    cap = 0
    logging.info("Laden")
    inst.write('VOLT ' + str(midvolt))
    logging.info("Spannung gesetzt")
    inst.write('OUTP ON')
    logging.info("Output An")
    rest(1)
    while True:
        start = time.time()
        v,i = datastr(dateiname, start)
        if i <= float(ccutoff):
            logging.info("Cut Off Erreicht")
            inst.write('OUTP OFF')
            logging.info("Output OFF")
            return    
        time.sleep(1)

# Entladen
def discharge(minvolt,dcutoff,dateiname):
    global cap
    cap = 0
    logging.info("Entladen")
    inst.write('VOLT ' + str(minvolt))
    logging.info("Spannung gesetzt")
    inst.write('OUTP ON')
    logging.info("Output On")
    rest(1)
    while True:
        start = time.time()
        v,i = datastr(dateiname, start)
        if i >= (-abs(float(dcutoff))):
            logging.info("Cut Off Erreicht")
            inst.write('OUTP OFF')
            logging.info("Output OFF")
            return
        time.sleep(1)
        
# Pause    
def rest(seconds):
    global cap
    cap = 0
    logging.info("Pause")
    
    for i in range(0,seconds):
        v,i = datastr(dateiname,0)
        time.sleep(1)
        
# Zyklus aus komplett Laden und Entladen        
def zyklus(dateiname,maxvolt,midvolt,minvolt,ccurr,dcurr,ccutoff,dcutoff,crest,drest,cyclenr):
	setpara(ccurr,dcurr)
	print("Entladen gestartet")
	discharge(minvolt,dcutoff,dateiname)
	print("Zyklus gestartet")
	for x in range(0,int(cyclenr)): 
		charge(maxvolt,ccutoff,dateiname)
		rest(int(crest))
		discharge(minvolt,dcutoff,dateiname)
		rest(int(drest))
		print("Zyklus Durchlauf " + str(x) + " abgeschlossen")
	rescuecharge(midvolt,ccutoff,dateiname)
	print("Zyklus beendet")

# Settingsabfragen
def askforsettings():
    while True:
        dateiname = input("Dateiname: ")
        maxvolt = input("Batteriespannung Max.: ")
        midvolt = input("Batteriespannung Mid.: ")
        minvolt = input("Batteriespannung Min.: ")
        ccurr = input("Stromstärke Charge Max.: " )
        dcurr = input("Stromstärke Discharge Max.: " )
        ccutoff = input("Charge Cutoff: ")
        dcutoff = input("Discharge Cutoff: ")
        crest = input("Charge Pause: ")
        drest = input("Discharge Pause: ")
        cyclenr = input("Zyklenzahl: ")
        
        print("Dateiname " + str(dateiname) + "\n" + str(maxvolt) + " V Max\n" + str(midvolt) + " V Mid\n" + str(minvolt) + " V Min\n" + str(ccurr) + " A Laden\n" +
              str(dcurr) + " A Entladen\n" + str(ccutoff)  + " A Cutoff Laden\n" + str(dcutoff) +
              " A Cutoff Entladen\n" + str(crest) + " Pausenzeit Laden\n" + str(drest) +
              " Pausenzeit Entladen\n" + str(cyclenr) + " Anzahl der Zyklen\n")
    
        start = input ("GO zum Starten: ")
        
        if start == "GO":
            return dateiname,maxvolt,midvolt,minvolt,ccurr,dcurr,ccutoff,dcutoff,crest,drest,cyclenr
        else:
            pass
    
    
        
# Main Programm
print("Zyklisier-O-Tron " + str(version) + "\n")
inst.write('SYST:LOCK ON') # AYBABTU https://www.youtube.com/watch?v=ynQdJe48bkE
dateiname,maxvolt,midvolt,minvolt,ccurr,dcurr,ccutoff,dcutoff,crest,drest,cyclenr = askforsettings()
zyklus(dateiname,maxvolt,midvolt,minvolt,ccurr,dcurr,ccutoff,dcutoff,crest,drest,cyclenr)







# Verbindung beenden
inst.disconnect()
