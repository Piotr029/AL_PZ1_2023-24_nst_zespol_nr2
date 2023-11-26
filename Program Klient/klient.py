import socket       #bilioteka do twrzenia polaczen 
import funkcje as f
from test_UI import SimpleUI as Ui

VERSION = 1.1

PORT = 5050         #na jakim portcie bedzie relizowane poloczenie
SERVER_IP = "192.168.1.7"   #IP serwera, w tym przykladzie dzialamy w sieci lokalnej wiec ip lokalne
ADR = (SERVER_IP, PORT)     #adress naszego serwera

HEADER = 4       #dlugosc 4 bajtow
FORMAT = 'utf-8'
ROZLACZ = '!Out'
SEPARATOR = "/" 
TEST = False

#Format - GET,POST / Jakiej tabeli/procedury dotyczy/ Argumenty

klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tworzymy serwer, pierwszy arg to typ polcznia ip4/ip6/bluetooth itd
                                                            #drugi argument to jak realizujemy przesyl danych
                                                            
klient.connect(ADR)

def send(txt: str):
    msg = txt.encode(FORMAT)                        #zamien str na bajty
    msg_length = len(msg)                           #zmierz jako dlugosc bedzie miala wiadomosc juz w bytach
    send_length = str(msg_length).encode(FORMAT)    #zamien dlugosc wiadomosci na str a pozniej na byty
    send_length += b' '*(HEADER-len(send_length))   #Dodaje puste znaki do wyznaczonej dlugosci, zeby pierwsza wiadomosc byla zawsze tej samej dl
    klient.send(send_length)                        #Wysylam najpierw jakiej dlugosci bedzie wiadomosc
    klient.send(msg)                                #Wysylam wiadomosc
    print(klient.recv(21).decode(FORMAT))                          #otrzymuje potwierdzenie - akutat potwierdzenie jest dl 21
    
if TEST:
    czesci = f.pobierz_Typy_Czesci(klient)
    for czesc in czesci:
        print(czesc)
    input()
    send(ROZLACZ)
    
def dodawanie_czesci(klient):
    nowa_czesc = ui.dane_z_formularza()
    ui.czesci = f.dodaj_czesc(klient, nowa_czesc)
    ui.update_tree()



if __name__ == "__main__":
    ui = Ui()
    ui.typy = f.pobierz_Typy_Czesci(klient)
    ui.czesci = f.pobierz_czesci(klient)
    ui.context_menu.add_command(label="Zmien", command=lambda: f.zmien_czesc(klient, ui))
    ui.context_menu.add_command(label="Usun", command=lambda: f.usun_czesc(klient, ui))
    ui.context_menu.add_command(label="Opcja 3")
    ui.button_dodaj.config(command=lambda: dodawanie_czesci(klient))
    
    ui.run()
    send(ROZLACZ)
