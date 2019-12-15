CREATE DATABASE valvo;
SHOW DATABASES;
USE valvo;

CREATE TABLE IF NOT EXISTS `valvo`.`Tunnistus` (
  `idTunnistus` INT(11) NOT NULL AUTO_INCREMENT,
  `k_aika` TIMESTAMP(3) NULL DEFAULT NULL,
  `ihmiset_kpl` VARCHAR(45) NULL DEFAULT NULL,
  `odotettu_kpl` VARCHAR(45) NULL DEFAULT NULL,
  `sisa_lkm` VARCHAR(45) NULL DEFAULT NULL,
  `ulos_lkm` VARCHAR(45) NULL DEFAULT NULL,
  `lev` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idTunnistus`))
ENGINE = InnoDB
AUTO_INCREMENT = 30000356
DEFAULT CHARACTER SET = latin1;

SET SQL_SAFE_UPDATES = 0;
SHOW TABLES;

SELECT sum(ihmiset_kpl) as ihmiset_kpl, date_format(k_aika, "%H - %d/%m/%y") as datecreated FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 168 HOUR AND lev != 'manual'
GROUP BY date_format(k_aika, "%H - %d/%m/%y") ORDER BY min(k_aika) ASC;

SELECT sum(ihmiset_kpl), sum(odotettu_kpl), date_format(k_aika, '%H - %d/%m/%y') as datecreated
FROM Tunnistus WHERE k_aika > NOW() - INTERVAL 168 HOUR
GROUP BY date_format(k_aika, '%H - %d/%m/%y') ORDER BY min(k_aika) ASC;

INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl, sisa_lkm, ulos_lkm, lev) VALUES ('2019-12-12 12:13:13.222', '2', '2', '1', '1', '70');
INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl, sisa_lkm, ulos_lkm, lev) VALUES ('2019-12-12 12:42:14.222', '500', '500', '500', '500', 'manual');
SELECT * FROM Tunnistus;
SELECT TIME(k_aika) FROM Tunnistus;
SELECT DATE(k_aika) FROM Tunnistus;
DELETE FROM Arduino1 WHERE a1_etaisyys = '11';
DELETE FROM Tunnistus WHERE lev = 'manual';