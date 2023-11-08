
CREATE TABLE czesci_maszyny_pt ( 
    id_maszyny NUMBER, 
    id_czesci  NUMBER, 
    maszyny_id NUMBER NOT NULL, 
    częsci_id  NUMBER NOT NULL 
);

ALTER TABLE czesci_maszyny_pt ADD CONSTRAINT czesci_maszyny_pt_id_maszyny_un UNIQUE ( id_maszyny );

ALTER TABLE czesci_maszyny_pt ADD CONSTRAINT czesci_maszyny_pt_id_czesci_un UNIQUE ( id_czesci );

CREATE TABLE częsci ( 
    id             NUMBER NOT NULL, 
    nazwa          CLOB, 
    id_typu        NUMBER, 
    parametr_1     CHAR(15 CHAR), 
    parametr_2     CHAR(15 CHAR), 
    parametr_3     CHAR(15 CHAR), 
    zdjecie        BLOB, 
    link_przyklad  CLOB, 
    typy_czesci_id NUMBER NOT NULL 
);

ALTER TABLE częsci ADD CONSTRAINT częsci_pk PRIMARY KEY ( id );

CREATE TABLE dzienik_napraw ( 
    id               NUMBER NOT NULL, 
    id_maszyny       NUMBER, 
    id_usterki       NUMBER, 
    data_wystopienia DATE, 
    id_naprawil      NUMBER, 
    dodatkowe_info   CLOB, 
    usterka_id       NUMBER NOT NULL, 
    uzytkownik_id    NUMBER NOT NULL, 
    maszyny_id       NUMBER NOT NULL 
);

ALTER TABLE dzienik_napraw ADD CONSTRAINT dzienik_napraw_pk PRIMARY KEY ( id );

CREATE TABLE etapy_zadan ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(20 CHAR) 
);

ALTER TABLE etapy_zadan ADD CONSTRAINT etapy_pk PRIMARY KEY ( id );

CREATE TABLE etapy_zamowienia ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(15 CHAR) 
);

ALTER TABLE etapy_zamowienia ADD CONSTRAINT etapy_zamowienia_pk PRIMARY KEY ( id );

CREATE TABLE historia_zmian ( 
    id                 NUMBER NOT NULL, 
    id_czesci          NUMBER, 
    id_pozycji         NUMBER, 
    data_zmiany        DATE, 
    id_rodzaju_zmiany  NUMBER, 
    id_uzytkownika     NUMBER, 
    dodatkowe_info     CLOB, 
    miejsce_pozycja_id NUMBER NOT NULL, 
    częsci_id          NUMBER NOT NULL, 
    rodzaj_zmiany_id   NUMBER NOT NULL, 
    uzytkownik_id      NUMBER NOT NULL 
);

ALTER TABLE historia_zmian ADD CONSTRAINT historia_zmian_pk PRIMARY KEY ( id );

CREATE TABLE kategorie_dostepu ( 
    id             NUMBER NOT NULL, 
    kategoria      NUMBER, 
    dodatkowe_info CLOB 
);

ALTER TABLE kategorie_dostepu ADD CONSTRAINT kategorie_dostepu_pk PRIMARY KEY ( id );

CREATE TABLE magazyn ( 
    id                NUMBER NOT NULL, 
    nazwa             CHAR(20 CHAR)
);

ALTER TABLE magazyn ADD CONSTRAINT magazyn_pk PRIMARY KEY ( id );

CREATE TABLE magazyn_miejsca ( 
    id                 NUMBER NOT NULL, 
    nazwa              CHAR(20 CHAR),
    magazyn_id  NUMBER NOT NULL 
);

ALTER TABLE magazyn_miejsca ADD CONSTRAINT magazyn_miejsca_pk PRIMARY KEY ( id );

