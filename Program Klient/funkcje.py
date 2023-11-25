import socket
import pickle
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
    
    