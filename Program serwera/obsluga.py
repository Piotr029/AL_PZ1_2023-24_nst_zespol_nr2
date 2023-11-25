import cx_Oracle as orc

"""_summary_
"""
def obrob_dane(dane):
    for w in range(len(dane)):
        new_czesc = str(dane[w]).strip('()').replace("'", '')
        dane[w] = new_czesc
    return dane   


def GET_TYPY_CZESCI(db_conn, atrybuty):
    """_summary_ TYPY_CZESCI
    """
    cursor = db_conn.cursor()
    
    if atrybuty == "ALL": 
        cursor.execute("SELECT * FROM TYPY_CZESCI")
        czesci = cursor.fetchall()
        cursor.close()
        czesci = obrob_dane(czesci)
        return czesci
    
def GET_CZESCI(db_conn):
    cursor = db_conn.cursor()
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
    
    
def Post_CZESCI(db_conn, dane):
    cursor = db_conn.cursor()
    nazwa = dane[0]
    typ = dane[1]
    parametr1 = dane[2]
    parametr2 = dane[3]
    parametr3 = dane[4]
    
    
    cursor.callproc("dodaj_czesc", (nazwa, typ, parametr1, parametr2, parametr3))
    db_conn.commit()
    cursor.close()
    nowe_dane = GET_CZESCI(db_conn)
    return nowe_dane
    
        
        