CREATE TABLE maszyny ( 
    id             NUMBER NOT NULL, 
    dluga_nazwa    CHAR(40 CHAR), 
    krotka_nazwa   CHAR(8 CHAR), 
    id_typu        NUMBER, 
    producent      CHAR(15 CHAR), 
    Nr_Seryjny  CHAR(20 CHAR), 
    id_stanu       NUMBER, 
    stany_id       NUMBER NOT NULL, 
    typy_maszyn_id NUMBER NOT NULL 
);

ALTER TABLE maszyny ADD CONSTRAINT maszyny_pk PRIMARY KEY ( id );

CREATE TABLE miary ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(10 CHAR) 
);

ALTER TABLE miary ADD CONSTRAINT miary_pk PRIMARY KEY ( id );

CREATE TABLE miejsce_pozycja (
    id                 NUMBER NOT NULL,
    nazwa              NUMBER,
    dodatkowe_info     CHAR(100 CHAR),
    id_miejsca         NUMBER,
    magazyn_miejsca_id NUMBER NOT NULL
);;

ALTER TABLE miejsce_pozycja ADD CONSTRAINT miejsce_pozycja_pk PRIMARY KEY ( id );

CREATE TABLE pilnosc ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(10 CHAR), 
    tajne CHAR(1) 
);

ALTER TABLE pilnosc ADD CONSTRAINT pilnosc_pk PRIMARY KEY ( id );

CREATE TABLE pozycja_czesci ( 
    id_pozycji         NUMBER, 
    id_czesci          NUMBER, 
    ilosc              FLOAT, 
    id_miary           NUMBER, 
    miejsce_pozycja_id NUMBER NOT NULL, 
    częsci_id          NUMBER NOT NULL, 
    miary_id           NUMBER NOT NULL 
);

CREATE TABLE problemy ( 
    id               NUMBER NOT NULL, 
    id_maszyny       NUMBER, 
    id_stanu         NUMBER, 
    data             DATE, 
    opis             CLOB, 
    data_rozwiazania DATE, 
    stany_id         NUMBER NOT NULL, 
    maszyny_id       NUMBER NOT NULL 
);

ALTER TABLE problemy ADD CONSTRAINT problemy_pk PRIMARY KEY ( id );

CREATE TABLE przeglady ( 
    id             NUMBER NOT NULL, 
    id_maszyny     NUMBER, 
    id_uzytkownika NUMBER,    
    data_wykonania           DATE, 
    raport         BLOB, 
    uzytkownik_id  NUMBER NOT NULL, 
    maszyny_id     NUMBER NOT NULL 
);

ALTER TABLE przeglady ADD CONSTRAINT przeglady_pk PRIMARY KEY ( id );

CREATE TABLE rodzaj_zmiany ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(10 CHAR) 
);

ALTER TABLE rodzaj_zmiany ADD CONSTRAINT rodzaj_zmiany_pk PRIMARY KEY ( id );

CREATE TABLE stanowiska ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(40 CHAR) 
);

ALTER TABLE stanowiska ADD CONSTRAINT stanowiska_pk PRIMARY KEY ( id );

CREATE TABLE stany ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(15 CHAR) 
);

ALTER TABLE stany ADD CONSTRAINT stany_pk PRIMARY KEY ( id );

CREATE TABLE typy_czesci ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(10 CHAR) 
);

ALTER TABLE typy_czesci ADD CONSTRAINT typy_czesci_pk PRIMARY KEY ( id );

CREATE TABLE typy_maszyn ( 
    id    NUMBER NOT NULL, 
    nazwa CHAR(15 CHAR) 
);

ALTER TABLE typy_maszyn ADD CONSTRAINT typy_maszyn_pk PRIMARY KEY ( id );

CREATE TABLE usterka ( 
    id             NUMBER NOT NULL, 
    kod            CHAR(20 CHAR), 
    id_typumaszyny NUMBER, 
    opis           CLOB, 
    rozwiazanie    CLOB, 
    typy_maszyn_id NUMBER NOT NULL 
);

ALTER TABLE usterka ADD CONSTRAINT usterka_pk PRIMARY KEY ( id );

