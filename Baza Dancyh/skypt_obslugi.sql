-- #######################################################
--Oblusga tabeli czesci
--#######################################################
--Sekwecja id czesci
CREATE SEQUENCE seq_czesci 
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  NOCYCLE;
 --Procedura dodawania czesci 
 CREATE OR REPLACE PROCEDURE dodaj_czesc (
  p_nazwa IN VARCHAR2,
  p_typ_czesci_id IN NUMBER,
  p_parametr_1 IN VARCHAR2,
  p_parametr_2 IN VARCHAR2,
  p_parametr_3 IN VARCHAR2
) AS
BEGIN
  INSERT INTO czesci (id, nazwa, typy_czesci_id, parametr_1, parametr_2, parametr_3, zdjecie, link_przyklad)
  VALUES (seq_czesci.NEXTVAL, p_nazwa, p_typ_czesci_id, p_parametr_1, p_parametr_2, p_parametr_3, NULL, NULL);

  COMMIT;
END dodaj_czesc;
/
--Procedura usuwania czesci i jezeli nie ostatni element zminia id o -1
create or replace PROCEDURE usun_czesc(p_id IN NUMBER) AS
  v_max_id NUMBER;
  dummy NUMBER;
BEGIN
  DELETE FROM czesci WHERE id = p_id;

  SELECT MAX(id) INTO v_max_id FROM czesci;

  IF p_id < v_max_id THEN
    -- Jeżeli usunięty element nie był ostatnim, dostosuj ID dla rekordów po nim
    FOR rec IN (SELECT id FROM czesci WHERE id > p_id ORDER BY id)
    LOOP
      UPDATE czesci SET id = rec.id - 1 WHERE id = rec.id;
    END LOOP;
  END IF;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_czesci INCREMENT BY -1';
SELECT seq_czesci.NEXTVAL INTO dummy FROM dual;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_czesci INCREMENT BY 1';
COMMIT;
END usun_czesc;
/
--Procedura zmiany danych w podanej kolumnie tekstowej
create or replace PROCEDURE zmien_czesc_czar(p_id IN NUMBER, p_nazwa_kolumny IN VARCHAR2, p_nowa_wartosc IN VARCHAR2) AS
BEGIN
  EXECUTE IMMEDIATE 'UPDATE czesci SET ' || p_nazwa_kolumny || ' = :nowa_wartosc WHERE id = :id'
    USING p_nowa_wartosc, p_id;
END zmien_czesc_czar;
/
--Procedura zmiany danych w podanej kolumnie numerycznej
create or replace PROCEDURE zmien_czesc_num(p_id IN NUMBER, p_nazwa_kolumny IN VARCHAR2, p_nowa_wartosc IN NUMBER) AS
BEGIN
  EXECUTE IMMEDIATE 'UPDATE czesci SET ' || p_nazwa_kolumny || ' = :nowa_wartosc WHERE id = :id'
    USING p_nowa_wartosc, p_id;
END zmien_czesc_num;
/
-- ########################################################################
-- Obsluga tabeli Magazyn
-- ########################################################################
--Sekwencja id magazyn
CREATE SEQUENCE seq_magazyn
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;
/
--Procedura dodawania elementu do tabeli magazyn
CREATE OR REPLACE PROCEDURE dodaj_magazyn(
	p_nazwa in VARCHAR2) AS
BEGIN
	INSERT INTO MAGAZYN (ID, NAZWA)
	VALUES (seq_magazyn.NEXTVAL, p_nazwa);
	
	COMMIT;
END dodaj_magazyn;
/
--procedura usuwania elementu z tabeli magazyn
CREATE OR REPLACE PROCEDURE usun_magazyn(p_id in NUMBER) AS
v_max_id NUMBER;
dummy NUMBER;
BEGIN
	DELETE FROM MAGAZYN WHERE ID = p_id;
	SELECT MAX(ID) INTO v_max_id FROM MAGAZYN; 
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_magazyn INCREMENT BY -1';
SELECT seq_magazyn.NEXTVAL INTO dummy FROM dual;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_magazyn INCREMENT BY 1';
COMMIT;
END usun_magazyn;
/
--Procedura zmiany nazwy magazynu
CREATE OR REPLACE PROCEDURE zmien_n_magazyn(p_id in NUMBER, p_nowa_nazwa in VARCHAR2) AS
BEGIN
	EXECUTE IMMEDIATE 'UPDATE MAGAZYN SET NAZWA = :nowa_nazwa WHERE ID = :id'
	USING p_nowa_nazwa, p_id;
