import easy_scpi as scpi 
import time, os, logging, csv
from datetime import datetime

# SCPI Verbindung Herstellen
#inst = scpi.Instrument('COM8')
#inst.connect()


# Befehle
# Output An/Aus: inst.write('OUTP ON') / inst.write('OUTP OFF')
# Messen: inst.query('MEAS:VOLT?;MEAS:CURR?;MEAS:POW?')
# Entladen: inst.write('SINK:CURR ' + str(Curr))
# Laden: inst.write('CURR ' + str(Curr))

# Allgemeine Variabeln
# Abfragen oder aus Datei importieren
version = 0.002
pathcycle = "D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/cycle/"
pathsettings = "D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/settings/"

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
    
    
        

#inst.write('SYST:LOCK ON') # AYBABTU https://www.youtube.com/watch?v=ynQdJe48bkE
#dateiname,maxvolt,midvolt,minvolt,ccurr,dcurr,ccutoff,dcutoff,crest,drest,cyclenr = askforsettings()
#zyklus(dateiname,maxvolt,midvolt,minvolt,ccurr,dcurr,ccutoff,dcutoff,crest,drest,cyclenr)

def read_settings(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    return data

def read_cycle(filename):
    with open(filename, 'r') as file:
        data = [float(row.replace(',', '.')) for row in file]
    return data

def settings(pathcycle, data):
    name=data[0][0]
    vmin=data[0][1]
    vmid=data[0][2]
    vmax=data[0][3]
    currcharge=data[0][4]
    currdischarge=data[0][5]
    rest=data[0][6]
    cyclecount=data[0][7]
    cyclename=data[0][8]
    cycle=read_cycle(pathcycle + str(cyclename))
    return name,vmin,vmid,vmax,currcharge,currdischarge,rest,cyclecount,cyclename,cycle

def settingscheck(name,vmin,vmid,vmax,currcharge,currdischarge,rest,cyclecount,cyclename,cycle):
    print("Name: " + str(name))
    print("Min. Spannung: " + str(vmin))
    print("Mid. Spannung: " + str(vmid))
    print("Max. Spannung: " + str(vmax))
    print("Stromstärke Laden: " + str(currcharge))
    print("Stromstärke Entladen: " + str(currdischarge))
    print("Pause: " + str(rest))
    print("Zyklen: " + str(cyclecount))
    print("Zyklusname: " + str(cyclename))
    print("Zyklenzahl: " + str(cyclecount))
    
    print("Settings übernehmen? (y/n)")
    
    if input() == "y":
        print("Settings übernommen")
        return
    else:    
        print("Settings verworfen")
        exit() 

def calculatecap(cap, i, start):
    cap = cap + i * ((time.time() - start) + 1) / 3600
    return cap

def datastr(dateiname,start):
    ts = gettime()
    data = str(inst.query('MEAS:VOLT?;MEAS:CURR?')).split(";")
    v = nounit(data[0])
    i = nounit(data[1])
    cap = cap + i * ((time.time() - start) + 1) / 3600
    
    #print(str(ts) + ";" + str(v) + ";" + str(i) + ";" + str(cap))
    save(str(ts) + ";" + str(v) + ";" + str(i) + ";" + str(cap),csvpath)
    return v,i
    
def discharge(voltage):
    cap = 0    
    inst.write('VOLT ' + str(vmin))
    inst.write('OUTP ON')
    rest(1)
    while True:
        start = time.time()
        v,i,cap = datastr(dateiname, start, cap)
        if v <= (-abs(float(vmin))):
            inst.write('OUTP OFF')
            return
        time.sleep(1)
    return

def charge(voltage):
    cap = 0    
    inst.write('VOLT ' + str(vmax))
    inst.write('OUTP ON')
    rest(1)
    while True:
        start = time.time()
        v,i,cap = datastr(dateiname, start, cap)
        if v >= (-abs(float(vmax))):
            inst.write('OUTP OFF')
            return
        time.sleep(1)
    return cap

def charge(vmin,vmax,cap,cycle):
    cap = cap   
    inst.write('VOLT ' + str(vmax))
    inst.write('OUTP ON')
    rest(1)
    while True:
        for item in watt:
            if float(item) < 0:
                print("Die Zahl ist negativ.")
                inst.write('VOLT ' + vmin + ';POW ' + str(item))
            else:
                print("Die Zahl ist positiv.")
                inst.write('VOLT ' + vmax + ';POW ' + str(item))
                        start = time.time()
                v,i,cap = datastr(dateiname, start, cap)
        
        start = time.time()
        v,i,cap = datastr(dateiname, start, cap)
        if v >= (-abs(float(vmax))):
            inst.write('OUTP OFF')
            return
        time.sleep(1)
    return cap


for item in watt:
    if float(item) < 0:
        print("Die Zahl ist negativ.")
        inst.write('VOLT ' + vmin + ';POW ' + str(item))
    else:
        print("Die Zahl ist positiv.")
        inst.write('VOLT ' + vmax +
                   ';POW ' + str(item))
         
#    time.sleep(1)
        
# Main Programm
def main():
    print("Zyklisier-O-Tron " + str(version) + "\n")
    # Weitere Anweisungen hier
    print("Settings aus Datei lesen\n")
    data = read_settings(str(pathsettings) + "Leonard-Testzelle.csv")
    print(data)
    name, vmin, vmid, vmax, currcharge, currdischarge, rest, cyclecount, cyclename, cycle = settings(pathcycle, data)
    settingscheck(name, vmin, vmid, vmax, currcharge, currdischarge, rest, cyclecount, cyclename, cycle)
    
    

if __name__ == "__main__":
    main()

# Datenstring erstellen

                        
#watt = read_cycle("D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/cycle/1Ah Zyklus WLTP.CSV")
#print(watt)


    
#inst.write('OUTP ON')


    

    



# SINK:POW˽4500
# POW˽3000 Absolute Kurzform. Setzt 3000 W.
# SOUR:POWER˽3.5kW G
# SOURCE:VOLTAGE MIN 2.0
# SOURCE:VOLTAGE MAX 3.65
# INP˽ON
# OUTP˽ON 

#try:
#    print("Einstellungen setzen")
#    inst.write('SOURCE:VOLTAGE 2.0')
#    inst.write('VOLT 3.65')
#    inst.write('INP ON')
    
#except:
#    # Verbindung beenden
#    print("Fehler:", e)
#    inst.disconnect()
    
# Verbindung beenden
#inst.disconnect()
