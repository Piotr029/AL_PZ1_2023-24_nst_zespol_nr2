import tkinter as tk
from tkinter import ttk, Menu, filedialog 
import sv_ttk
import csv
from tkinter import ttk
from tkcalendar import Calendar
from ttkthemes import ThemedTk
import funkcje
import klient 

def initialize_styles():
    style = ttk.Style()
    # Definiowanie stylu dla przycisków
    style.configure("Sidebar.TButton", font=('Calibri', 12), padding=5)
    style.map("Sidebar.TButton", background=[('active', 'lightblue')], foreground=[('active', 'black')])
def change_theme(root, theme):
    root.set_theme(theme)
####################################################################################
class WarehouseModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.klient = klient
        # Konfiguracja rozmiarów wierszy i kolumn dla responsywności
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Tabela z aktualnym stanem magazynowym
        self.create_warehouse_table()
        # Panel sterowania z przyciskami i polem wyszukiwania
        self.create_control_panel()

    def create_warehouse_table(self):
        columns = ('ID', 'Czesc', 'Ilosc', 'Pokoj', 'Lokalizacja')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky='nsew')
        # Konfiguracja przewijania tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
    def create_control_panel(self):
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        # Przyciski do zarządzania zawartością magazynu
        ttk.Button(control_frame, text="Dodaj", style="Sidebar.TButton", command=self.add_item).pack(side='left')
        ttk.Button(control_frame, text="Usuń", style="Sidebar.TButton", command=self.remove_item).pack(side='left', padx=10)
        ttk.Button(control_frame, text="Edytuj", style="Sidebar.TButton", command=self.edit_item).pack(side='left')
        # Pole wyszukiwania
        search_label = ttk.Label(control_frame, text="Wyszukaj: ")
        search_label.pack(side='left', padx=10, pady=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        #ttk.Button(control_frame, text="Szukaj", style="Accent.TButton", command=self.search_item).pack(side='left')
    # Metody do obsługi zdarzeń przycisków (szkielety)
    def update_warehouse_table(self):
        self.stan_magazynu = funkcje.pobierz_stan_magazynu(self.klient)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.stan_magazynu:
            self.tree.insert("", "end", values=item)
    def add_item(self):
        new_item_window = tk.Toplevel(self)
        new_item_window.title("Dodaj Nowy Przedmiot")

        labels = ['Część', 'Ilość', 'Pokój', 'Lokalizacja']
        entries = {}

        for i, label in enumerate(labels):
            ttk.Label(new_item_window, text=label + ":").grid(row=i, column=0)
            entry = ttk.Entry(new_item_window)
            entry.grid(row=i, column=1)
            entries[label] = entry

        submit_button = ttk.Button(new_item_window, text="Dodaj",
                                   command=lambda: self.submit_new_item(entries, new_item_window))
        submit_button.grid(row=len(labels), column=0, columnspan=2)

    def submit_new_item(self, entries, window):
        nowy_przedmiot = {label: entry.get() for label, entry in entries.items()}
        funkcje.dodaj_czesc(self.klient, nowy_przedmiot)
        window.destroy()
        self.update_warehouse_table()

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item, "values")[0]
            funkcje.usun_czesc(self.klient, item_id)
            self.update_warehouse_table()
    def edit_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Pobieranie wartości z zaznaczonego wiersza
            item_values = self.tree.item(selected_item, "values")
            edit_item_window = tk.Toplevel(self)
            edit_item_window.title("Edytuj Przedmiot")

            labels = ['ID', 'Część', 'Ilość', 'Pokój', 'Lokalizacja']
            entries = {}

            for i, label in enumerate(labels):
                ttk.Label(edit_item_window, text=label + ":").grid(row=i, column=0)
                entry = ttk.Entry(edit_item_window)
                entry.grid(row=i, column=1)
                if i < len(item_values):
                    entry.insert(0, item_values[i])
                entry.configure(state='readonly' if label == 'ID' else 'normal')  # ID jest nieedytowalne
                entries[label] = entry

            submit_button = ttk.Button(edit_item_window, text="Zatwierdź",
                                       command=lambda: self.submit_edit_item(entries, edit_item_window))
            submit_button.grid(row=len(labels), column=0, columnspan=2)

    def submit_edit_item(self, entries, window):
        zmienione_dane = {label: entry.get() for label, entry in entries.items() if label != 'ID'}
        item_id = entries['ID'].get()
        funkcje.popraw_nz_w_magazynie(self.klient, item_id, zmienione_dane)
        window.destroy()
        self.update_warehouse_table()

""" def search_item(self):
        search_query = self.search_var.get()
        if search_query:
            # Wysyłanie zapytania do serwera
            wyniki_wyszukiwania = funkcje.wyszukaj_w_magazynie(self.klient, search_query)
            # Wyczyszczenie obecnych danych w tabeli
            for row in self.tree.get_children():
                self.tree.delete(row)
            # Wypełnienie tabeli wynikami wyszukiwania
            for item in wyniki_wyszukiwania:
                self.tree.insert("", "end", values=item)
        else:
            # Jeśli pole wyszukiwania jest puste, odśwież tabelę
            self.update_warehouse_table()"""
