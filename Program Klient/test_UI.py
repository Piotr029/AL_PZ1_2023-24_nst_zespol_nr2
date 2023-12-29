import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sv_ttk

class SimpleUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplikacja Testowa")
        
        self.uzytkownicy = []
        self.typy = []
        self.czesci = []
        self.miary = []
        self.stan = [] #stan magazynu
        self.hist_zmin_mag = []
        self.wybrna_kol = ""
        
        #Tworzenie dwoch glownych obaszarow
        fr_lewy = tk.Frame(self.root)
        fr_uzytkownika = tk.LabelFrame(fr_lewy, text="Wybierz Uzytkownika")
        fr_menu = tk.LabelFrame(fr_lewy, width=100, text='Menu')
        fr_uzytkownika.grid(row=0, column=0, padx=5, pady=5)
        fr_menu.grid(row=1, column=0, padx=5, pady=5)
        
        fr_roboczy = tk.LabelFrame(self.root, text="'Obszar Roboczy'")
        fr_lewy.grid(row=0, column=0, padx=5, pady=5)
        fr_roboczy.grid(row=0, column=1, padx=5, pady=5)
        
        #Wybor Uzytkownika
        self.wybor_uz = ttk.Combobox(fr_uzytkownika, state='readonly', width=10)
        self.wybor_uz.pack(anchor='center', padx=5, pady=5)
        
        #Menu
        b_magazyn = tk.Button(fr_menu, text="Magazyn", command=self.pokaz_magazyn)
        b_puste = tk.Button(fr_menu, text="Puste", command=self.pokaz_ekran1)
        b_czesci = tk.Button(fr_menu, text = "Katalog Czesci", command=self.pokaz_kat_czesci)
        b_historia_mag = tk.Button(fr_menu, text = 'Historia Zmian w Magazynie', command = self.pokaz_hist_mag)
    
        b_puste. grid(column=0, row=0, padx=5, pady=5)
        b_magazyn.grid(column=0, row=1, padx=5, pady=5)
        b_czesci.grid(column=0, row=2, padx=5, pady=5)
        
        #Pusty Frame - testowy
        self.__fr_pusty = tk.Frame(fr_roboczy, width=500, height=500)
        l_test = tk.Label(self.__fr_pusty, text="Testowy Obszar")
        l_test.pack(anchor='center')
        
        self.__fr_pusty.pack(anchor='center')
##############################################################################################################       
        #Magazyn
##############################################################################################################
        
        self.__fr_magazyn = tk.Frame(fr_roboczy)
        
        
        #Tworzenie tabeli(treeview) do wyswietlania danych z stanem magazynu
        #Deklaracja i tworzenie ile bedzie kolumn - id tych kolumn
        self.tab_magazyn = ttk.Treeview(self.__fr_magazyn, columns=("ID", "Czesc", "Ilosc", "Pokoj", "Lokalizacja")) 
        #nazwy naglowkow kolumn - #0 to kolumna obslugujaca "childy" gdyby byly
        self.tab_magazyn.heading("#0", text="", anchor=tk.CENTER)
        self.tab_magazyn.heading("ID", text="ID", anchor=tk.CENTER)
        self.tab_magazyn.heading("Czesc", text="Część", anchor=tk.CENTER)
        self.tab_magazyn.heading("Ilosc", text="Ilość", anchor=tk.CENTER)
        self.tab_magazyn.heading("Pokoj", text="Pokój", anchor=tk.CENTER)
        self.tab_magazyn.heading("Lokalizacja", text="Lokalizacja", anchor=tk.CENTER)

        #szerokosci kolumn
        self.tab_magazyn.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tab_magazyn.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tab_magazyn.column("Czesc", stretch=tk.NO, minwidth=0, width=150)
        self.tab_magazyn.column("Ilosc", stretch=tk.NO, minwidth=0, width=150)
        self.tab_magazyn.column("Pokoj", stretch=tk.NO, minwidth=0, width=150)
        self.tab_magazyn.column("Lokalizacja", stretch=tk.NO, minwidth=0, width=300)
 
        #Elemnty wyszukiwania
        fr_szukania = tk.Frame(self.__fr_magazyn)
        self.__entry_szukaj = tk.Entry(fr_szukania)
        b_szukaj = tk.Button(fr_szukania, text="Szukaj", command=self.szukaj_w_tabeli_magazyn)
        
        # Stworzenie menu kontekstowego
        self.b3_menu_magazyn = tk.Menu(self.__fr_magazyn, tearoff=0)
        #Przypisanie menu do prawego przycisku myszy w obszarze tabeli
        self.tab_magazyn.bind("<Button-3>", self.show_b3_menu_magazyn)
        
        #Umieszczanie elemntow fr_magazynu
        self.__entry_szukaj.grid(row=0, column=0, padx=5, pady=5)
        b_szukaj.grid(row=0, column=1, padx=5, pady=5)        
        fr_szukania.grid(row = 0, column=0, padx=5, pady=5)
        self.tab_magazyn.grid(row=1, column=0, padx=5, pady=5)
        
