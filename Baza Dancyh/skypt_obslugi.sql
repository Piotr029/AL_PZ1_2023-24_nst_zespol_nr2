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
