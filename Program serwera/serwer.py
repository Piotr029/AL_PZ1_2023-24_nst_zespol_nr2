#Kod Serwera Wykonał Raducha Michał
import socket
import threading
import cx_Oracle as orc
import obsluga as obs   #modul obslugi zapytan bazy danych
import pickle as pck    #bilioteka to pakowania(serializowania)/odpakowywania danych

VERSION = 1.2 
PORT = 5050                                                                     
SERVER_IP = "192.168.1.6" #dom - 192.168.1.7  #Praca - 192.168.23.244
ADR = (SERVER_IP, PORT) 
HEADER = 4
FORMAT = 'utf-8'
ROZLACZ = '!Out'
SEPARATOR = "/"
OK = "!OK" 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADR)

def start():
    """
    Funkcja Glowna, startuje serwer i nasluchuje polaczen
    """
    server.listen()
    #polaczenie bazy do bazy dancyh
    db_conn = orc.connect('c##admin/dbpass2@localhost:1521/xe')
    while True:
        conn, adr = server.accept() 
        klient = threading.Thread(target=obsluga_klienta, args=(conn, adr, db_conn))
        klient.start()
        print(f"[NOWY KLIENT] Utworzono Nowe Poloczenie. Aktualnie {threading.active_count()-1} aktywnych poloczen")
        
def odbierz_wiadomosc(con: socket.socket):
    """
    Funkcja odbierania wiadomosci str
    
    Args:
    con (socket.socket): obiekt poloczenia serwera

    Returns:
    msg (str) - tresc wiadomosc
    warunek(True/False) - czy wyslano komende !out
    """
    msg_length = con.recv(HEADER).decode(FORMAT)
    warunek = True
    if msg_length:
        msg_length = int(msg_length)
        msg = con.recv(msg_length).decode(FORMAT)
        print(f"[RECV]: {msg}")
        con.send((OK).encode(FORMAT))
        if msg == ROZLACZ:
            warunek = False
            return msg, warunek
        #Wiadomosci maja format: "Tryb/Tabela_ktorej_dotyczy/argumenty"
        #czyli np "GET/CZESCI/ALL"
        msg = msg.split(SEPARATOR)
        return msg, warunek
    
def odbierz_dane(con: socket.socket):
    """
    Funkcja odbiernia danych innych niz str, np listy, uzywajaca pickla

    Args:
    con (socket.socket): obiekt poloczenia serwera

    Returns:
    dane (ANY) - od-picklowane dane np liste, obiekt, zdjecie
    """
    dane_length = int(con.recv(HEADER).decode(FORMAT))
    msg_dane = con.recv(dane_length)
    dane = pck.loads(msg_dane)
    return dane
    
    
def przeslij_dane(con: socket.socket, dane):
    """
    Funkcja wysylania danych innych niz str, np listy, uzywajaca pickla

    Args:
    con (socket.socket): obiekt poloczenia serwera
    dane (ANY): dane do przeslania, tj listy, obiekty, zdjecie
    """
    msg = pck.dumps(dane)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' '*(HEADER-len(msg_length))
    con.send(msg_length)
    con.send(msg)
        
def obsluga_klienta(con: socket.socket, adr, db_conn):
    """
    Funkcja obslugujaca poszczegolnych klientow

    Args:
    con (socket.socket): obiekt poloczenia serwera
    adr (socket._RetAddress): Adres klienta
    db_conn (polocznie_bd): obiekt poloczenia z bd
    """
    print(f"[POLACZENIE] Poloczono z {adr}")
    connected = True
    #Jezeli wiadomosc nie jest NONE, pierwsze wiadmosci przy poloczeniu sa puste
    while connected:
        msg, connected = odbierz_wiadomosc(con)
        if connected == False: continue #wychodzi z petli
        #Wiadomosci maja format: "Tryb/Tabela_ktorej_dotyczy/argumenty"
        tryb = msg[0]
        tabela = msg[1]
        atrybuty = msg[2]
        match tryb:
            #Pobieranie danych
            case 'GET':
                if tabela == "TYPY_CZESCI": g_dane = obs.GET_TYPY_CZESCI(db_conn, atrybuty)
                if tabela == "CZESCI": g_dane = obs.GET_CZESCI(db_conn)
                if tabela == 'POZYCJA_CZESCI': g_dane = obs.GET_STAN_MAGAZYNU(db_conn)
                if tabela == 'MIARY': g_dane = obs.GET_MIARY(db_conn)
                if tabela == 'UZYTKOWNIK': g_dane = obs.GET_UZYTKOWNIK(db_conn)
                if tabela == 'HISTORIA_ZMIAN': g_Dane = obs.GET_HISTORIA_ZMIAN(db_conn)
            #Wstawianie danych    
            case 'POST':
                p_dane = odbierz_dane(con)
                if tabela == "CZESCI": g_dane = obs.Post_CZESCI(db_conn, p_dane)
            #Usuwanie danych    
            case 'DEL':
                if tabela == "CZESCI": g_dane = obs.DEL_CZESCI(db_conn, atrybuty)
            #Zmiana danych    
            case 'UPDT':
                if tabela == "CZESCI": g_dane = obs.UPDT_CZESCI(db_conn, atrybuty)
                if tabela == "POZYCJA_CZESCI": g_dane = obs.UPDT_POZYCJA_CZESCI(db_conn, atrybuty)
        #Przeslij z powrotem dane tabeli po zmianach 
        przeslij_dane(con, g_dane)
    #Po wyjsciu z petli zakoncz polaczenie                                        
    con.close()
    
if __name__ == "__main__":
    print('[STARTING] Serwer startuje......')
    
    start()
