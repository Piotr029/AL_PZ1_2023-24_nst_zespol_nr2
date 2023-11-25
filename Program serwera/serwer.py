#Kod Serwera Wykonał Raducha Michał
import socket
import threading
import cx_Oracle as orc
import obsluga as obs
import pickle as pck

PORT = 5050 
SERVER_IP = "192.168.1.7" #dom - 192.168.1.7  #Praca - 192.168.23.244
ADR = (SERVER_IP, PORT) 
HEADER = 4
FORMAT = 'utf-8'
ROZLACZ = '!Out'
SEPARATOR = "/"
OK = "!OK" 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADR)

def start():
    server.listen()
    db_conn = orc.connect('c##admin/dbpass2@localhost:1521/xe')
    while True:
        conn, adr = server.accept() 
        klient = threading.Thread(target=obsluga_klienta, args=(conn, adr, db_conn))
        klient.start()
        print(f"[NOWY KLIENT] Utworzono Nowe Poloczenie. Aktualnie {threading.active_count()-1} aktywnych poloczen")
        
def odbierz_wiadomosc(con: socket.socket):
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
        msg = msg.split(SEPARATOR)
        return msg, warunek
    
def odbierz_dane(con: socket.socket):
    dane_length = int(con.recv(HEADER).decode(FORMAT))
    msg_dane = con.recv(dane_length)
    dane = pck.loads(msg_dane)
    return dane
    
    
def przeslij_dane(con, dane):
    msg = pck.dumps(dane)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' '*(HEADER-len(msg_length))
    con.send(msg_length)
    con.send(msg)
        
def obsluga_klienta(con, adr, db_conn):
    print(f"[POLACZENIE] Poloczono z {adr}")
    connected = True
    while connected:
        msg, connected = odbierz_wiadomosc(con)
        if connected == False: continue
        tryb = msg[0]
        tabela = msg[1]
        atrybuty = msg[2]
        match tryb:
            case 'GET':
                if tabela == "TYPY_CZESCI": g_dane = obs.GET_TYPY_CZESCI(db_conn, atrybuty)
                if tabela == "CZESCI": g_dane = obs.GET_CZESCI(db_conn)
                
            case 'POST':
                p_dane = odbierz_dane(con)
                if tabela == "CZESCI": g_dane = obs.Post_CZESCI(db_conn, p_dane)
        
        przeslij_dane(con, g_dane)
        
                                            
    con.close()
    
if __name__ == "__main__":
    print('[STARTING] Serwer startuje......')
    start()