CREATE DATABASE valvo;
SHOW DATABASES;
USE valvo;
SET SQL_SAFE_UPDATES = 0;
SHOW TABLES;
SELECT sum(ihmiset_kpl), date_format(k_aika, '%H - %d/%m/%y') as datecreated
FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 24 HOUR
GROUP BY date_format(k_aika, '%H - %d/%m/%y') ORDER BY min(k_aika) ASC;
INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl) VALUES ('2019-11-26 13:51:12.122', '1', '3');
SELECT * FROM Alue;
SELECT * FROM Tunnistus;
SELECT k_aika, kasvot_kpl FROM Tunnistus;
SELECT * FROM Arduino1;
SELECT * FROM Arduino2;
SELECT * FROM Tunnistus ORDER BY k_aika DESC;
SELECT * FROM Arduino1 ORDER BY a1_aika DESC;
SELECT * FROM Arduino2 ORDER BY a2_aika DESC;
SELECT TIME(k_aika) FROM Tunnistus;
SELECT DATE(k_aika) FROM Tunnistus;
DELETE FROM Arduino1 WHERE a1_etaisyys = '11';
DELETE FROM Tunnistus WHERE kasvot_kpl = '0' or '1' or '2' or 'testi';
INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES ('2019-11-12 10:16:11.999777', 'tulo', '555', '12');
INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES ('2019-11-12 10:16:11.955999', 'tulo', '555', '19');