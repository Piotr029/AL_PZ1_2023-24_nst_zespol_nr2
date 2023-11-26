import socket
import pickle
from tkinter.simpledialog import askstring
import tkinter.messagebox

VERSION = 1.1

HEADER = 4
FORMAT = 'utf-8'
ROZLACZ = '!Out'
DL_POTWIERDZENIA = 3
OK = "!OK"
SEPARATOR = "/"

def zakoduj_txt(txt: str):
    msg = txt.encode(FORMAT)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' '*(HEADER-len(msg_length))
    return msg, msg_length

def zakoduj_dane(dane: list):
    msg = pickle.dumps(dane)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' '*(HEADER-len(msg_length))
    return msg, msg_length

def odbierz_dane(con: socket.socket):
    msg_length = int(con.recv(HEADER).decode(FORMAT))
    msg = con.recv(msg_length)
    dane = pickle.loads(msg)
    return dane
    

def blad_przesylu():
    print(["BLAD PRZESYLU"])

def pobierz_Typy_Czesci(klient: socket.socket):
    txt = "GET/TYPY_CZESCI/ALL"
    typy = []
    msg, msg_length = zakoduj_txt(txt)
    klient.send(msg_length)
    klient.send(msg)
    potwiedzenie = klient.recv(DL_POTWIERDZENIA).decode(FORMAT)
    if potwiedzenie != OK: blad_przesylu()
    if potwiedzenie == OK:
        print('[MSG-OK] Przesłano Prawidlowo')
        dane = odbierz_dane(klient)
    for linia in dane:
        txt = str(linia).split(',')
        typy.append(f"{txt[1]}-{txt[2]}")
    return typy

def dodaj_czesc(klient: socket.socket, dane_f):
    txt = "POST/CZESCI/ "
    msg, msg_length = zakoduj_txt(txt)
    klient.send(msg_length)
    klient.send(msg)
    potwiedzenie = klient.recv(DL_POTWIERDZENIA).decode(FORMAT)
    if potwiedzenie != OK: blad_przesylu()    
    dane, dane_length = zakoduj_dane(dane_f)
    klient.send(dane_length)
    klient.send(dane)
    nowe_dane = odbierz_dane(klient)
    return nowe_dane

def usun_czesc(klient, ui):
    confirmed = tkinter.messagebox.askyesno("Potwierdzenie usunięcia", "Czy na pewno chcesz usunąć ten wiersz danych?")
    if confirmed:
        id = ui.tree.item(ui.tree.selection(),"values") [0]
        txt = f"DEL/CZESCI/{id}"
        msg, msg_length = zakoduj_txt(txt)
        klient.send(msg_length)
        klient.send(msg)
        potwiedzenie = klient.recv(DL_POTWIERDZENIA).decode(FORMAT)
        if potwiedzenie != OK: blad_przesylu()
        ui.czesci = odbierz_dane(klient)
        ui.update_tree()
    
def zmien_czesc(klient, ui):
    selected_item = ui.tree.selection()
    if selected_item:
        # Pobranie wartości zaznaczonego elementu
        selected_value = ui.tree.item(selected_item, 'values')
        # Wywołanie okna dialogowego do wprowadzenia nowej wartości
        nazwa_kolumny = ui.tree.column(ui.wybrna_kol, 'id')
        index_kol = int(ui.wybrna_kol.lstrip("#"))
        id = selected_value[0]
        if nazwa_kolumny == 'Typ':  # Jeżeli kolumna to 'Typ', użyj Combobox
            new_value = ui.show_combobox_dialog("Zmiana wartości", ui.typy)
        else:
            new_value = askstring("Zmiana wartości", f"Wprowadź nową zawartość dla {nazwa_kolumny}:", initialvalue=selected_value[int(index_kol-1)])
        # Aktualizacja wartości w Treeview
        if new_value is not None:
            txt = f"UPDT/CZESCI/{id},{nazwa_kolumny},{new_value}"
            msg, msg_length = zakoduj_txt(txt)
            klient.send(msg_length)
            klient.send(msg)
            potwiedzenie = klient.recv(DL_POTWIERDZENIA).decode(FORMAT)
            if potwiedzenie != OK: blad_przesylu()
            ui.czesci = odbierz_dane(klient)
            ui.update_tree()
                
    


def pobierz_czesci(klient: socket.socket):
    txt = 'GET/CZESCI/ALL'
    msg, msg_length = zakoduj_txt(txt)
    klient.send(msg_length)
    klient.send(msg)
    potwiedzenie = klient.recv(DL_POTWIERDZENIA).decode(FORMAT)
    if potwiedzenie != OK: blad_przesylu()
    if potwiedzenie == OK:
        print('[MSG-OK] Przesłano Prawidlowo')
        dane = odbierz_dane(klient)
    return dane
