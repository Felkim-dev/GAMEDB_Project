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

CREATE TABLE Transaction (
    TransactionID INT NOT NULL AUTO_INCREMENT,
    ItemID INT NOT NULL,
    ReceiverID INT NOT NULL,
    GiverID INT NOT NULL,
    TransactionDate DATE NOT NULL,
    TransactionType INT NOT NULL,
    PRIMARY KEY (TransactionID)
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

-- Foreign Keys
ALTER TABLE CharacterMission 
ADD CONSTRAINT mission_charactermission_fk
FOREIGN KEY (MissionID) REFERENCES Mission(MissionID);

ALTER TABLE Inventory 
ADD CONSTRAINT item_inventory_fk
FOREIGN KEY (ItemID) REFERENCES Item(ItemID);

ALTER TABLE Transaction 
ADD CONSTRAINT item_transaction_fk
FOREIGN KEY (ItemID) REFERENCES Item(ItemID);

ALTER TABLE Character_1 
ADD CONSTRAINT player_character_1_fk
FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID);

ALTER TABLE Inventory 
ADD CONSTRAINT character_inventory_fk
FOREIGN KEY (CharacterID) REFERENCES Character_1(CharacterID);

ALTER TABLE CharacterMission 
ADD CONSTRAINT character_charactermission_fk
FOREIGN KEY (CharacterID) REFERENCES Character_1(CharacterID);

ALTER TABLE Transaction 
ADD CONSTRAINT receiver_transaction_fk
FOREIGN KEY (ReceiverID) REFERENCES Character_1(CharacterID);

ALTER TABLE Transaction 
ADD CONSTRAINT giver_transaction_fk
FOREIGN KEY (GiverID) REFERENCES Character_1(CharacterID);
