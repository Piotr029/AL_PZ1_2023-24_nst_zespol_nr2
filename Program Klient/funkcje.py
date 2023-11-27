import socket
import pickle as pck
from tkinter.simpledialog import askstring
import tkinter.messagebox

VERSION = 1.15

HEADER = 4
FORMAT = 'utf-8'
ROZLACZ = '!Out'
DL_POTWIERDZENIA = 3
OK = "!OK"
SEPARATOR = "/"

def zakoduj_txt(txt: str):
    """
    Funkcja zamieniajaca wysylana wiadmosc z postaci str na postac bytes oraz przygtowujaca dl wiadomosci w bytes

    Args:
    txt (str): wiadmosc do wyslania w postaci str

    Returns:
    msg(bytes): wiadmosc do wyslania w postaci bytes
    msg_length (bytes): dlugosc wiadomosci w bytes
    """
    msg = txt.encode(FORMAT)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' '*(HEADER-len(msg_length))
    return msg, msg_length

def wyslij_msg(klient: socket.socket, txt: str):
    """
    Funkcja wysylajaca wiadomosc z poleceniem do serwera

    Args:
    klient (socket.socket): polaczenie z serwerem
    txt (str): tresc polecenia do serwera
    """
    msg, msg_length = zakoduj_txt(txt)
    klient.send(msg_length)
    klient.send(msg)
    potwiedzenie = klient.recv(DL_POTWIERDZENIA).decode(FORMAT)
    #Tu kiedys bedzie obsluga bledu przesylu
    if potwiedzenie != OK: blad_przesylu()
    if potwiedzenie == OK: print(f'[MSG-OK] Przesłano Prawidlowo: {txt}')
    

def zakoduj_dane(dane: list):
    """
    Funkcja picklujaca dane, zamienia np listy, obiekty itd na forme bytowa, zachowujaca strukture

    Args:
    dane (list): dane do wyslanai

    Returns:
    msg(bytes): dane w formie bytes
    msg_length(bytes): dlugosc wiadomosci w bytes
    """
    msg = pck.dumps(dane)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' '*(HEADER-len(msg_length))
    return msg, msg_length

def odbierz_dane(con: socket.socket):
    """
    Funkcja odbierajac dane z bazy danych i odpickulowuje je z powrotem na format listy

    Args:
    con (socket.socket): poloczenie z serwerem

    Returns:
    dane(list): dane z bazy danych w fomie listy
    """
    msg_length = int(con.recv(HEADER).decode(FORMAT))
    msg = con.recv(msg_length)
    dane = pck.loads(msg)
    return dane
    

def blad_przesylu():
    """
    Tu bedzie obsluga bledu przesylu
    """
    print(["BLAD PRZESYLU"])

def pobierz_Typy_Czesci(con: socket.socket):
    """
    Pobiera wszystkie elementy z tabeli Typy_Czesci 

    Args:
    con (socket.socket): poloczenie z serwerem

    Returns:
    typy(list): lista typow czesci w postaci "Kategoria-Podkategoria"
    """
    msg = "GET/TYPY_CZESCI/ALL"
    typy = []
    wyslij_msg(con, msg)
    dane = odbierz_dane(con)
    for linia in dane:
        txt = str(linia).split(',')
        typy.append(f"{txt[1]}-{txt[2]}")
    return typy


def dodaj_czesc(con: socket.socket, ui):
    """
    Funkcja dodawnia elementu do Tabeli Czesci

    Args:
    con (socket.socket): poloczenie z serwerem
    ui (Ui): GUI programu
    """
    #Pobieramy dane z formalarza 
    nowa_czesc = ui.dane_z_formularza()
    #3 czlon " " pusty bo zaraz po nim wysylamy dane dodawanej czesci
    msg = "POST/CZESCI/ "
    wyslij_msg(con, msg)   
    dane, dane_length = zakoduj_dane(nowa_czesc)
    con.send(dane_length)
    con.send(dane)
    #Przypisujemy zaktualizowane dane do zmiennej w ui
    ui.czesci = odbierz_dane(con)
    #Aktualizujemy wyswietlanie zawartosci tabeli
    ui.update_tree()
    
def usun_czesc(con, ui):
    """
    Funkcja usuwania elementu z tabeli czesci o podanym id

    Args:
    con (socket.socket): poloczenie z serwerem
    ui (Ui): GUI programu
    """
    #Przy kliknieciu "Usun" tworzy wyskakujace okienko do potwierdzenia ze na pewno chcemy usunac
    potwierdzenie = tkinter.messagebox.askyesno("Potwierdzenie usunięcia", "Czy na pewno chcesz usunąć ten wiersz danych?")
    if potwierdzenie:
        #Pobiera wartosci z pierwszej kolumny z wiersza wybranego(tree.selection)
        id = ui.tree.item(ui.tree.selection(),"values") [0]
        msg = f"DEL/CZESCI/{id}"
        wyslij_msg(con, msg)
        #Przypisujemy zaktualizowane dane do zmiennej w ui
        ui.czesci = odbierz_dane(con)
        #Aktualizujemy wyswietlanie zawartosci tabeli
        ui.update_tree()
    
def zmien_czesc(con, ui):
    """
    Funkcja zmiany wybranego pola wybranego elementu w tabeli Czesci

    Args:
    con (socket.socket): poloczenie z serwerem
    ui (Ui): GUI programu
    """
    #Wybrany element
    wybrany_el = ui.tree.selection()
    if wybrany_el:
        # Pobranie wartości zaznaczonego elementu
        wartosci = ui.tree.item(wybrany_el, 'values')
        nazwa_kolumny = ui.tree.column(ui.wybrna_kol, 'id')
        index_kol = int(ui.wybrna_kol.lstrip("#"))
        id = wartosci[0]
        # Wywołanie okna dialogowego do wprowadzenia nowej wartości
        if nazwa_kolumny == 'Typ':  # Jeżeli kolumna to 'Typ', użyj Combobox(okienko z  wyborem z listy)
            new_value = ui.show_combobox_dialog("Zmiana wartości", ui.typy)
        else:   #Jezeli to inne kolumny wywolaj wyskakujace okienko z polem do wpisania nowej wartosci, domyslnie wyswietla aktualna wartosc
            new_value = askstring("Zmiana wartości", f"Wprowadź nową zawartość dla {nazwa_kolumny}:", initialvalue=wartosci[int(index_kol-1)])
        # Wysylanie id elementu zmienionego, w jakiej kolumnie to zmieniono i na co zmieniono
        if new_value is not None:
            msg = f"UPDT/CZESCI/{id},{nazwa_kolumny},{new_value}"
            wyslij_msg(con, msg)
            ui.czesci = odbierz_dane(con)
            ui.update_tree()
            
def pobierz_czesci(con: socket.socket):
    """
    Pobiera wszystkie elementy z tabeli Czesci 

    Args:
    con (socket.socket): poloczenie z serwerem

    Returns:
    dane (list): zwaraca dane z tabeli w postaci listy
    """
    msg = 'GET/CZESCI/ALL'
    wyslij_msg(con, msg)
    dane = odbierz_dane(con)
    return dane