#################################################################################################
class PartsCatalogModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tworzenie tabeli do wyświetlania danych części
        self.create_parts_table()

        # Tworzenie panelu kontrolnego z przyciskami
        self.create_control_panel()

    def create_parts_table(self):
        columns = ('ID', 'Nazwa', 'Typ', 'Cena', 'Parametr1', 'Parametr2', 'Parametr3')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Dodanie paska przewijania
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

    def create_control_panel(self):
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        # Przyciski do zarządzania katalogiem części
        ttk.Button(control_frame, text="Dodaj", style="Accent.TButton", command=self.add_part).pack(side='left')
        ttk.Button(control_frame, text="Edytuj", style="Accent.TButton", command=self.edit_part).pack(side='left', padx=10)
        ttk.Button(control_frame, text="Usuń", style="Accent.TButton", command=self.delete_part).pack(side='left')

    def add_part(self):
        # Logika dla dodawania nowej części
        pass

    def edit_part(self):
        # Logika dla edycji istniejącej części
        pass

    def delete_part(self):
        # Logika dla usuwania części
        pass

    # Możesz dodać dodatkowe metody, które będą obsługiwać funkcjonalności jak wyszukiwanie, eksport danych itp.
###################################################################################################################


class TasksModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela z zadaniami
        self.create_tasks_table()

        # Panel kontrolny z przyciskami i formularzem do dodawania zadań
        self.create_control_panel()

    def create_tasks_table(self):
        columns = ('Nazwa Zadania', 'Opis','Termin Wykonania', 'Priorytet')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Pasek przewijania dla tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

    def create_control_panel(self):
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        # Przyciski do zarządzania zadaniami
        ttk.Button(control_frame, text="Dodaj Zadanie", style="Accent.TButton", command=self.add_task).pack(side='left')
        ttk.Button(control_frame, text="Edytuj Zadanie", style="Accent.TButton", command=self.edit_task).pack(side='left', padx=10)
        ttk.Button(control_frame, text="Usuń Zadanie", style="Accent.TButton", command=self.delete_task).pack(side='left')

        # Formularz do dodawania nowych zadań
        self.task_name_var = tk.StringVar()
        self.task_deadline_var = tk.StringVar()
        self.task_priority_var = tk.StringVar()

        ttk.Entry(control_frame, textvariable=self.task_name_var).pack(side='left', padx=5)
        ttk.Entry(control_frame, textvariable=self.task_deadline_var).pack(side='left', padx=5)
        ttk.Entry(control_frame, textvariable=self.task_priority_var).pack(side='left', padx=5)

    def add_task(self):
        # Logika dodawania nowego zadania
        pass

    def edit_task(self):
        # Logika edycji istniejącego zadania
        pass

    def delete_task(self):
        # Logika usuwania zadania
        pass

    # Możesz dodać dodatkowe metody, które będą obsługiwać funkcjon alności jak wyszukiwanie, eksport danych itp.
##########################################################################################################
    
class RepairScheduleModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabela z terminarzem napraw
        self.create_schedule_table()

        # Panel kontrolny z przyciskami i formularzem do dodawania napraw
        self.create_control_panel()

    def create_schedule_table(self):
        columns = ('ID Maszyny', 'Serwisant', 'Data Przeglądu', 'Data Naprawy', 'Stan Maszyny')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style="Custom.Treeview.Heading")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Pasek przewijania dla tabeli
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

    def create_control_panel(self):
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        # Przyciski do zarządzania terminarzem napraw
        ttk.Button(control_frame, text="Dodaj Naprawę", style="Accent.TButton", command=self.add_repair).pack(side='left')
        ttk.Button(control_frame, text="Edytuj Naprawę", style="Accent.TButton", command=self.edit_repair).pack(side='left', padx=10)
        ttk.Button(control_frame, text="Usuń Naprawę", style="Accent.TButton", command=self.delete_repair).pack(side='left')

        # Formularz do dodawania nowych napraw
        self.machine_id_var = tk.StringVar()
        self.serviceman_var = tk.StringVar()
        self.review_date_var = tk.StringVar()
        self.repair_date_var = tk.StringVar()
        self.machine_status_var = tk.StringVar()

        ttk.Entry(control_frame, textvariable=self.machine_id_var).pack(side='left', padx=5)
        ttk.Entry(control_frame, textvariable=self.serviceman_var).pack(side='left', padx=5)
        ttk.Entry(control_frame, textvariable=self.review_date_var).pack(side='left', padx=5)
        ttk.Entry(control_frame, textvariable=self.repair_date_var).pack(side='left', padx=5)
        ttk.Entry(control_frame, textvariable=self.machine_status_var).pack(side='left', padx=5)

    def add_repair(self):
        # Logika dodawania nowej naprawy
        pass

    def edit_repair(self):
        # Logika edycji istniejącej naprawy
        pass

    def delete_repair(self):
        # Logika usuwania naprawy
        pass

    # Możesz dodać dodatkowe metody, które będą obsługiwać funkcjonalności jak wyszukiwanie, eksport danych itp.
