import socket       #bilioteka do twrzenia polaczen 
import funkcje as f #modul z funkcjami, pewnie profesjonalniej bedzie trzeba to nazwac
from test_UI import SimpleUI as Ui  #ui testowe

VERSION = 1.2

PORT = 5050         #na jakim portcie bedzie relizowane poloczenie #5050
SERVER_IP = "192.168.1.6"   #IP serwera, w tym przykladzie dzialamy w sieci lokalnej wiec ip lokalne #192.168.23.244 
ADR = (SERVER_IP, PORT)     #adress naszego serwera

HEADER = 4       #dlugosc 4 bajtow mowiaca jaka bedzie dl glownej wiadomosci
FORMAT = 'utf-8'
ROZLACZ = '!Out'
SEPARATOR = "/" 
TEST = False

#Format msg - GET,POST / Jakiej tabeli/ Argumenty

klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tworzymy serwer, pierwszy arg to typ polcznia ip4/ip6/bluetooth itd
                                                            #drugi argument to jak realizujemy przesyl danych
                                                            
klient.connect(ADR)

#Na razie zostawiam do testowania tutaj
def send(txt: str):
    msg = txt.encode(FORMAT)                        #zamien str na bajty
    msg_length = len(msg)                           #zmierz jako dlugosc bedzie miala wiadomosc juz w bytach
    send_length = str(msg_length).encode(FORMAT)    #zamien dlugosc wiadomosci na str a pozniej na byty
    send_length += b' '*(HEADER-len(send_length))   #Dodaje puste znaki do wyznaczonej dlugosci, zeby pierwsza wiadomosc byla zawsze tej samej dl
    klient.send(send_length)                        #Wysylam najpierw jakiej dlugosci bedzie wiadomosc
    klient.send(msg)                                #Wysylam wiadomosc
    print(klient.recv(3).decode(FORMAT))                          #otrzymuje potwierdzenie - akutat potwierdzenie jest dl 3
    
if TEST:
    print('Prubuje wyslac')
    send("Witaj z komuptera w Pracy")
    print('wyslalem')
    input()
    send(ROZLACZ)
    
def start_ui():
    """
    Funkcja tworzaca GUI i wykonujaca przypisanie funkcji do widgetow

    Returns:
    ui(UI obiekt) = zbudowane ui
    """
    #tworzenie obiektu ui()
    ui = Ui()
    #pobranie poczatkowych danych do wyswietlenia
    ui.stan = f.pobierz_stan_magazynu(klient)
    ui.miary = f.pobierz_miary(klient)
    ui.uzytkownicy = f.pobierz_uztkownikow(klient)
    ui.hist_zmin_mag = f.pobierz_hist_zmin_mag(klient)
    #Przypisanie funkcji do elementow Ui
    ui.b3_menu_magazyn.add_command(label="Popraw Nazwe", command=lambda: f.popraw_nz_w_magazynie(klient, ui))
    ui.b3_menu_magazyn.add_command(label="Popraw Ilość", command=lambda: f.popraw_ilosc_w_magazynie(klient, ui))
    ui.czesci = f.pobierz_czesci(klient)
    #przypisanie funkcji do widgetow je obslugujacyh przyciski itd
    #zwaracamy zbydowane ui
    return ui
    
    

if __name__ == "__main__":
    #Budujemy ui
    ui = start_ui()
    #Startujemy Main Loop okna
    ui.run()
    #Po zamknieciu okna(wyjscia z app) wyslij o rozloczeniu z serwera
    send(ROZLACZ)
