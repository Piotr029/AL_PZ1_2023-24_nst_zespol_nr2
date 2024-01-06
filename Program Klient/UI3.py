import tkinter as tk
from tkinter import ttk, Menu
import sv_ttk

from tkinter import ttk
from tkcalendar import Calendar

# Klasa dla modułu Magazyn
class WarehouseModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Tworzenie stylu
        style = ttk.Style()
        #style.configure("Custom.Treeview.Heading", font=('Calibri', 20, 'bold'), background="#A3A3A3", foreground="black")
        style.configure("Warehouse.TButton", font=('Calibri', 20, 'bold'), background="#4F7942", foreground="white")

        # Konfiguracja rozmiarów wierszy i kolumn
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela z aktualnym stanem magazynowym
        columns = ('ID', 'Czesc', 'Ilosc', 'Pokoj', 'Lokalizacja')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Konfiguracja przewijania tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # Przyciski i pole wyszukiwania
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        ttk.Button(control_frame, text="Dodaj", style="Accent.TButton").pack(side='left')
        ttk.Button(control_frame, text="Usuń", style="Accent.TButton").pack(side='left',padx=10)
        ttk.Button(control_frame, text="Edytuj", style="Accent.TButton").pack(side='left')

        # Pole wyszukiwania
        search_label = ttk.Label(control_frame, text="Wyszukaj: ")
        search_label.pack(side='left',  padx=10, pady=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(control_frame, text="Szukaj", style="Accent.TButton").pack(side='left')



# Klasa dla modułu Katalog Części
class PartsCatalogModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Stosowanie tego samego stylu co w WarehouseModule
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=('Calibri', 10, 'bold'), background="#6A5ACD", foreground="white")

        # Konfiguracja rozmiarów wierszy i kolumn dla responsywności
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela z listą części
        columns = ('id', 'nazwa', 'typ', 'cena', 'parametr1', 'parametr2', 'parametr3')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Konfiguracja przewijania tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # Przyciski do zarządzania katalogiem części
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        ttk.Button(control_frame, text="Dodaj", style="Accent.TButton").pack(side='left')
        ttk.Button(control_frame, text="Usuń", style="Accent.TButton").pack(side='left',padx=10)
        ttk.Button(control_frame, text="Edytuj", style="Accent.TButton").pack(side='left')

        # Pole wyszukiwania
        search_label = ttk.Label(control_frame, text="Wyszukaj: ")
        search_label.pack(side='left',  padx=10, pady=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(control_frame, text="Szukaj", style="Accent.TButton").pack(side='left')

        # Tutaj można dodać logikę do ładowania danych do tabeli, obsługi przycisków itp.


# Klasa dla modułu Terminarz Napraw

class RepairScheduleModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Stylizowanie przycisków i nagłówków tabeli
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=('Calibri', 10, 'bold'), background="#A3A3A3", foreground="black")
        style.configure("Custom.TButton", font=('Calibri', 10, 'bold'), background="#4F7942", foreground="white")

        # Konfiguracja responsywności layoutu
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)  # Tabela ma większy priorytet
        self.grid_columnconfigure(1, weight=1)  # Kalendarz ma mniejszy priorytet

        # Tabela z informacjami o naprawach
        columns = ('id_maszyny', 'serwisant', 'data_przegladu', 'data_naprawy', 'stan_maszyny')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Konfiguracja przewijania tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

       # Widget kalendarza
        self.calendar = Calendar(self, selectmode='day')
        self.calendar.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # Przyciski do zarządzania terminarzem napraw
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10, pady=10)
        ttk.Button(btn_frame, text="Dodaj", style="Accent.TButton").pack(side='left')
        ttk.Button(btn_frame, text="Edytuj", style="Accent.TButton").pack(side='left',padx=10)
        ttk.Button(btn_frame, text="Usuń", style="Accent.TButton").pack(side='left')

        # Dodatkowa logika (np. ładowanie danych, obsługa zdarzeń przycisków) powinna być tutaj

