USE GAME_DATABASE;
-- Datos de prueba para GAME_DATABASE
USE GAME_DATABASE;

-- Players
INSERT INTO `Player` (`PlayerID`,`UserName`,`Email`,`RegistrationDate`) VALUES
(1,'alice','alice@example.com','2025-01-15'),
(2,'bob','bob@example.com','2025-02-20'),
(3,'carla','carla@example.com','2025-03-10');

-- Characters
INSERT INTO `Character` (`CharacterID`,`PlayerID`,`Name`,`Level`,`Experience`) VALUES
(1,1,'Alicia',5,1200),
(2,1,'Shadow',2,300),
(3,2,'Boris',10,5000),
(4,3,'Cara',1,0);

-- Missions
INSERT INTO `Mission` (`MissionID`,`Title`,`Description`,`Difficulty`) VALUES
(1,'Recolectar hierbas','Recoge 10 hierbas medicinales','Easy'),
(2,'Defender la aldea','Defiende la aldea de bandidos','Medium'),
(3,'Asaltar la fortaleza','Infiltra y toma la fortaleza enemiga','Hard');

-- Items
INSERT INTO `Item` (`ItemID`,`Name`,`Type`,`Rarity`) VALUES
(1,'Espada corta','Arma','Common'),
(2,'Armadura ligera','Armadura','Special'),
(3,'Poción de vida','Comestible','Common'),
(4,'Amuleto antiguo','Coleccionables','Legendary');

-- CharacterMission (relación personaje-misión)
INSERT INTO `CharacterMission` (`CharacterID`,`MissionID`,`Status`,`StartDate`,`CompletionDate`) VALUES
(1,1,'In Progress',NOW(),NULL),
(1,2,'Incomplete',NULL,NULL),
(3,2,'Complete','2025-05-01 10:00:00','2025-05-05 15:30:00');

-- Inventory
INSERT INTO `Inventory` (`CharacterID`,`ItemID`,`Quantity`,`AcquiredDate`) VALUES
(1,1,1,'2025-06-01 12:00:00'),
(1,3,5,'2025-06-02 09:00:00'),
(3,2,1,'2025-04-20 18:00:00'),
(4,4,1,'2025-07-10 08:00:00');

-- Transactions (asegurar GiverID != ReceiverID)
INSERT INTO `Transaction` (`TransactionID`,`ItemID`,`GiverID`,`ReceiverID`,`TransactionDate`,`TransactionType`,`Quantity`) VALUES
(1,3,1,2,'2025-06-03 10:00:00','Trade',1),
(2,4,3,4,'2025-07-11 09:30:00','Donation',1),
(3,1,3,1,'2025-05-15 14:00:00','Purchase',1);

-- Notas:
-- - Los IDs están fijados para facilitar referencias en pruebas; si prefieres
--   dejar que AUTO_INCREMENT asigne IDs, puedo actualizar el script
--   para no proporcionar valores de PK explícitos.
-- - Asegúrate de que `script_project.sql` ya fue ejecutado antes de correr
--   este script (creación de tablas y constraints).
