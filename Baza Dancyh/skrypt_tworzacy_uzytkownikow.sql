CREATE USER c##admin IDENTIFIED BY dbpass2;

GRANT CREATE SESSION TO c##admin;


GRANT CREATE TABLE TO c##admin;


GRANT ALTER ANY TABLE TO c##admin;


GRANT CREATE VIEW TO c##admin;


GRANT CREATE PROCEDURE TO c##admin;


GRANT CREATE TRIGGER TO c##admin;


GRANT CREATE USER TO c##admin;


GRANT ALTER USER TO c##admin;


GRANT DBA TO c##admin;


COMMIT;

