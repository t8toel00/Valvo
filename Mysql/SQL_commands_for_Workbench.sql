CREATE DATABASE valvo;
SHOW DATABASES;
USE valvo;
SET SQL_SAFE_UPDATES = 0;
SHOW TABLES;

SELECT sum(ihmiset_kpl) as ihmiset_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 168 HOUR AND lev != 'manual'
GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC;

SELECT sum(ihmiset_kpl), sum(odotettu_kpl), date_format(k_aika, '%H - %d/%m/%y') as datecreated
FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 168 HOUR
GROUP BY date_format(k_aika, '%H - %d/%m/%y') ORDER BY min(k_aika) ASC;

INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl, ) VALUES ('2019-11-29 10:44:50.111', '1', '0');
INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl, sisa_lkm, ulos_lkm, lev) VALUES ('2019-12-12 12:13:13.222', '2', '2', '1', '1', '70');
INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl, sisa_lkm, ulos_lkm, lev) VALUES ('2019-12-12 12:42:14.222', '500', '500', '500', '500', 'manual');
SELECT * FROM Alue;
SELECT * FROM Tunnistus;
SELECT count(*) FROM Tunnistus;
SELECT k_aika, kasvot_kpl FROM Tunnistus;
SELECT * FROM Arduino1;
SELECT * FROM Arduino2;
SELECT * FROM Tunnistus ORDER BY k_aika DESC;
SELECT * FROM Arduino1 ORDER BY a1_aika DESC;
SELECT * FROM Arduino2 ORDER BY a2_aika DESC;
SELECT TIME(k_aika) FROM Tunnistus;
SELECT DATE(k_aika) FROM Tunnistus;
DELETE FROM Arduino1 WHERE a1_etaisyys = '11';
DELETE FROM Tunnistus WHERE lev = 'manual';
INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES ('2019-11-12 10:16:11.999777', 'tulo', '555', '12');
INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES ('2019-11-12 10:16:11.955999', 'tulo', '555', '19');