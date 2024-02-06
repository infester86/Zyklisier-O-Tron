import easy_scpi as scpi
import time,queue
from datetime import datetime 

class EA:    
    def __init__(self, settings,data):
        self.inst = scpi.Instrument(settings['port'])
        self.inst.connect()
        self.inst.write('SYST:LOCK ON') # AYBABTU https://www.youtube.com/watch?v=ynQdJe48bkE
        self.cap = 0
        self.version = 0.001
        self.maxvolt = settings['maxvolt']
        self.minvolt = settings['minvolt']
        self.ccurr = settings['ccurr']
        self.dcurr = settings['dcurr']
        self.drest = int(float(settings['drest']))
        self.crest = int(float(settings['crest']))
        self.ccutoff = settings['ccutoff']
        self.dcutoff = settings['dcutoff']
        self.dataq = data
        print(settings)
        print(self.maxvolt)
            
    def nounit(self, data):
        value = str(data).split(" ")
        return float(value[0])
    
    def datastr(self):
        timestamp = datetime.now()
        data = str(self.inst.query('MEAS:VOLT?;MEAS:CURR?;MEAS:POW?;STAT:OPER:COND?')).split(";")
        print(data)
        v = self.nounit(data[0])
        i = self.nounit(data[1])
        p = self.nounit(data[2])
        con = data[3]

        
        cap = self.calc_cap(int(timestamp.timestamp()),i)         
        # Fixing Problem 1, 2, and 3
        print(str(timestamp) + ";" + str(v) + ";" + str(i) + ";" + str(cap) + ";" + str(p))
        self.dataq.put(str(timestamp) + ";" + str(v) + ";" + str(i) + ";" + str(cap) + ";" + str(p) + ";" + str(con))
        return v,i,con
           
    def setpara(self,volt,curr,cutoff):
        self.cap = 0
        self.inst.write('VOLT ' + str(volt) + ';CURR ' + str(curr) + ';SINK:CURR ' + str(curr)+';POW MAX;' + 'SINK:POW MAX')
        self.inst.write('OUTP ON')
        self.rest(1)
        
        
    def rest(self,seconds):
        for x in range(0,int(float(seconds))):
            self.datastr()
            time.sleep(1)
       
    
    def charge(self,volt,curr,cutoff):
        self.setpara(volt,curr,cutoff)
        v,i,con = self.datastr()
        while True:            
            v,i,con = self.datastr()
            #Cut OFF erreicht abschalten
            if i <= float(cutoff):
                self.inst.write('OUTP OFF')
                return "Laden abgeschlossen"
            time.sleep(1)
       
    def discharge(self,volt,curr,cutoff):
        self.setpara(volt,curr,cutoff)
        while True:            
            v,i,con = self.datastr()
            #Cut OFF erreicht abschalten
            if i >= (-abs(float(cutoff))):
                self.inst.write('OUTP OFF')
                return "Entladen abgeschlossen"
            #Cut OFF erreicht abschalten
            if i >= (-abs(float(cutoff))):
                self.inst.write('OUTP OFF')
                return "Entladen abgeschlossen"
            time.sleep(1)
    
    def rescuecharge(self,volt,cutoff):
        print("Rescuecharge gestartet")
        self.charge(volt,self.ccurr,cutoff)
        return "Rescuecharge abgeschlossen"
    
    # All Calculation Happen here        
    def calc_cap(self,start,i):
        self.cap = self.cap + i * ((time.time() - start) + 1) / 3600
        return self.cap      

    def calc_ires(self,v,oldv,i,oldi):
        r = (v-oldv) / (i-oldi)
        return (r)
 
    # This is how a Test Looks Like  
    # Test Innenwiderstand
    def test_ires(self,settings):
        print("Folgende Einstellungen werden für den Innenwiderstandstest verwendet: \n")
        print(settings)
        
        v,i,con = self.datastr()
        
        if v > float(settings['ires_volt']):
            self.discharge(str(settings['ires_volt']),self.dcurr,str(settings['ires_cutoff']))
            self.rest(int(float(self.crest)))
        if v < float(settings['ires_volt']):
            self.charge(str(settings['ires_volt']),self.ccurr,str(settings['ires_cutoff']))
            self.rest(int(float(self.drest)))
        if v == float(settings['ires_volt']):
            print("Zelle hat die gewünschte Spannung")
            self.rest(1)     

        self.rest(settings['ires_rest'])
        v,i,con = self.datastr()
        
        print("Folgende Einstellungen werden für den Innenwiderstandstest verwendet: \n")
        print(settings)
        
        v,i,con = self.datastr()
        
        if v > float(settings['ires_volt']):
            self.discharge(str(settings['ires_volt']),self.dcurr,str(settings['ires_cutoff']))
            self.rest(int(float(self.crest)))
        if v < float(settings['ires_volt']):
            self.charge(str(settings['ires_volt']),self.ccurr,str(settings['ires_cutoff']))
            self.rest(int(float(self.drest)))
        if v == float(settings['ires_volt']):
            print("Zelle hat die gewünschte Spannung")
            self.rest(1)     

        self.rest(settings['ires_rest'])
        v,i,con = self.datastr()
        
        oldv = v
        
        
        # Befehl für Test an gerät senden und starten
        self.setpara(str(self.maxvolt),str(settings['ires_curr']),str(settings['ires_cutoff']))
        self.setpara(str(self.maxvolt),str(settings['ires_curr']),str(settings['ires_cutoff']))
        
        for x in range(0,int(float(settings['ires_timecutoff']))+1):
            v,i,con = self.datastr()
            v,i,con = self.datastr()
            print("Dies ist Durchlauf Nummer", x)
            time.sleep(1)
            time.sleep(1)
        self.inst.write('OUTP OFF')
        #print(self.calc_ires(v,oldv,i,0)) 
        self.rest(int(float(settings['ires_rest'])))
        #print(self.calc_ires(v,oldv,i,0)) 
        self.rest(int(float(settings['ires_rest'])))
        return("Innenwiderstandstest abgeschlossen")
    
    
    # Test Zyklisieren
    # Zelle wird erst Entladen danach starten die Zyklus Durchläufe Zelle wird geladen und dann 
    def test_cycle(self,Zyklus):
        print("Batterie entladen")
        self.discharge(self.minvolt,self.dcurr,self.dcutoff)
        self.rest(int(float(self.drest)))
        self.discharge(self.minvolt,self.dcurr,self.dcutoff)
        self.rest(int(float(self.drest)))
        print("Zyklus gestartet")
        for x in range(0,int(Zyklus['cycle_nr'])): 
            self.charge(self.maxvolt,self.ccurr,self.ccutoff)
            self.rest(int(float(self.crest)))
            self.discharge(self.minvolt,self.dcurr,self.dcutoff)
            self.rest(int(float(self.drest)))
            self.charge(self.maxvolt,self.ccurr,self.ccutoff)
            self.rest(int(float(self.crest)))
            self.discharge(self.minvolt,self.dcurr,self.dcutoff)
            self.rest(int(float(self.drest)))
            print("Zyklus Durchlauf " + str(x) + " abgeschlossen")
        return "Zyklus beendet"
    
     
    def test_watt_cycle(self,Zyklus,watt):
        self.setpara(self.maxvolt,self.ccurr,self.ccutoff)
        self.rest(1)
        for x in range(0,int(Zyklus['cycle_nr'])):
            for item in watt:
                if float(item) < 0:
                    print("Negativ " + str(abs(float(item)))) 
                    self.inst.write('VOLT ' + self.maxvolt + ';POW ' + str(abs(float(item))))
                    v,i,con = self.datastr()
                    self.seccheck(v,con)
                    time.sleep(1)
                else:
                    print("Positiv " + str(item))
                    self.inst.write('VOLT ' + self.minvolt + ';SINK:POW ' + str(item))
                    v,i,con = self.datastr()
                    self.seccheck(v,con)
                    time.sleep(1)      
            print("Zyklus Durchlauf " + str(x) + " abgeschlossen")
            self.rest(int(float(self.drest)))
        return "Watt Zyklus beendet"
    
    def seccheck(self,v,con):
        if v > (float(self.maxvolt)+0.1):
            print("Zelle ist zu voll")
            self.inst.write('OUTP OFF')
            return("Zelle ist zu Voll")
        elif con == "4352\n" and v <= (float(self.minvolt)):
            print("CV Ladung beginnt Zelle wird geladen")
            self.charge(self.maxvolt,self.ccurr,self.ccutoff)
            self.rest(int(float(self.crest)))
            self.inst.write('OUTP ON')
        else:
            pass
      
    def quit(self):
        time.sleep(10)
        self.inst.close()
        return("EA Verbindung getrennt")