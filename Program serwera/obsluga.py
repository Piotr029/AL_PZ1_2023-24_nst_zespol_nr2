"""
Modul obslugi zapytan do bazy dancych
"""
import cx_Oracle as orc

VERSION = 1.2

def obrob_dane(dane: list):
    """
    Funkcja obrobki danych z bazy danych
    
    Dane przychodza w formacie "('Dana1', 'Dana2', 'Dana3')"
         wychodza z funkcj w formacie "Dana1, Dana2, Dana3"
    Args:
    dane (lista): dane z bazy dancyh

    Returns:
    dane(lsita): dane z bazy danych bez znakow , i ()
    """
    for w in range(len(dane)):
        new_czesc = str(dane[w]).strip('()').replace("'", '')
        dane[w] = new_czesc
    return dane   


def GET_TYPY_CZESCI(db_conn, atrybuty: str):
    """
    Pobiera i zwraca dane z tabeli Typy_Czesci

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    atrybuty (str): atrybuty(3 czlon wiadomosci)

    Returns:
    czesci (list): dane z tabeli typy_czesci
    """
    #obiekt do operacji w bazie danych
    cursor = db_conn.cursor()
    #Jezeli chcemy wszystkie dane, kiedys moze bedziemy chcec pojedynczy element
    if atrybuty == "ALL": 
        cursor.execute("SELECT * FROM TYPY_CZESCI")
        czesci = cursor.fetchall()
        cursor.close()
        czesci = obrob_dane(czesci)
        return czesci
    
def GET_CZESCI(db_conn):
    """
    Pobiera i zwraca dane z tabeli Czesci

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    atrybuty (str): atrybuty(3 czlon wiadomosci)

    Returns:
    czesci (list): dane z tabeli czesci
    """
    cursor = db_conn.cursor()
    # if atrybuty == "ALL":
        #Chwilowo tak zrobilem, zeby nie pobierac danych z kolum zdjecie/link, bo nie oblsuguje tego jeszcze
    zapytanie = """
        SELECT CZESCI.ID, CZESCI.NAZWA, 
            TYPY_CZESCI.NAZWA || '-' || TYPY_CZESCI.POD_NAZWA AS TYPY_CZESCI_FORMAT,
            CZESCI.PARAMETR_1, CZESCI.PARAMETR_2, CZESCI.PARAMETR_3
        FROM CZESCI
        JOIN TYPY_CZESCI ON CZESCI.TYPY_CZESCI_ID = TYPY_CZESCI.ID
        ORDER BY CZESCI.ID
    """
    cursor.execute(zapytanie)
    czesci = cursor.fetchall()
    cursor.close()
    czesci = obrob_dane(czesci)
    return czesci
    
    
def Post_CZESCI(db_conn, dane: list):
    """
    Wstawia nowy element do tabeli Czesci i zwraca zauktalizowane dane tabeli czesci

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    dane (list): dane elementu do wstawienia

    Returns:
    nowe_dane: zauktalizowa dane tabeli czesci
    """
    cursor = db_conn.cursor()
    nazwa = dane[0]
    typ = dane[1]
    parametr1 = dane[2]
    parametr2 = dane[3]
    parametr3 = dane[4]
    
    #uzywamy procedury PL/SQL dodaj_czesc (atrybuty procedury)
    cursor.callproc("dodaj_czesc", (nazwa, typ, parametr1, parametr2, parametr3))
    db_conn.commit()
    cursor.close()
    #Pobieramy zaktualizowane dane
    nowe_dane = GET_CZESCI(db_conn)
    return nowe_dane

def DEL_CZESCI(db_conn, id :int):
    """
    Usuwa elemnt o id
    
    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    id (int): id elementu do usuniecia

    Returns:
    nowe_dane: zauktalizowa dane tabeli czesci
    """
    cursor = db_conn.cursor()
    #uzywamy procedury PL/SQL usun_czesc
    cursor.callproc("usun_czesc", (id))
    db_conn.commit()
    cursor.close()
    nowe_dane = GET_CZESCI(db_conn)
    return nowe_dane