CREATE TABLE uzytkownik ( 
    id                   NUMBER NOT NULL, 
    nazwa                CHAR(30 CHAR), 
    id_stanowiska        NUMBER, 
    id_kategoria_dostepu NUMBER, 
    kategorie_dostepu_id NUMBER NOT NULL, 
    stanowiska_id        NUMBER NOT NULL 
);

ALTER TABLE uzytkownik ADD CONSTRAINT uzytkownik_pk PRIMARY KEY ( id );

CREATE TABLE zadania ( 
    id              NUMBER NOT NULL, 
    opis            CLOB, 
    id_zlecajacego  NUMBER, 
    id_wykonujacego NUMBER, 
    id_pilonosci    NUMBER, 
    data_zlecenia   DATE, 
    id_etapu        NUMBER, 
    data_wykonania  DATE, 
    uzytkownik_id   NUMBER NOT NULL, 
    uzytkownik_id1  NUMBER NOT NULL, 
    pilnosc_id      NUMBER NOT NULL, 
    etapy_id        NUMBER NOT NULL 
);

ALTER TABLE zadania ADD CONSTRAINT zadania_pk PRIMARY KEY ( id );

CREATE TABLE zamowienia ( 
    id                  NUMBER NOT NULL, 
    id_czesci           NUMBER, 
    id_etapu_zamowienia NUMBER, 
    data_zamowienia     DATE, 
    ilosc               FLOAT, 
    id_miary            NUMBER, 
    data_dostarczenia   DATE, 
    miary_id            NUMBER NOT NULL, 
    częsci_id           NUMBER NOT NULL, 
    etapy_zamowienia_id NUMBER NOT NULL 
);

ALTER TABLE zamowienia ADD CONSTRAINT zamowienia_pk PRIMARY KEY ( id );

ALTER TABLE czesci_maszyny_pt 
    ADD CONSTRAINT czesci_maszyny_pt_częsci_fk FOREIGN KEY ( częsci_id ) 
        REFERENCES częsci ( id );

ALTER TABLE czesci_maszyny_pt 
    ADD CONSTRAINT czesci_maszyny_pt_maszyny_fk FOREIGN KEY ( maszyny_id ) 
        REFERENCES maszyny ( id );

ALTER TABLE częsci 
    ADD CONSTRAINT częsci_typy_czesci_fk FOREIGN KEY ( typy_czesci_id ) 
        REFERENCES typy_czesci ( id );

ALTER TABLE dzienik_napraw 
    ADD CONSTRAINT dzienik_napraw_maszyny_fk FOREIGN KEY ( maszyny_id ) 
        REFERENCES maszyny ( id );

ALTER TABLE dzienik_napraw 
    ADD CONSTRAINT dzienik_napraw_usterka_fk FOREIGN KEY ( usterka_id ) 
        REFERENCES usterka ( id );

ALTER TABLE dzienik_napraw 
    ADD CONSTRAINT dzienik_napraw_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) 
        REFERENCES uzytkownik ( id );

ALTER TABLE historia_zmian 
    ADD CONSTRAINT historia_zmian_częsci_fk FOREIGN KEY ( częsci_id ) 
        REFERENCES częsci ( id );

ALTER TABLE historia_zmian 
    ADD CONSTRAINT miejsce_pozycja_fk FOREIGN KEY ( miejsce_pozycja_id ) 
        REFERENCES miejsce_pozycja ( id );

ALTER TABLE historia_zmian 
    ADD CONSTRAINT rodzaj_zmiany_fk FOREIGN KEY ( rodzaj_zmiany_id ) 
        REFERENCES rodzaj_zmiany ( id );

ALTER TABLE historia_zmian 
    ADD CONSTRAINT historia_zmian_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) 
        REFERENCES uzytkownik ( id );

ALTER TABLE magazyn_miejsca
    ADD CONSTRAINT magazyn_miejsca_magazyn_fk FOREIGN KEY ( magazyn_id )
        REFERENCES magazyn ( id );;

