import socket       #bilioteka do twrzenia polaczen 

PORT = 5050         #na jakim portcie bedzie relizowane poloczenie
SERVER_IP = "192.168.1.7"   #IP serwera, w tym przykladzie dzialamy w sieci lokalnej wiec ip lokalne
ADR = (SERVER_IP, PORT)     #adress naszego serwera

HEADER = 4       #dlugosc 4 bajtow
FORMAT = 'utf-8'
ROZLACZ = '!Out'

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
    
    
send("Hello Serwerze!")
send(ROZLACZ)    