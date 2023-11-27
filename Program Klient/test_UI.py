import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class SimpleUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Testowanie Przesyłania Danych")
        
        self.typy = []
        self.czesci = []
        self.wybrna_kol = ""

        # Tworzenie podstawowych elementow
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
        

        # Umieszczanie podstawowych elementow
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
        
        #Tworzenie tabeli(treeview) do wyswietlania danych z bazdy danych
        #Deklaracja i tworzenie ile bedzie kolumn - id tych kolumn
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nazwa", "Typ", "Parametr1", "Parametr2", "Parametr3"))
        #nazwy naglowkow kolumn - #0 to kolumna obslugujaca "childy" gdyby byly
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Nazwa", text="Nazwa", anchor=tk.W)
        self.tree.heading("Typ", text="Typ", anchor=tk.W)
        self.tree.heading("Parametr1", text="Parametr 1", anchor=tk.W)
        self.tree.heading("Parametr2", text="Parametr 2", anchor=tk.W)
        self.tree.heading("Parametr3", text="Parametr 3", anchor=tk.W)
        #szerokosci kolumn
        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tree.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tree.column("Nazwa", stretch=tk.NO, minwidth=0, width=150)
        self.tree.column("Typ", stretch=tk.NO, minwidth=0, width=150)
        self.tree.column("Parametr1", stretch=tk.NO, minwidth=0, width=100)
        self.tree.column("Parametr2", stretch=tk.NO, minwidth=0, width=100)
        self.tree.column("Parametr3", stretch=tk.NO, minwidth=0, width=100)
        
        # Stworzenie menu kontekstowego
        self.context_menu = tk.Menu(self.root, tearoff=0)
        #Przypisanie menu do prawego przycisku myszy w obszarze tabeli
        self.tree.bind("<Button-3>", self.show_context_menu)
        #Umieszczanie tabeli
        self.tree.grid(row=6, columnspan=2, pady=10)

    
    def run(self):
        """
        Main Loop GUI i app
        """
        #Przed uruchomieniem petli wyswietlamy poczatkowe wartosci
        self.update_combobox_options()
        self.update_tree()
        self.root.mainloop()
        
    def update_combobox_options(self):
        """
        Odswieraza wyswietlanie typow Czesci w wyborze formularza
        """
        self.combobox_typ["values"] = self.typy
    
    
    def update_tree(self):
        """
        Odswieza wyswietlanie danych w tabeli
        """
        # Usunięcie istniejących wierszy z Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Wstawienie nowych danych do Treeview
        for czesc in self.czesci:
            self.tree.insert("", "end", values=czesc.replace("None","-").split(","))       
        
    def dane_z_formularza(self):
        """
        Pobiera i zwraca wpisane dane z formularza

        Returns:
        dane (list): dane z formularza
        """
        dane = []
        dane.append(self.z_entry_nazwa.get())
        dane.append(self.combobox_typ.current()+1)
        dane.append(self.z_entry_parametr1.get())
        dane.append(self.z_entry_parametr2.get())
        dane.append(self.z_entry_parametr3.get())
        return dane
    
    def show_context_menu(self, event):
        """
        Wyswietla menu kontekstowe po nacisnieciu prawego (Button-3) przycisku myszy w miejscu klikniecia
        """
        #Wybrany element
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            #wybrana kolumna
            self.wybrna_kol = self.tree.identify_column(event.x)
            #wyswietl menu
            self.context_menu.post(event.x_root, event.y_root)

    def show_combobox_dialog(self, title: str, values: list):
        """
        Tworzy wyskakujace okienko z comboboxem wyboru Typu czesci

        Args:
        title (str): tytul okienka
        values (list): wartosci do comboboxa

        Returns:
            wybor(int): id wyboru uzytkownika
        """
        #Tworzy wyskakujace okienko (self.root to "okno-rodzic")
        dialog = Dialog_zmiana_typu(self.root, title, values)
        wybor = dialog.result
        return wybor

#nowa klasa dla wyskakujacego okienka            
class Dialog_zmiana_typu(simpledialog.Dialog):
    #konstruktor
    def __init__(self, parent, title, values):
        self.values = values
        self.result = None
        super().__init__(parent, title)

    #co zawierac bedzie okno - nadpisujemy metode wbudowana w klase
    def body(self, master):
        self.combobox = ttk.Combobox(master, values=self.values)
        self.combobox.pack(pady=10)
        return master

    #funkcja przy wcisniciu ok - wlasna metoda
    def ok_pressed(self):
        self.result = self.combobox.current()+1
        self.destroy()

    #Funkcja przy wcisnieciu cancel - wlasna metoda
    def cancel_pressed(self):
        self.destroy()

    #Obsluga przciskow okna - nadpisujemy metode wbudowana w klase
    def buttonbox(self):
        self.ok_button = tk.Button(self, text='Ok', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        #obsluga wcisniecia Enter i Escape
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())          


#testowanie wygladu GUI
if __name__ == "__main__":
    app = SimpleUI()
    app.run()