END zmien_n_magazyn;
/
-- ########################################################################
-- Obsluga tabeli Magazyn_Miejsca
-- ########################################################################
--Sekwencja id magazyn_miejsca
CREATE SEQUENCE seq_magazyn_miejsca
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;
/
--Procedura dodawania elementu do tabeli magazyn_miejsca
CREATE OR REPLACE PROCEDURE dodaj_magazyn_miejsca(
	p_nazwa in VARCHAR2, p_id_magazynu in VARCHAR2) AS
BEGIN
	INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID)
	VALUES (seq_magazyn_miejsca.NEXTVAL, p_nazwa, p_id_magazynu);
	
	COMMIT;
END dodaj_magazyn_miejsca;
/
--procedura usuwania elementu z tabeli magazyn_miejsca
CREATE OR REPLACE PROCEDURE usun_magazyn_miejsca(p_id in NUMBER) AS
v_max_id NUMBER;
dummy NUMBER;
BEGIN
	DELETE FROM MAGAZYN_MIEJSCA WHERE ID = p_id;
	SELECT MAX(ID) INTO v_max_id FROM MAGAZYN;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_magazyn_miejsca INCREMENT BY -1';
SELECT seq_magazyn_miejsca.NEXTVAL INTO dummy FROM dual;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_magazyn_miejsca INCREMENT BY 1';
COMMIT;
END usun_magazyn_miejsca;
/
--Procedura zmiany nazwy magazyn_miejsca
CREATE OR REPLACE PROCEDURE zmien_n_magazyn_miejsca(p_id in NUMBER, p_nowa_nazwa in VARCHAR2) AS
BEGIN
	EXECUTE IMMEDIATE 'UPDATE MAGAZYN_MIEJSCA SET NAZWA = :nowa_nazwa WHERE ID = :id'
	USING p_nowa_nazwa, p_id;
END zmien_n_magazyn_miejsca;
/
--Procedura zmiany magazynu magazyn_miejsca
CREATE OR REPLACE PROCEDURE zmien_m_magazyn_miejsca(p_id in NUMBER, p_nowy_magazyn in NUMBER) AS
BEGIN
	EXECUTE IMMEDIATE 'UPDATE MAGAZYN_MIEJSCA SET MAGAZYN_ID= p_nowy_magazyn WHERE ID = :id'
	USING p_nowy_magazyn, p_id;
END zmien_m_magazyn_miejsca;
/
-- ########################################################################
-- Obsluga tabeli Miejsce_Pozycja
-- ########################################################################
--Sekwencja id miejsce_pozycja
CREATE SEQUENCE seq_miejsce_pozycja
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;
/
--Procedura dodawania elementu do tabeli miejsce_pozycja
CREATE OR REPLACE PROCEDURE dodaj_miejsce_pozycja(
	p_nazwa in VARCHAR2, p_id_miejsce_pozycja in NUMBER ) AS
BEGIN
	INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID)
	VALUES (seq_miejsce_pozycja.NEXTVAL, p_nazwa, p_id_miejsce_pozycja);
	COMMIT;
END dodaj_miejsce_pozycja;
/
--procedura usuwania elementu z tabeli miejsce_pozycja
CREATE OR REPLACE PROCEDURE usun_miejsce_pozycja(p_id in NUMBER) AS
dummy NUMBER;
BEGIN
	DELETE FROM MIEJSCE_POZYCJA WHERE ID = p_id;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_miejsce_pozycja INCREMENT BY -1';