#################################################################################################################        
        #Katalog Czesci
##################################################################################################################
        
        self.__fr_czesci = tk.Frame(fr_roboczy)

        # #Tworzenie podstawowych elementow
        # label_nazwa = tk.Label(self.root, text="Nazwa:")
        # self.z_entry_nazwa = tk.Entry(self.root)

        # label_typ = tk.Label(self.root, text="Typ:")
        # self.combobox_typ = ttk.Combobox(self.root, values=self.typy)

        # label_parametr1 = tk.Label(self.root, text="Parametr 1:")
        # self.z_entry_parametr1 = tk.Entry(self.root)

        # label_parametr2 = tk.Label(self.root, text="Parametr 2:")
        # self.z_entry_parametr2 = tk.Entry(self.root)

        # label_parametr3 = tk.Label(self.root, text="Parametr 3:")
        # self.z_entry_parametr3 = tk.Entry(self.root)

        # self.button_dodaj = tk.Button(self.root, text="Dodaj")
        

        # # Umieszczanie podstawowych elementow
        # label_nazwa.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        # self.z_entry_nazwa.grid(row=0, column=1, padx=10, pady=5)

        # label_typ.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        # self.combobox_typ.grid(row=1, column=1, padx=10, pady=5)

        # label_parametr1.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        # self.z_entry_parametr1.grid(row=2, column=1, padx=10, pady=5)

        # label_parametr2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        # self.z_entry_parametr2.grid(row=3, column=1, padx=10, pady=5)

        # label_parametr3.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        # self.z_entry_parametr3.grid(row=4, column=1, padx=10, pady=5)

        # self.button_dodaj.grid(row=5, columnspan=2, pady=10)
        
        #Tworzenie tabeli(treeview) do wyswietlania danych z czesciami
        #Deklaracja i tworzenie ile bedzie kolumn - id tych kolumn
        self.tab_czesci = ttk.Treeview(self.__fr_czesci, columns=("ID", "Nazwa", "Typ", "Parametr1", "Parametr2", "Parametr3"))
        #nazwy naglowkow kolumn - #0 to kolumna obslugujaca "childy" gdyby byly
        self.tab_czesci.heading("#0", text="", anchor=tk.W)
        self.tab_czesci.heading("ID", text="ID", anchor=tk.W)
        self.tab_czesci.heading("Nazwa", text="Nazwa", anchor=tk.W)
        self.tab_czesci.heading("Typ", text="Typ", anchor=tk.W)
        self.tab_czesci.heading("Parametr1", text="Parametr 1", anchor=tk.W)
        self.tab_czesci.heading("Parametr2", text="Parametr 2", anchor=tk.W)
        self.tab_czesci.heading("Parametr3", text="Parametr 3", anchor=tk.W)
        #szerokosci kolumn
        self.tab_czesci.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tab_czesci.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tab_czesci.column("Nazwa", stretch=tk.NO, minwidth=0, width=150)
        self.tab_czesci.column("Typ", stretch=tk.NO, minwidth=0, width=150)
        self.tab_czesci.column("Parametr1", stretch=tk.NO, minwidth=0, width=100)
        self.tab_czesci.column("Parametr2", stretch=tk.NO, minwidth=0, width=100)
        self.tab_czesci.column("Parametr3", stretch=tk.NO, minwidth=0, width=100)
        
        #Umieszczanie elemntow fr_czesci
        self.tab_czesci.grid(row=0, column=0, padx=5, pady=5)
        
#################################################################################################################        
        #Historia zmian w magazynie
