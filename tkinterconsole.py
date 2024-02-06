import tkinter as tk
import sys

class ConsoleOutput(tk.Tk):
    def __init__(self):
        super().__init__()

        self.text = tk.Text(self)
        self.text.pack()

        sys.stdout = self

        self.print_loop()

    def write(self, txt):
        self.text.insert(tk.END, txt)
        self.update()

    def flush(self):
        pass

    def print_loop(self):
        print("test")
        self.after(1000, self.print_loop)  # Aktualisierung alle 1 Sekunde

app = ConsoleOutput()

print("Hello, world!")
app.mainloop()

