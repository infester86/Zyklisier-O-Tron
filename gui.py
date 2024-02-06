import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports, json
from PIL import ImageTk, Image

class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.img = ImageTk.PhotoImage(Image.open("Tim-O-Tron.png"))
        self.root.title("EA-Tim-O-Tron")	
        self.setup_ui()
        self.pack_ui()
        self.update_ports()
        
    def update_ports(self):
        ports = serial.tools.list_ports.grep("")
        port_names = [port.device for port in ports]
        self.port_var.set('')  # set to empty
        self.port_menu['menu'].delete(0, 'end')
        for name in port_names:
            self.port_menu['menu'].add_command(label=name, command=tk._setit(self.port_var, name))

    def export(self):
        # COM Port
        port = self.port_var.get()
        
        # Allgemeine Parameter
        dateiname = self.dateiname_entry.get()
        maxvolt = self.maxvolt_entry.get()
        minvolt = self.minvolt_entry.get()
        ccurr = self.ccurr_entry.get()
        dcurr = self.dcurr_entry.get()
        ccutoff = self.ccutoff_entry.get()
        dcutoff = self.dcutoff_entry.get()
        crest = self.crest_entry.get()
        drest = self.drest_entry.get()

        # Innenwiderstand Test
        ires_check = self.ires_var.get()
        ires_volt = self.ires_volt_entry.get()
        ires_curr = self.ires_curr_entry.get()
        ires_cutoff = self.ires_cutoff_entry.get()
        ires_timecutoff = self.ires_timecutoff_entry.get()
        ires_rest = self.ires_rest_entry.get()

        # Zyklisieren
        cycle_check = self.cycle_var.get()
        cycle_watt_check = self.cycle_watt_var.get()
        cycle_nr = self.cycle_nr_entry.get()

        # Rescue Charge
        rescue_check = self.rescue_var.get()
        rescue_volt = self.rescue_volt_entry.get()
        rescue_cutoff = self.rescue_cutoff_entry.get()
        
        settings =  {
            'Allgemein': {
                'dateiname': dateiname,
                'maxvolt': maxvolt,
                'minvolt': minvolt,
                'ccurr': ccurr,
                'dcurr': dcurr,
                'ccutoff': ccutoff,
                'dcutoff': dcutoff,
                'crest': crest,
                'drest': drest,
                'port': port # 'COM5
            },
            'Innenwiderstand': {
                'ires_check': ires_check, # 'ON' or 'OFF
                'ires_volt': ires_volt,
                'ires_curr': ires_curr,
                'ires_cutoff': ires_cutoff,
                'ires_timecutoff': ires_timecutoff,
                'ires_rest': ires_rest
            },
            'Zyklisieren': {
                'cycle_check': cycle_check, # 'ON' or 'OFF
                'cycle_watt_check': cycle_watt_check, # 'ON' or 'OFF
                'cycle_nr': cycle_nr
            },
            'Rescue Charge': {
                'rescue_check': rescue_check, # 'ON' or 'OFF
                'rescue_volt': rescue_volt,
                'rescue_cutoff': rescue_cutoff
            }
        }
        return settings
    
    def start(self):
        self.exported_data = self.export()
        self.root.quit()
        
    def save_settings(settings, filename):
        with open(filename, 'w') as f:
            json.dump(settings, f)

    def load_settings(filename):
        with open(filename, 'r') as f:
            return json.load(f)
        
    def toggle_ires(self):
        if self.cycle_var.get():
            self.rescue_volt_entry.config(state='normal')
            self.rescue_cutoff_entry.config(state='normal')
        else:
            self.rescue_volt_entry.config(state='disabled')
            self.rescue_cutoff_entry.config(state='disabled')

    def toggle_cycle(self):
        if self.cycle_var.get():
            self.rescue_volt_entry.config(state='normal')
            self.rescue_cutoff_entry.config(state='normal')
        else:
            self.rescue_volt_entry.config(state='disabled')
            self.rescue_cutoff_entry.config(state='disabled')

    def toggle_cycle_watt(self):
        if self.cycle_var.get():
            self.rescue_volt_entry.config(state='normal')
            self.rescue_cutoff_entry.config(state='normal')
        else:
            self.rescue_volt_entry.config(state='disabled')
            self.rescue_cutoff_entry.config(state='disabled')

    def toggle_rescue(self):
        if self.rescue_var.get():
            self.rescue_volt_entry.config(state='normal')
            self.rescue_cutoff_entry.config(state='normal')
        else:
            self.rescue_volt_entry.config(state='disabled')
            self.rescue_cutoff_entry.config(state='disabled')

    def setup_ui(self):
        # COM Port
        self.port_var = tk.StringVar()
        self.port_menu = tk.OptionMenu(self.root, self.port_var, '')
        self.update_button = tk.Button(self.root, text="Update Ports", command=self.update_ports)
        
        # Logo
        self.panel = tk.Label(self.root, image = self.img)
        
        # Allgemeine Parameter
        self.allgemein_label = ttk.Label(self.root, text="Allgemeine Parameter")
        self.dateiname_label = ttk.Label(self.root, text="Dateiname:")
        self.dateiname_entry = ttk.Entry(self.root, width=15)
        self.maxvolt_label = ttk.Label(self.root, text="Max. (V):")
        self.maxvolt_entry = ttk.Entry(self.root, width=15)
        self.minvolt_label = ttk.Label(self.root, text="Min. (V):")
        self.minvolt_entry = ttk.Entry(self.root, width=15)
        self.ccurr_label = ttk.Label(self.root, text="Charge Max. (A):")
        self.ccurr_entry = ttk.Entry(self.root, width=15)
        self.dcurr_label = ttk.Label(self.root, text="Discharge Max. (A):")
        self.dcurr_entry = ttk.Entry(self.root, width=15)
        self.ccutoff_label = ttk.Label(self.root, text="Charge Cutoff (A):")
        self.ccutoff_entry = ttk.Entry(self.root, width=15)
        self.dcutoff_label = ttk.Label(self.root, text="Discharge Cutoff (A):")
        self.dcutoff_entry = ttk.Entry(self.root, width=15)
        self.crest_label = ttk.Label(self.root, text="Charge Pause (s):")
        self.crest_entry = ttk.Entry(self.root, width=15)
        self.drest_label = ttk.Label(self.root, text="Discharge Pause (s):")
        self.drest_entry = ttk.Entry(self.root, width=15)
        
        # Innenwiderstandtest
        self.ires_var = tk.BooleanVar()
        self.ires_label = ttk.Label(self.root, text="Innenwiderstandstest")
        self.ires_check = ttk.Checkbutton(self.root, text="ON", variable=self.ires_var, command=self.toggle_ires)
        self.ires_volt_label = ttk.Label(self.root, text="Spannung (V):")
        self.ires_volt_entry = ttk.Entry(self.root, width=15)
        self.ires_curr_label = ttk.Label(self.root, text="Stromstärke (A):")
        self.ires_curr_entry = ttk.Entry(self.root, width=15)
        self.ires_cutoff_label = ttk.Label(self.root, text="Cutoff (A):")
        self.ires_cutoff_entry = ttk.Entry(self.root, width=15)
        self.ires_timecutoff_label = ttk.Label(self.root, text="Dauer (s):")
        self.ires_timecutoff_entry = ttk.Entry(self.root, width=15)
        self.ires_rest_label = ttk.Label(self.root, text="Pause (s):")
        self.ires_rest_entry = ttk.Entry(self.root, width=15)
        
        # Zyklisieren
        self.cycle_var = tk.BooleanVar()
        self.cycle_watt_var = tk.BooleanVar()
        self.cycle_label = ttk.Label(self.root, text="Zyklisierung")
        self.cycle_check = ttk.Checkbutton(self.root, text="ON", variable=self.cycle_var, command=self.toggle_cycle)
        self.cycle_watt_check = ttk.Checkbutton(self.root, text="Watt", variable=self.cycle_watt_var, command=self.toggle_cycle_watt)
        self.cycle_nr_label = ttk.Label(self.root, text="Zyklenzahl:")
        self.cycle_nr_entry = ttk.Entry(self.root, width=15)
        
        # Rescue Charge
        self.rescue_var = tk.BooleanVar()
        self.rescue_label = ttk.Label(self.root, text="Rescuecharge")
        self.rescue_check = ttk.Checkbutton(self.root, text="ON", variable=self.rescue_var, command=self.toggle_rescue)
        self.rescue_volt_label = ttk.Label(self.root, text="Spannung (V):")
        self.rescue_volt_entry = ttk.Entry(self.root, width=15)
        self.rescue_cutoff_label = ttk.Label(self.root, text="Cutoff (A):")
        self.rescue_cutoff_entry = ttk.Entry(self.root, width=15)
        
        self.submit_button = ttk.Button(self.root, text="Starten", command=self.start)

    def pack_ui(self):
        # Packen der Widgets
        #Allgemein
        #self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.allgemein_label.grid(row=0, column=0, columnspan=2)
        self.dateiname_label.grid(row=1, column=0)
        self.dateiname_entry.grid(row=1, column=1)
        self.maxvolt_label.grid(row=2, column=0)
        self.maxvolt_entry.grid(row=2, column=1)
        self.minvolt_label.grid(row=3, column=0)
        self.minvolt_entry.grid(row=3, column=1)
        self.ccurr_label.grid(row=4, column=0)
        self.ccurr_entry.grid(row=4, column=1)
        self.dcurr_label.grid(row=5, column=0)
        self.dcurr_entry.grid(row=5, column=1)
        self.ccutoff_label.grid(row=6, column=0)
        self.ccutoff_entry.grid(row=6, column=1)
        self.dcutoff_label.grid(row=7, column=0)
        self.dcutoff_entry.grid(row=7, column=1)
        self.crest_label.grid(row=8, column=0)
        self.crest_entry.grid(row=8, column=1)
        self.drest_label.grid(row=9, column=0)
        self.drest_entry.grid(row=9, column=1)
        self.submit_button.grid(row=9, column=5)

        #Rescuecharge
        self.rescue_label.grid(row=0, column=2, columnspan=2)
        self.rescue_check.grid(row=1, column=2, columnspan=2)
        self.rescue_volt_label.grid(row=2, column=2)
        self.rescue_volt_entry.grid(row=2, column=3)
        self.rescue_cutoff_label.grid(row=3, column=2)
        self.rescue_cutoff_entry.grid(row=3, column=3)

        #Zyklisieren
        self.cycle_label.grid(row=5, column=2,columnspan=2)
        self.cycle_check.grid(row=6, column=2,columnspan=1)
        self.cycle_watt_check.grid(row=6, column=3,columnspan=1)
        self.cycle_nr_label.grid(row=7, column=2)
        self.cycle_nr_entry.grid(row=7, column=3)

        #Innenwiderstandstest
        self.ires_label.grid(row=0, column=4,columnspan=2)
        self.ires_check.grid(row=1, column=4,columnspan=2)
        self.ires_volt_label.grid(row=2, column=4)
        self.ires_volt_entry.grid(row=2, column=5)
        self.ires_curr_label.grid(row=3, column=4)
        self.ires_curr_entry.grid(row=3, column=5)
        self.ires_cutoff_label.grid(row=4, column=4)
        self.ires_cutoff_entry.grid(row=4, column=5)
        self.ires_timecutoff_label.grid(row=5, column=4)
        self.ires_timecutoff_entry.grid(row=5, column=5)
        self.ires_rest_label.grid(row=6, column=4)
        self.ires_rest_entry.grid(row=6, column=5)

        # Buttons
        self.port_menu.grid(row=9, column=3)
        self.update_button.grid(row=9, column=4)
        self.submit_button.grid(row=9, column=5)

    def run(self):
        self.root.mainloop()
        return self.exported_data