##################################################################################################################
        
        self.__fr_hitoria_mag = tk.Frame(fr_roboczy)
        
        #Tworzenie tabeli z danymi
        self.tab_hitoria_mag = ttk.Treeview(self.__fr_hitoria_mag, columns=("ID", "Czesc", "Pokoj", "Lokalizacja", "Data_Zmiany", "Rodzaj_Zmiany", "Dokonal", "Info"))
        #Tworzenie naglowkow tabeli
        self.tab_hitoria_mag.heading("#0", text="", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("ID", text="ID", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Czesc", text="Część", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Pokoj", text="Pokój", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Lokalizacja", text="Lokalizacja", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Data_Zmiany", text="Data Zmiany", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Rodzaj_Zmiany", text="Rodzaj Zmiany", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Dokonal", text="Dokonał", anchor=tk.CENTER)
        self.tab_hitoria_mag.heading("Info", text="Info", anchor=tk.CENTER)
        #szerokosci kolumn
        self.tab_hitoria_mag.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.tab_hitoria_mag.column("ID", stretch=tk.NO, minwidth=0, width=50)
        self.tab_hitoria_mag.column("Czesc",  stretch=tk.NO, minwidth=0, width=150)
        self.tab_hitoria_mag.column("Pokoj",  stretch=tk.NO, minwidth=0, width=150)
        self.tab_hitoria_mag.column("Lokalizacja",  stretch=tk.NO, minwidth=0, width=150)
        self.tab_hitoria_mag.column("Data_Zmiany",  stretch=tk.NO, minwidth=0, width=100)
        self.tab_hitoria_mag.column("Rodzaj_Zmiany",  stretch=tk.NO, minwidth=0, width=100)
        self.tab_hitoria_mag.column("Dokonal",  stretch=tk.NO, minwidth=0, width=100)
        self.tab_hitoria_mag.column("Info",  stretch=tk.NO, minwidth=0, width=150)
        
        #Umieszczanie elemntow fr_czesci
        self.tab_hitoria_mag.grid(row=0, column=0, padx=5, pady=5)        
        
        
        
        sv_ttk.set_theme("light") 
    #Koniec konstruktora/ Paczatek metod
    
    def run(self):
        """
        Main Loop GUI i app
        """
        #Przed uruchomieniem petli wyswietlamy poczatkowe wartosci
        self.update_uzytkownicy()
        self.root.mainloop()
    
    def update_uzytkownicy(self):
        self.wybor_uz.config(values=self.uzytkownicy)
        
    def ukryj_widoki(self):
        self.__fr_pusty.forget()
        self.__fr_magazyn.grid_forget()
        self.__fr_czesci.grid_forget()
        self.__fr_hitoria_mag.grid_forget()
        
    def pokaz_ekran1(self):
        self.ukryj_widoki()
        self.__fr_pusty.pack(anchor='center')
################################################################################################################
    #Metody zwiazne z ekranem Magazyn
################################################################################################################        
    def pokaz_magazyn(self):
        self.ukryj_widoki()
        self.update_tabela_magazyn()
        self.__fr_magazyn.grid(row=0, column=0, padx=5, pady=5)
        
    def update_tabela_magazyn(self):
        """
        Odswieza wyswietlanie danych w tabeli magazynu
        """
        # Usunięcie istniejących wierszy z Treeview
        for row in self.tab_magazyn.get_children():
            self.tab_magazyn.delete(row)

        # Wstawienie nowych danych do Treeview
        for czesc in self.stan:
            self.tab_magazyn.insert("", "end", values=czesc.replace("None","-").split(",")) 

    def show_b3_menu_magazyn(self, event):
        """
        Wyswietla menu kontekstowe po nacisnieciu prawego (Button-3) przycisku myszy w miejscu klikniecia
        """
        #Wybrany element
        item = self.tab_magazyn.identify_row(event.y)
        if item:
            self.tab_magazyn.selection_set(item)
            #wybrana kolumna
            self.wybrna_kol = self.tab_magazyn.identify_column(event.x)
            #wyswietl menu
            self.b3_menu_magazyn.post(event.x_root, event.y_root)
                    
    def szukaj_w_tabeli_magazyn(self):
        """
        Funkcja wyszukiwania danych w tabeli
        """
        self.update_tabela_magazyn()
        szukane = self.__entry_szukaj.get().lower()
        znalezione = []
        #Przypisz znalezlione dane
        for row_id in self.tab_magazyn.get_children():
            czesc = self.tab_magazyn.item(row_id)
            if szukane in czesc['values'][1].lower():  # Szukaj po nazwie części (kolumna "Czesc")
                znalezione.append(czesc["values"])
        #Ukryj dane tabeli
        for row in self.tab_magazyn.get_children():
            self.tab_magazyn.delete(row)
        #Pokaz tylko znalezione dane
        for czesc in znalezione:
            self.tab_magazyn.insert("", "end", values=czesc)
            
    def show_Dialog_poprawa_ilosci(self, title: str, wrt_obecna:str, miara_obecna:str, values: list):
        """
        Tworzy wyskakujace okienko z comboboxem wyboru Typu czesci

        Args:
        title (str): tytul okienka
        values (list): wartosci do comboboxa

        Returns:
            wybor(int): id wyboru uzytkownika
        """
        #Tworzy wyskakujace okienko (self.root to "okno-rodzic")
        dialog = Dialog_poprawa_ilosci(self.root, title, wrt_obecna, miara_obecna, values)
        zmiana = dialog.result
        return zmiana 
    
################################################################################################################
    #Metody zwiazne z ekranem Historia Zmian w Magazynie
################################################################################################################ 

    def pokaz_hist_mag(self):
        self.ukryj_widoki()
        self.update_tabela_hitoria_mag()
        self.__fr_hitoria_mag.grid(row=0, column=0, padx=5, pady=5)
        
    def update_tabela_hitoria_mag(self):
        """
        Odswieza wyswietlanie danych w tabeli histira zmian magazynu
        """
        # Usunięcie istniejących wierszy z Treeview
        for row in self.tab_hitoria_mag.get_children():
            self.tab_hitoria_mag.delete(row)
        
        # Wstawienie nowych danych do Treeview
        for linia in self.hist_zmin_mag:
            self.tab_hitoria_mag.insert("", "end", values=linia.replace("None","-").split(","))
               
            
################################################################################################################
    #Metody zwiazne z ekranem Katalog Czesci
################################################################################################################        

    def pokaz_kat_czesci(self):
        self.ukryj_widoki()
        self.update_tabela_czesci()
        self.__fr_czesci.grid(row=0, column=0, padx=5, pady=5)
        
    def update_tabela_czesci(self):
        """
        Odswieza wyswietlanie danych w tabeli czesci
        """
        # Usunięcie istniejących wierszy z Treeview
        for row in self.tab_czesci.get_children():
            self.tab_czesci.delete(row)

        # Wstawienie nowych danych do Treeview
        for czesc in self.czesci:
            self.tab_czesci.insert("", "end", values=czesc.replace("None","-").split(","))       
                                 
    def update_combobox_options(self):
        """
        Odswieraza wyswietlanie typow Czesci w wyborze formularza
        """
        self.combobox_typ["values"] = self.typy
    
 
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
        item = self.tab_czesci.identify_row(event.y)
        if item:
            self.tab_czesci.selection_set(item)
            #wybrana kolumna
            self.wybrna_kol = self.tab_czesci.identify_column(event.x)
            #wyswietl menu
            self.b3_menu_czesci.post(event.x_root, event.y_root)
            

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

#nowa klasa dla wyskakujacego okienka dla poprawy ilosci ilosci           
class Dialog_poprawa_ilosci(simpledialog.Dialog):
    #konstruktor
    def __init__(self, parent, title, v_pocztkowe, m_pocztkowa, miary):
        self.wartosc = v_pocztkowe
        self.p_miara = m_pocztkowa
        self.miary = miary
        self.result = None
        super().__init__(parent, title)

    #co zawierac bedzie okno - nadpisujemy metode wbudowana w klase
    def body(self, master):
        self.combobox = ttk.Combobox(master, values=self.miary, state='readonly')
        self.combobox.set(self.combobox['values'][self.p_miara])
        self.entry = tk.Entry(master)
        self.entry.insert(0, self.wartosc)
        self.entry.pack(padx=5, pady=10, side="left")
        self.combobox.pack(padx=5, pady=10, side="right")
        return master

    #funkcja przy wcisniciu ok - wlasna metoda
    def ok_pressed(self):
        self.result = (f"{self.entry.get()},{self.combobox.current()+1}")
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