SELECT seq_miejsce_pozycja.NEXTVAL INTO dummy FROM dual;
EXECUTE IMMEDIATE 'ALTER SEQUENCE seq_miejsce_pozycja INCREMENT BY 1';
COMMIT;
END usun_miejsce_pozycja;
/
--Procedura zmiany nazwy miejsce_pozycja
CREATE OR REPLACE PROCEDURE zmien_n_miejsce_pozycja(p_id in NUMBER, p_nowa_nazwa in VARCHAR2) AS
BEGIN
	EXECUTE IMMEDIATE 'UPDATE MIEJSCE_POZYCJA, SET NAZWA = :nowa_nazwa WHERE ID = :id'
	USING p_nowa_nazwa, p_id;
END zmien_n_miejsce_pozycja;
/
--Procedura zmiany id_miejsca_magazynu tabeli miejsce_pozycja
CREATE OR REPLACE PROCEDURE zmien_m_miejsce_pozycja(p_id in NUMBER, p_nowy_numer in NUMBER) AS
BEGIN
	EXECUTE IMMEDIATE 'UPDATE MIEJSCE_POZYCJA SET MAGAZYN_MIEJSCA_ID= p_nowy_numer WHERE ID = :id'
	USING p_nowy_numer, p_id;
END zmien_m_miejsce_pozycja;
/
-- ########################################################################
-- Obsluga tabeli Pozycja_Czesci
-- ########################################################################
--Pobieranie danych z pozycja_czesci wraz z nazwa magazynu, nazwa miiesca, nazwa pozycji, nazwa czesci, nazwa miary dla odpowiednich id
CREATE OR REPLACE PROCEDURE pobierz_dane_pozycja_czesci(p_resoult OUT SYS_REFCURSOR) AS
BEGIN
	OPEN p_resoult FOR
		SELECT
			pc.id AS id,
			m.nazwa AS nazwa_magazynu,
			mm.nazwa AS nazwa_miejsca,
			mp.nazwa AS nazwa_pozycji,
			pc.dodatkowe_info,
			c.nazwa AS nazwa_czesci,
			pc.ilosc,
			mi.nazwa AS nazwa_miary
		FROM
			Magazyn m
			JOIN Magazyn_Miejsca mm ON m.id = mm.magazyn_id
			JOIN Miejsce_Pozycja mp ON mm.id = magazyn_miejsca_id
			JOIN Pozycja_Czesci pc ON mp.id = pc.MIEJSCE_POZYCJA_ID
			JOIN Miary mi ON pc.miary_id = mi.id
			JOIN Czesci c ON pc.czesci_id = c.id;
END pobierz_dane_pozycja_czesci;
/
--Sekwencja id Pozycja_Czesci
CREATE SEQUENCE seq_pozycja_czesci
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;
/
--Procedura dodawania elementu do tabeli pozycja_czesci
CREATE OR REPLACE PROCEDURE dodaj_czesc_pozycje(
	p_mp_id in NUMBER, p_info in VARCHAR2, p_czesc_id in NUMBER, p_ilosc in FLOAT, p_miary in NUMBER) AS
BEGIN
	INSERT INTO POZYCJA_CZESCI (ID, MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID)
	VALUES (seq_pozycja_czesci.NEXTVAL, p_mp_id, p_info, p_czesc_id, p_ilosc, p_miary);
	COMMIT;
END dodaj_czesc_pozycje;
/
--Procedura zmiany ilosci w tabeli pozycja_czesci
CREATE OR REPLACE PROCEDURE zmien_ilosc_poz_czesci(
    p_id IN NUMBER,
    p_ilosc IN FLOAT,
    p_miary_id IN NUMBER
)
AS
BEGIN
    -- Aktualizujemy wartość w kolumnie ILOSC
    UPDATE POZYCJA_CZESCI SET ILOSC = p_ilosc WHERE ID = p_id;
    -- Aktualizujemy wartość w kolumnie MIARY_ID
    UPDATE POZYCJA_CZESCI SET MIARY_ID = p_miary_id WHERE ID = p_id;
    COMMIT; -- Potwierdzamy zmiany
END;
/
-- ########################################################################
-- Obsluga tabeli Historia_Zmian
-- ########################################################################
--Sekwecja id Histori_Zmian
CREATE SEQUENCE SEQ.HISTORIA_ZMIAN
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