ALTER TABLE maszyny 
    ADD CONSTRAINT maszyny_stany_fk FOREIGN KEY ( stany_id ) 
        REFERENCES stany ( id );

ALTER TABLE maszyny 
    ADD CONSTRAINT maszyny_typy_maszyn_fk FOREIGN KEY ( typy_maszyn_id ) 
        REFERENCES typy_maszyn ( id );

ALTER TABLE pozycja_czesci 
    ADD CONSTRAINT pozycja_czesci_częsci_fk FOREIGN KEY ( częsci_id ) 
        REFERENCES częsci ( id );

ALTER TABLE pozycja_czesci 
    ADD CONSTRAINT pozycja_czesci_miary_fk FOREIGN KEY ( miary_id ) 
        REFERENCES miary ( id );

ALTER TABLE pozycja_czesci 
    ADD CONSTRAINT czesci_miejsce_pozycja_fk FOREIGN KEY ( miejsce_pozycja_id ) 
        REFERENCES miejsce_pozycja ( id );

ALTER TABLE problemy 
    ADD CONSTRAINT problemy_maszyny_fk FOREIGN KEY ( maszyny_id ) 
        REFERENCES maszyny ( id );

ALTER TABLE problemy 
    ADD CONSTRAINT problemy_stany_fk FOREIGN KEY ( stany_id ) 
        REFERENCES stany ( id );

ALTER TABLE przeglady 
    ADD CONSTRAINT przeglady_maszyny_fk FOREIGN KEY ( maszyny_id ) 
        REFERENCES maszyny ( id );

ALTER TABLE przeglady 
    ADD CONSTRAINT przeglady_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) 
        REFERENCES uzytkownik ( id );

ALTER TABLE usterka 
    ADD CONSTRAINT usterka_typy_maszyn_fk FOREIGN KEY ( typy_maszyn_id ) 
        REFERENCES typy_maszyn ( id );

ALTER TABLE uzytkownik 
    ADD CONSTRAINT uzytkownik_kat_dost_fk FOREIGN KEY ( kategorie_dostepu_id ) 
        REFERENCES kategorie_dostepu ( id );

ALTER TABLE uzytkownik 
    ADD CONSTRAINT uzytkownik_stanowiska_fk FOREIGN KEY ( stanowiska_id ) 
        REFERENCES stanowiska ( id );

ALTER TABLE zadania 
    ADD CONSTRAINT zadania_etapy_fk FOREIGN KEY ( etapy_id ) 
        REFERENCES etapy_zadan ( id );

ALTER TABLE zadania 
    ADD CONSTRAINT zadania_pilnosc_fk FOREIGN KEY ( pilnosc_id ) 
        REFERENCES pilnosc ( id );

ALTER TABLE zadania 
    ADD CONSTRAINT zadania_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) 
        REFERENCES uzytkownik ( id );

ALTER TABLE zadania 
    ADD CONSTRAINT zadania_uzytkownik_fkv1 FOREIGN KEY ( uzytkownik_id1 ) 
        REFERENCES uzytkownik ( id );

ALTER TABLE zamowienia 
    ADD CONSTRAINT zamowienia_częsci_fk FOREIGN KEY ( częsci_id ) 
        REFERENCES częsci ( id );

ALTER TABLE zamowienia 
    ADD CONSTRAINT zamowienia_etapy_zamowienia_fk FOREIGN KEY ( etapy_zamowienia_id ) 
        REFERENCES etapy_zamowienia ( id );

ALTER TABLE zamowienia 
    ADD CONSTRAINT zamowienia_miary_fk FOREIGN KEY ( miary_id ) 
        REFERENCES miary ( id );

ALTER TABLE miejsce_pozycja
    ADD CONSTRAINT miejsca_magazyn_miejsca_fk FOREIGN KEY ( magazyn_miejsca_id )
        REFERENCES magazyn_miejsca ( id );


