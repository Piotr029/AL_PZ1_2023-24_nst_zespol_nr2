import tkinter as tk
from tkinter import ttk

class SimpleUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Testowanie Przesyłania Danych")
        
        self.typy = []
        self.czesci = []

        # Tworzenie 
        label_nazwa = tk.Label(self.root, text="Nazwa:")
        self.z_entry_nazwa = tk.Entry(self.root)

        label_typ = tk.Label(self.root, text="Typ:")
        self.combobox_typ = ttk.Combobox(self.root, values=self.typy)

        label_parametr1 = tk.Label(self.root, text="Parametr 1:")
        self.z_entry_parametr1 = tk.Entry(self.root)

        label_parametr2 = tk.Label(self.root, text="Parametr 2:")
        self.z_entry_parametr2 = tk.Entry(self.root)

        label_parametr3 = tk.Label(self.root, text="Parametr 3:")
        self.z_entry_parametr3 = tk.Entry(self.root)

        self.button_dodaj = tk.Button(self.root, text="Dodaj")
        
        self.text_czesci = tk.Text(self.root, height=10, width=80)

        # Uklad
        label_nazwa.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.z_entry_nazwa.grid(row=0, column=1, padx=10, pady=5)

        label_typ.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.combobox_typ.grid(row=1, column=1, padx=10, pady=5)

        label_parametr1.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.z_entry_parametr1.grid(row=2, column=1, padx=10, pady=5)

        label_parametr2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.z_entry_parametr2.grid(row=3, column=1, padx=10, pady=5)

        label_parametr3.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.z_entry_parametr3.grid(row=4, column=1, padx=10, pady=5)

        self.button_dodaj.grid(row=5, columnspan=2, pady=10)
        
        self.text_czesci.grid(row=6, columnspan=2, pady=10)


    def run(self):
        self.update_combobox_options()
        self.update_text()
        self.root.mainloop()
        
    def update_combobox_options(self):
        self.combobox_typ["values"] = self.typy
    
    def update_text(self):
        self.text_czesci.delete(1.0, tk.END)
        
        for czesc in self.czesci:
            self.text_czesci.insert(tk.END, f"{czesc}\n")        
        
    def dane_z_formularza(self):
        dane = []
        dane.append(self.z_entry_nazwa.get())
        dane.append(self.combobox_typ.current()+1)
        dane.append(self.z_entry_parametr1.get())
        dane.append(self.z_entry_parametr2.get())
        dane.append(self.z_entry_parametr3.get())
        return dane

if __name__ == "__main__":
    app = SimpleUI()
    app.run()