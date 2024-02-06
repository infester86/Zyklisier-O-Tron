import os, time, queue

class Save:
    def __init__(self,dataq,dateiname):
        self.dataq = dataq
        self.folder="D:/Projekte/EA Hardware/Software/ea-zyklisier-o-tron/data"
        self.createfolder()
        self.path = self.folder + "/" + str(dateiname) + ".csv"
    
    def createfolder(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    # Speichern der Daten
    def run(self):
        print("Running save thread...")
        while True:
            try:
                data = self.dataq.get()
                print("Data: ", data)
                with open(self.path, "a+") as csvfile:
                    csvfile.write(str(data))
            except Exception as e:
                print("Error: ", e)
            time.sleep(1)
            