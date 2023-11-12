import cx_Oracle as orc #bilioteka do laczenia sie z baza danych


conn = orc.connect('c##admin/dbpass2@localhost:1521/xe')       #tworzenie poloczenia
                    #user_name/haslo/adres do poloczenia
cursor = conn.cursor()          #tworzenie obiektu ktorym bedzie relizowac zapytania
cursor.execute("SELECT * FROM TYPY_CZESCI") #mozna albo pelne zapytanie na razie przy testach,
                                            #ale lepiej zeby wykonywac zapisane wczesniej w bazie danych procedury
                                            #uzywajac cursor.callproc('nazwa_procedury'[atrybuty])
czesci = cursor.fetchall()                  #zwraca odpwiedz bazy danych
cursor.close()                              #po kazdym zapytaniu i pobraniu zawartosci odpowiedzi zamykmy je              
print(f"zawartosc: {czesci}")
                       

conn.close()                                #konczymy poloczenie z serwerem, jezeli zamkniemy program poloczenie tez sie zamyka