#################################################################################################################
class ReportsModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Panel kontrolny z przyciskami
        self.create_control_panel()

        # Miejsce na wyświetlanie raportów
        self.report_display = tk.Text(self, height=10)
        self.report_display.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

    def create_control_panel(self):
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        # Przyciski do zarządzania raportami
        ttk.Button(control_frame, text="Generuj Raport", style="Accent.TButton", command=self.generate_report).pack(side='left')
        ttk.Button(control_frame, text="Eksportuj do CSV", style="Accent.TButton", command=self.export_to_csv).pack(side='left', padx=10)

    def generate_report(self):
        # Logika generowania raportu
        # Na przykład, możesz tutaj załadować dane i wyświetlić je w 'report_display'
        pass

    def export_to_csv(self):
        # Logika eksportowania danych do CSV
        report_data = self.get_report_data()  # Pobierz dane, które chcesz eksportować
        if not report_data:
            return  # Brak danych do eksportu

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return  # Anulowano zapisywanie pliku

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(report_data)

    def get_report_data(self):
        # Pobierz dane raportu, które chcesz eksportować
        # Ta funkcja powinna zwracać dane w formacie listy list, gdzie każda wewnętrzna lista to wiersz danych
        # Na przykład: [['Nagłówek1', 'Nagłówek2'], ['Dane1', 'Dane2'], ['Dane3', 'Dane4']]
        return [["Przykład", "Danych"], ["Wartość 1", "Wartość 2"], ["Wartość 3", "Wartość 4"]]
############################################################################################################
class Application(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.modules = {}
        self.current_module = None
        initialize_styles()
        self.create_menu(parent)
        self.create_sidebar()
        self.init_modules()

    def create_menu(self, root):
        # Tworzenie głównego menu
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        # Menu użytkownika
        user_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Użytkownik", menu=user_menu)
        user_menu.add_command(label="Właściciel", command=self.user_owner)
        user_menu.add_command(label="Kierownik", command=self.user_manager)
        user_menu.add_command(label="Automatyk", command=self.user_technician)

        # Menu widoku i zmiany motywu
        view_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Widok", menu=view_menu)
        theme_menu = Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Motyw", menu=theme_menu)
        theme_menu.add_command(label="Adapta", command=lambda: change_theme(root, "adapta"))
        theme_menu.add_command(label="Equilux", command=lambda: change_theme(root, "equilux"))

        # Menu pomocy
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Pomoc", menu=help_menu)
        help_menu.add_command(label="O aplikacji", command=self.about)
        help_menu.add_command(label="FAQ", command=self.faq)
        help_menu.add_command(label="Przewodnik użytkowania", command=self.user_guide)

        # Menu konfiguracji
        config_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Konfiguracja", menu=config_menu)
        config_menu.add_command(label="Połączenie", command=self.connection_settings)

    # Funkcje callback dla różnych opcji menu
    def user_owner(self):
        # Logika dla opcji "Właściciel"
        pass

    def user_manager(self):
        # Logika dla opcji "Kierownik"
        pass

    def user_technician(self):
        # Logika dla opcji "Automatyk"
        pass

    def about(self):
        # Wyświetlenie informacji o aplikacji
        pass

    def faq(self):
        # Wyświetlenie FAQ
        pass

    def user_guide(self):
        # Wyświetlenie przewodnika użytkowania
        pass

    def connection_settings(self):
        # Ustawienia połączenia
        pass

   
    def create_sidebar(self):
        sidebar = ttk.Frame(self)
        sidebar.pack(side="left", fill="y", expand=False)

        ttk.Button(sidebar, text="Magazyn", style="Accent.TButton",command=lambda: self.show_module("Magazyn")).pack(fill="x")
        ttk.Button(sidebar, text="Katalog Części", style="Accent.TButton" ,command=lambda: self.show_module("Katalog Części")).pack(fill="x")
        ttk.Button(sidebar, text="Raporty", style="Accent.TButton",command=lambda: self.show_module("Raporty")).pack(fill="x")
        ttk.Button(sidebar, text="Zadania", style="Accent.TButton",command=lambda: self.show_module("Zadania")).pack(fill="x")
        ttk.Button(sidebar, text="Terminarz Napraw", style="Accent.TButton" ,command=lambda: self.show_module("Terminarz Napraw")).pack(fill="x")

    def init_modules(self):
        self.modules["Magazyn"] = WarehouseModule(self)
        self.modules["Katalog Części"] = PartsCatalogModule(self)
        self.modules["Raporty"] = ReportsModule(self)
        self.modules["Zadania"] = TasksModule(self)
        self.modules["Terminarz Napraw"] = RepairScheduleModule(self)

    def show_module(self, module_name):
        if self.current_module:
            self.current_module.pack_forget()
        self.current_module = self.modules[module_name]
        self.current_module.pack(side="right", fill="both", expand=True)


    

def main():
    root = ThemedTk(theme="adapta")  # Wybierz motyw, który wspiera zaokrąglone rogi
    initialize_styles()
    root.title("Aplikacja Zarządzania Magazynem")
    root.geometry("1200x600")
    app = Application(root)
    app.pack(side="right", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
