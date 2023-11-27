"""
Modul obslugi zapytan do bazy dancych
"""
import cx_Oracle as orc

VERSION = 1.15

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
    
def GET_CZESCI(db_conn, atrybuty: str):
    """
    Pobiera i zwraca dane z tabeli Czesci

    Args:
    db_conn (polocznie z bd): obiekt poloczenia z bd
    atrybuty (str): atrybuty(3 czlon wiadomosci)

    Returns:
    czesci (list): dane z tabeli czesci
    """
    cursor = db_conn.cursor()
    if atrybuty == "ALL":
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
        