# Klasa dla modułu Raporty
class ReportsModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Stylizowanie przycisków
        style = ttk.Style()
        style.configure("Custom.TButton", font=('Calibri', 10, 'bold'), background="#4F7942", foreground="white")

        # Konfiguracja responsywności layoutu
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Przestrzeń na raporty i statystyki
        # Tutaj możesz dodać widgety, takie jak Canvas czy Text, do wyświetlania raportów

        # Przyciski do zarządzania raportami
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        ttk.Button(btn_frame, text="Generuj raport", style="Accent.TButton").pack(side='left')
        ttk.Button(btn_frame, text="Eksportuj do PDF", style="Accent.TButton").pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Eksportuj do Excel", style="Accent.TButton").pack(side='left')

        # Tutaj można dodać dodatkową logikę, np. generowanie raportów, eksportowanie danych itp.
# Klasa dla modułu Zadania
class TasksModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Stylizowanie przycisków
        style = ttk.Style()
        style.configure("Custom.TButton", font=('Calibri', 10, 'bold'), background="#4F7942", foreground="white")

        # Konfiguracja responsywności layoutu
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela z zadaniami
        columns = ('nazwa_zadania', 'termin_wykonania', 'waznosc_zadania')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Konfiguracja przewijania tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

       # Przyciski do zarządzania zadaniami
        btn_frame = ttk.Frame(self)  # Ramka dla przycisków
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)  # Dodanie ramki do głównego układu klasy

        ttk.Button(btn_frame, text="Dodaj zadanie", style="Accent.TButton").pack(side='left')
        ttk.Button(btn_frame, text="Edytuj zadanie", style="Accent.TButton").pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Usuń zadanie", style="Accent.TButton").pack(side='left')
        # Tutaj można dodać dodatkową logikę, np. obsługę przycisków i zarządzanie danymi zadania

# Funkcje do wyświetlania poszczególnych modułów
##
#
#
def show_module(module_class):
    for widget in main_frame.winfo_children():
        widget.destroy()
    module_instance = module_class(main_frame)
    module_instance.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

# Główne okno aplikacji
root = tk.Tk()
root.title("Aplikacja Zarządzania Magazynem")
root.geometry("1600x800")  # Ustawienie rozmiaru okna


# Stylowanie aplikacji przy użyciu sv_ttk
sv_ttk.set_theme("light")

# Menu główne
menu_bar = Menu(root)
root.config(menu=menu_bar)

# ... (tutaj dodaj pozycje menu)
# Menu użytkownika
user_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Użytkownik", menu=user_menu)
user_menu.add_command(label="Właściciel")
user_menu.add_command(label="Kierownik")
user_menu.add_command(label="Automatyk")

# Menu widoku

def set_light_theme():
    sv_ttk.set_theme("light")

def set_dark_theme():
    sv_ttk.set_theme("dark")
view_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Widok", menu=view_menu)
theme_menu = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Motyw", menu=theme_menu)
theme_menu.add_command(label="Jasny", command=set_light_theme)
theme_menu.add_command(label="Ciemny", command=set_dark_theme)
# Menu pomocy
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Pomoc", menu=help_menu)
help_menu.add_command(label="Pomoc")
help_menu.add_command(label="FAQ")
help_menu.add_command(label="Przewodnik użytkowania")

# Menu konfiguracji
config_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Konfiguracja", menu=config_menu)
config_menu.add_command(label="Połączenie")
# Panel boczny z przyciskami modułów
sidebar = ttk.Frame(root)
sidebar.pack(side="left", fill="y")

# Główny kontener dla modułów
main_frame = ttk.Frame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Przyciski w panelu bocznym
ttk.Button(sidebar, text="Magazyn", command=lambda: show_module(WarehouseModule)).pack(fill="x")
ttk.Button(sidebar, text="Katalog Części", command=lambda: show_module(PartsCatalogModule)).pack(fill="x")
ttk.Button(sidebar, text="Terminarz Napraw", command=lambda: show_module(RepairScheduleModule)).pack(fill="x")
ttk.Button(sidebar, text="Raporty", command=lambda: show_module(ReportsModule)).pack(fill="x")
ttk.Button(sidebar, text="Zadania", command=lambda: show_module(TasksModule)).pack(fill="x")
###########################################################################################################
##
###########################################################################################################
def szukaj_w_tabeli_magazyn(self):
       """"
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

# Uruchomienie głównej pętli aplikacji
root.mainloop()
