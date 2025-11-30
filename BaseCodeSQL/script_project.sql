CREATE DATABASE IF NOT EXISTS GAME_DATABASE;
USE GAME_DATABASE;

-- Tablas principales
CREATE TABLE `Player` (
    PlayerID INT NOT NULL AUTO_INCREMENT,
    UserName VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    RegistrationDate DATE NOT NULL,
    PRIMARY KEY (PlayerID),
    INDEX idx_email (Email),
    INDEX idx_username (UserName)
);

CREATE TABLE `Character` (
    CharacterID INT NOT NULL AUTO_INCREMENT,
    PlayerID INT NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Level INT NOT NULL DEFAULT 1 CHECK (Level > 0),
    Experience INT NOT NULL DEFAULT 0 CHECK (Experience >= 0),
    PRIMARY KEY (CharacterID),
    INDEX idx_player (PlayerID),
    INDEX idx_level (Level)
);

CREATE TABLE `Mission` (
    MissionID INT NOT NULL AUTO_INCREMENT,
    Title VARCHAR(100) NOT NULL,
    Description VARCHAR(1000) NOT NULL,
    Difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL DEFAULT 'Easy',
    PRIMARY KEY (MissionID),
    INDEX idx_difficulty (Difficulty)
);

CREATE TABLE `Item` (
    ItemID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Type ENUM('Arma', 'Armadura', 'Comestible', 'Coleccionables') NOT NULL,
    Rarity ENUM('Common', 'Special', 'Epic', 'Legendary') NOT NULL DEFAULT 'Common',
    PRIMARY KEY (ItemID),
    INDEX idx_type (Type),
    INDEX idx_rarity (Rarity)
);

-- Tablas de relación
CREATE TABLE `CharacterMission` (
    CharacterID INT NOT NULL,
    MissionID INT NOT NULL,
    Status ENUM('Incomplete', 'In Progress', 'Complete') NOT NULL DEFAULT 'Incomplete',
    StartDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CompletionDate DATETIME NULL,
    PRIMARY KEY (CharacterID, MissionID),
    INDEX idx_status (Status)
);

CREATE TABLE `Inventory` (
    CharacterID INT NOT NULL,
    ItemID INT NOT NULL,
    Quantity INT NOT NULL DEFAULT 1 CHECK (Quantity >= 0),
    AcquiredDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (CharacterID, ItemID)
);

-- Tabla de transacciones con conexión directa
CREATE TABLE `Transaction` (
    TransactionID INT NOT NULL AUTO_INCREMENT,
    ItemID INT NOT NULL,
    GiverID INT NOT NULL,
    ReceiverID INT NOT NULL,
    TransactionDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TransactionType ENUM('Trade', 'Purchase', 'Donation') NOT NULL,
    Quantity INT NOT NULL DEFAULT 1 CHECK (Quantity > 0),
    PRIMARY KEY (TransactionID),
    -- Prevenir auto-transacciones
    CONSTRAINT check_different_characters CHECK (GiverID != ReceiverID),
    INDEX idx_giver (GiverID),
    INDEX idx_receiver (ReceiverID),
    INDEX idx_date (TransactionDate),
    INDEX idx_item (ItemID),
    INDEX idx_type (TransactionType)
);

-- Foreign Keys
ALTER TABLE `Character` 
ADD CONSTRAINT fk_character_player
FOREIGN KEY (PlayerID) REFERENCES `Player`(PlayerID)
ON DELETE CASCADE;

ALTER TABLE `CharacterMission` 
ADD CONSTRAINT fk_cm_character
FOREIGN KEY (CharacterID) REFERENCES `Character`(CharacterID)
ON DELETE CASCADE;

ALTER TABLE `CharacterMission` 
ADD CONSTRAINT fk_cm_mission
FOREIGN KEY (MissionID) REFERENCES `Mission`(MissionID)
ON DELETE CASCADE;

ALTER TABLE `Inventory` 
ADD CONSTRAINT fk_inventory_character
FOREIGN KEY (CharacterID) REFERENCES `Character`(CharacterID)
ON DELETE CASCADE;

ALTER TABLE `Inventory` 
ADD CONSTRAINT fk_inventory_item
FOREIGN KEY (ItemID) REFERENCES `Item`(ItemID)
ON DELETE CASCADE;

-- Conexiones directas de Transaction con Character
ALTER TABLE `Transaction` 
ADD CONSTRAINT fk_transaction_giver
FOREIGN KEY (GiverID) REFERENCES `Character`(CharacterID)
ON DELETE RESTRICT;

ALTER TABLE `Transaction` 
ADD CONSTRAINT fk_transaction_receiver
FOREIGN KEY (ReceiverID) REFERENCES `Character`(CharacterID)
ON DELETE RESTRICT;

ALTER TABLE `Transaction` 
ADD CONSTRAINT fk_transaction_item
FOREIGN KEY (ItemID) REFERENCES `Item`(ItemID)
ON DELETE RESTRICT;
