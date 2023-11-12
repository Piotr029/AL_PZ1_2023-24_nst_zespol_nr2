import socket       #bilioteka do twrzenia polaczen 
import threading    #biliteka do nie tyle rownoleglego dzialania co rownoleglego kolejkowania polecen

PORT = 5050         #na jakim portcie bedzie relizowane poloczenie
SERVER_IP = "192.168.1.7"   #IP serwera, w tym przykladzie dzialamy w sieci lokalnej wiec ip lokalne
                            #Jezeli wpiszemy tu 0.0.0.0 to teroetycznie powinien sluchac na poloczenia przez internet - nie testowalem jeszcze                            
ADR = (SERVER_IP, PORT)     #adress naszego serwera
#alternatywnie mozna uzyc
#SERVER_IP = socket.gethostbyname(socket.gethostname()) Pobiera adress ip automatycznie
HEADER = 4       #dlugosc 4 bajtow
FORMAT = 'utf-8'
ROZLACZ = '!Out'      

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tworzymy serwer, pierwszy arg to typ polcznia ip4/ip6/bluetooth itd
                                                            #drugi argument to jak realizujemy przesyl danych
                                                            
server.bind(ADR)

def start():
    server.listen()
    while True:
        conn, adr = server.accept()             # tutaj program czeka na poloczenie, dopoki nie otrzyma polocznie nie reazlizuje dalszych polecen 
                                                # troche tak jak wait/sleep funkcja. Gdy otrzyma poloczenie przekazuje obiekt "polocznie" i z jakiego adresu
        klient = threading.Thread(target=obsluga_klienta, args=(conn,adr)) # tutaj tworzymy nowy "watek" klienta, pozwala to programowi jednoczesnie kolejkowac 
                                                # i wykonywac polecenia z funkcji oblusha kilenta 1, 2, 3 itd jak i nasluchiwac poloczenia
        klient.start()
        print(f"[NOWY KLIENT] Utworzono Nowe Poloczenie. Aktualnie {threading.active_count()-1} aktywnych poloczen")

def obsluga_klienta(con, adr):
    print(f"[POLACZENIE] Poloczono z {adr}")
    connected = True
    while connected:
        #con.recv(liczba) - okreslamy jakiej ilosci danych w bajtach mamy sluchac i pozniej je zlozyc w wiadomosc
        msg_length = con.recv(HEADER).decode(FORMAT)       #pierwsza wiadomosc to zawsze stalej wielkosci bajtow informacje o dlugosci nastpenej -wlasciwej- wiadomosci 
        if msg_length: #(pierwsza zawartosc poloczenia klient-serwer jest pusty pakiet, jego pomijamy)
            msg_length = int(msg_length)
            msg = con.recv(msg_length).decode(FORMAT)           #wlasciwa wiadomosc/.decode zamienia bajtowa wiadmosc w str
            con.send(("Wiadomość otrzymana").encode(FORMAT))
            if msg == ROZLACZ:
                connected = False
            print(f"{adr}: {msg}")
    con.close()
    
print('[STARTING] Serwer startuje......')
start()
