
INSERT INTO Magazyn (ID, NAZWA) VALUES (1, 'Magazyn Części');

INSERT INTO Magazyn (ID, NAZWA) VALUES (2, 'Warsztat');

INSERT INTO Magazyn (ID, NAZWA) VALUES (3, 'Magazynek G. Rybaka');

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (1, 'Regał‚ I', 1);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (2, 'Regał‚ II', 1);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (3, 'Regał‚ III', 1);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (4, 'Regał‚ IV', 1);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (5, 'Biurko', 2);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (6, 'Lewy Regał‚', 2);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (7, 'Prawy Regał‚', 2);

INSERT INTO MAGAZYN_MIEJSCA (ID, NAZWA, MAGAZYN_ID) VALUES (8, 'Koszyczki', 2);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (1, 'Sekcja A', 1);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (2, 'Sekcja A', 2);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (3, 'Sekcja B', 2);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (4, 'Sekcja A', 3);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (5, 'Sekcja B', 3);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (6, 'Sekcja C', 3);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (7, 'Sekcja A', 4);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (8, 'Sekcja B', 4);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (9, 'Sekcja C', 4);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (10, 'Sekcja D', 4);

INSERT INTO MIEJSCE_POZYCJA (ID, NAZWA, MAGAZYN_MIEJSCA_ID) VALUES (11, 'Sekcja E', 4);

INSERT INTO MIARY (ID, NAZWA) VALUES (1, 'szt');

INSERT INTO MIARY (ID, NAZWA) VALUES (2, 'cm');

INSERT INTO MIARY (ID, NAZWA) VALUES (3, 'm');

INSERT INTO MIARY (ID, NAZWA) VALUES (4, 'op');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (1, 'Elektryczne', 'bezpiecznik');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (2, 'Elektryczne', 'kontrakton');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (3, 'Elektryczne', 'czujnik');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (4, 'Elektryczne', 'typ Ea');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (5, 'Pneumatyczne', 'ElektorZawór');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (6, 'Pneumatyczne', 'Siłownik');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (7, 'Pneumatyczne', 'SzybkoZłączka');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (8, 'Pneumatyczne', 'typ Pa');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (9, 'Mechaniczne', 'frez');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (10, 'Mechaniczne', 'wiertło');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (11, 'Mechaniczne', 'chwytak');

INSERT INTO TYPY_CZESCI (ID, NAZWA, POD_NAZWA) VALUES (12, 'Mechaniczne', 'typ Ma');

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (1, 'Bezpiecznik 16A', 1, '16A', 'Wielkość - D01', 'Char - gG', NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (2, 'frez 5x5', 9, 'ostrze 5 mm', 'podstawa 5mm', NULL, NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (3, 'frez 8x5', 9, 'ostrze 5 mm', 'podstawa 8mm', NULL, NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (4, 'Eti 12H8', 3, 'NO', '3 Piny', 'Laserowy', NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (5, 'Część A', 4, 'ParA', 'ParB', NULL, NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (6, 'Część B', 8, 'ParA', 'ParB', NULL, NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (7, 'Część C', 8, 'ParA', 'ParB', NULL, NULL, NULL);

INSERT INTO CZESCI (seq_czesci.NEXTVAL, NAZWA, TYPY_CZESCI_ID, PARAMETR_1, PARAMETR_2, PARAMETR_3, ZDJECIE, LINK_PRZYKLAD) VALUES (8, 'Część D', 12, 'ParA', 'ParB', NULL, NULL, NULL);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (7, 'Półka 2', 1, 10, 1);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (1, 'Półka 1', 2, 5, 1);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (1, 'Półka 2', 3, 4, 1);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (5, 'Półka 4, W kartonie', 4, 20, 1);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (5, 'Półka 3', 5, 2, 1);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (3, 'Półka 3', 6, 10, 3);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (3, 'Półka 4', 7, 20, 4);

INSERT INTO POZYCJA_CZESCI (MIEJSCE_POZYCJA_ID, DODATKOWE_INFO, CZESCI_ID, ILOSC, MIARY_ID) VALUES (9, 'Półka 1', 8, 5, 1);

INSERT INTO RODZAJ_ZMIANY (ID, NAZWA) VALUES (1, 'Dodano');

INSERT INTO RODZAJ_ZMIANY (ID, NAZWA) VALUES (2, 'Pobrano');

INSERT INTO RODZAJ_ZMIANY (ID, NAZWA) VALUES (3, 'Zmieniono');
