CREATE SEQUENCE seq_czesci
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  NOCYCLE;
  
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