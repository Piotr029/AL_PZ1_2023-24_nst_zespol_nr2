import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter import simpledialog

class SimpleUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Testowanie Przesyłania Danych")
        
        self.typy = []
        self.czesci = []
        self.wybrna_kol = ""

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
        
        #self.text_czesci = tk.Text(self.root, height=10, width=80)

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
        
        #self.text_czesci.grid(row=6, columnspan=2, pady=10)
        
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nazwa", "Typ", "Parametr1", "Parametr2", "Parametr3"))
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Nazwa", text="Nazwa", anchor=tk.W)
        self.tree.heading("Typ", text="Typ", anchor=tk.W)
        self.tree.heading("Parametr1", text="Parametr 1", anchor=tk.W)
        self.tree.heading("Parametr2", text="Parametr 2", anchor=tk.W)
        self.tree.heading("Parametr3", text="Parametr 3", anchor=tk.W)

        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tree.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tree.column("Nazwa", stretch=tk.NO, minwidth=0, width=150)
        self.tree.column("Typ", stretch=tk.NO, minwidth=0, width=150)
        self.tree.column("Parametr1", stretch=tk.NO, minwidth=0, width=100)
        self.tree.column("Parametr2", stretch=tk.NO, minwidth=0, width=100)
        self.tree.column("Parametr3", stretch=tk.NO, minwidth=0, width=100)
        
        # Dodanie menu kontekstowego
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.tree.grid(row=6, columnspan=2, pady=10)


    def run(self):
        self.update_combobox_options()
        self.update_tree()
        self.root.mainloop()
        
    def update_combobox_options(self):
        self.combobox_typ["values"] = self.typy
    
    # def update_text(self):
    #     self.text_czesci.delete(1.0, tk.END)
        
    #     for czesc in self.czesci:
    #         self.text_czesci.insert(tk.END, f"{czesc}\n") 
    
    def update_tree(self):
        # Usunięcie istniejących wierszy z Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Wstawienie nowych danych do Treeview
        for czesc in self.czesci:
            self.tree.insert("", "end", values=czesc.replace("NONE","-").split(","))       
        
    def dane_z_formularza(self):
        dane = []
        dane.append(self.z_entry_nazwa.get())
        dane.append(self.combobox_typ.current()+1)
        dane.append(self.z_entry_parametr1.get())
        dane.append(self.z_entry_parametr2.get())
        dane.append(self.z_entry_parametr3.get())
        return dane
    
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.wybrna_kol = self.tree.identify_column(event.x)
            self.context_menu.post(event.x_root, event.y_root)

    def show_combobox_dialog(self, title, values):
        dialog = Dialog_zmiana_typu(self.root, title, values)
        dialog_result = dialog.result
        return dialog_result

    def handle_option3(self):
        selected_item = self.tree.selection()
        if selected_item:
            print(f"Opcja 3 dla wiersza: {self.tree.item(selected_item)['values']}")
            
class Dialog_zmiana_typu(simpledialog.Dialog):
    def __init__(self, parent, title, values):
        self.values = values
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        self.combobox = ttk.Combobox(master, values=self.values)
        self.combobox.pack(pady=10)
        return master

    def ok_pressed(self):
        self.result = self.combobox.current()+1
        self.destroy()
        
    def cancel_pressed(self):
        self.destroy()


    def buttonbox(self):
        self.ok_button = tk.Button(self, text='Ok', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())          


if __name__ == "__main__":
    app = SimpleUI()
    app.run()
