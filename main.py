
import queue,threading, os, time
from gui import Gui
from ea import EA
        
def cycler(dataq,settings):    
    EA1 = EA(settings['Allgemein'],dataq)
    print(settings['Allgemein'])
    print(settings['Zyklisieren'])
    
    if settings['Innenwiderstand']['ires_check'] == True:
        print(settings['Innenwiderstand'])
        EA1.test_ires(settings['Innenwiderstand'])
    else:
        print("Kein Innenwiderstandstest gewünscht")
        pass
    
    if settings['Zyklisieren']['cycle_check'] == True and settings['Zyklisieren']['cycle_watt_check'] == False:
        print(settings['Zyklisieren'])
        EA1.test_cycle(settings['Zyklisieren'])
    else:
        print("Keine Zyklisierung der Zelle gewünscht")
        pass
    
    if settings['Zyklisieren']['cycle_check'] == True and settings['Zyklisieren']['cycle_watt_check'] == True:
        print(settings['Zyklisieren'])
        watt = read_cycle()
        print(watt)
        EA1.test_watt_cycle(settings['Zyklisieren'],watt)
    else:
        print("Keine Watt Zyklisierung der Zelle gewünscht")
        pass
    
    if settings['Rescue Charge']['rescue_check'] == True:
        print(settings['Rescue Charge'])
        EA1.rescuecharge(settings['Rescue Charge']['rescue_volt'],settings['Rescue Charge']['rescue_cutoff'])
    else:
        print("Keine Aufladung zum schonen der Zelle gewünscht")
        pass
    
def speichern(dataq, dateiname):
    folder = "D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/data"
    filename = str(dateiname) + ".csv"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    komplett = os.path.join(folder, filename)
        
    with open(komplett, 'w') as f:
        pass

    print("Running save thread...")
    while True:
        try:
            data = dataq.get()
            print("Data: ", data)
            with open(komplett, "a+") as csvfile:
                csvfile.write(str(data) + "\n")
        except Exception as e:
            print("Error: ", e)

def read_cycle():
    print("Reading cycle data...")
    with open("D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/cycle/1Ah Zyklus WLTP.CSV", 'r') as file:
        data = [float(row.replace(',', '.')) for row in file]
    return data

def main():
    dataq = queue.Queue()

    print("Tim-O-Tron\n")

    gui_o_tron = Gui()
    settings = gui_o_tron.run()

    # Erstellen Sie Threads für die save und cycler Funktionen
    cycler_thread = threading.Thread(target=cycler, args=(dataq, settings))
    save_obj_thread = threading.Thread(target=speichern, args=(dataq, settings['Allgemein']['dateiname']))

    cycler_thread.start()
    save_obj_thread.start()

if __name__ == "__main__":
    main()
 