def UPDT_CZESCI(db_conn, atrybuty: str):
    """
    Zmienia dane  konkretnego elemntu w konkretnej kolumnie

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    atrybuty (str): "id,nazwa_kolumny,nowa_wartosc"

    Returns:
    nowe_dane: zauktalizowa dane tabeli czesci
    """
    lista = atrybuty.split(",")
    id = int(lista[0])
    nazwa_kolumny = lista[1]
    nowa_wartosc = lista[2].lstrip(" ") #czasami, chyba jezeli enter w formularzu kliknie, " wartosc" ma postac
    cursor = db_conn.cursor()
    #Jezeli kolumna to typ - czyli wartosci numeryczne wywolujemy procedure dla zmiany kolumny numerycznej
    if nazwa_kolumny == "Typ": cursor.callproc("zmien_czesc_num", (id, "TYPY_CZESCI_ID", nowa_wartosc))
    #Pozostalem kolumny w tej tabeli to varchary
    else: cursor.callproc("zmien_czesc_czar", (id, nazwa_kolumny, nowa_wartosc))
    db_conn.commit()
    cursor.close()
    nowe_dane = GET_CZESCI(db_conn)
    return nowe_dane

#######################################################################################################################
#Tabela Pozycja Czesci (Stan Magazynu)
#########################################################################################################################

def GET_STAN_MAGAZYNU(db_conn):
    """
    Pobiera i zwraca Stan Magazynu

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd

    Returns:
    dane (list): dane o stanie magazynu
    """
    cursor = db_conn.cursor()  
    result_set = cursor.var(orc.CURSOR)
    cursor.callproc("pobierz_dane_pozycja_czesci", (result_set,))
    dane = result_set.getvalue()
    dane = dane.fetchall()
    cursor.close()
    dane = obrob_dane(dane)
    stan = []
    for wiersz in dane:
        wiersz = str(wiersz)
        temp = wiersz.split(',')
        id = temp [0]
        pokoj = temp[1]
        miejsce = (f'{temp[2]} -{temp[3]} -{temp[4]}')
        czesc = temp[5]
        ilosc = (f'{temp[6]}{temp[7]}')
        stan.append(f'{id},{czesc},{ilosc},{pokoj},{miejsce}')
    return stan

def UPDT_POZYCJA_CZESCI(db_conn, atrybuty: str):
    """
    Zmienia dane  konkretnego elemntu w konkretnej kolumnie

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    atrybuty (str): "id,nazwa_kolumny,nowa_wartosc"

    Returns:
    nowe_dane: zauktalizowa dane tabeli czesci
    """
    lista = atrybuty.split(",")
    id = int(lista[1])
    kolumny = lista[0]
    cursor = db_conn.cursor()
    if kolumny == 'Ilosc': 
        nowa_ilosc = float(lista[2].lstrip())
        nowa_miara = int(lista[3].lstrip())
        id_uzytkownika = int(lista[4].lstrip())
        cursor.callproc("POPRAW_ILOSC_POZ_CZESCI", (id, nowa_ilosc, nowa_miara, id_uzytkownika))
    db_conn.commit()
    cursor.close()
    nowe_dane = GET_STAN_MAGAZYNU(db_conn)
    return nowe_dane

###########################################################
    #Drugorzedne tabele
###########################################################

#Miary

def GET_MIARY(db_conn):
    """
    Pobiera i zwraca dane z tabeli Miary

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    atrybuty (str): atrybuty(3 czlon wiadomosci)

    Returns:
    dane (list): dane z tabeli
    """
    #obiekt do operacji w bazie danych
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM MIARY")
    dane = cursor.fetchall()
    cursor.close()
    dane = obrob_dane(dane)
    return dane    

#Uzytkownicy

def GET_UZYTKOWNIK(db_conn):
    """
    Pobiera i zwraca dane z tabeli Uzytkownicy

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd

    Returns:
    dane (list): dane z tabeli
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM UZYTKOWNIK")
    dane = cursor.fetchall()
    cursor.close()
    dane = obrob_dane(dane)
    return dane 

#Historia Zmian

def GET_HISTORIA_ZMIAN(db_conn):
    """
    Pobiera i zwraca dane z tabeli HISTORIA_ZMIAN

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd

    Returns:
    dane (list): dane z tabeli
    """    
    cursor = db_conn.cursor()
    #Kontynuowac
