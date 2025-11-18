CREATE DATABASE GAME_DATABASE;
USE GAME_DATABASE;

CREATE TABLE Mission (
    MissionID INT NOT NULL AUTO_INCREMENT,
    Title VARCHAR(100) NOT NULL,
    Description VARCHAR(1000) NOT NULL,
    Difficulty INT NOT NULL,
    PRIMARY KEY (MissionID)
);

CREATE TABLE Item (
    ItemID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Type INT NOT NULL,
    Rarity INT NOT NULL,
    PRIMARY KEY (ItemID)
);

CREATE TABLE Player (
    PlayerID INT NOT NULL AUTO_INCREMENT,
    UserName VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    RegistrationDate DATE NOT NULL,
    PRIMARY KEY (PlayerID)
);

CREATE TABLE Character_1 (
    CharacterID INT NOT NULL AUTO_INCREMENT,
    PlayerID INT NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Level INT NOT NULL,
    Experience INT NOT NULL,
    PRIMARY KEY (CharacterID)
);

-- Tablas intermedias (ReceiverID = CharacterID)
CREATE TABLE Receiver (
    ReceiverID INT NOT NULL,
    PRIMARY KEY (ReceiverID)
);

CREATE TABLE Giver (
    GiverID INT NOT NULL,
    PRIMARY KEY (GiverID)
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

CREATE TABLE CharacterMission (
    CharacterID INT NOT NULL,
    MissionID INT NOT NULL,
    Status INT NOT NULL,
    PRIMARY KEY (CharacterID, MissionID)
);

CREATE TABLE Inventory (
    CharacterID INT NOT NULL,
    ItemID INT NOT NULL,
    Quantity INT NOT NULL,
    PRIMARY KEY (CharacterID, ItemID)  -- Corregido
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

ALTER TABLE Giver 
ADD CONSTRAINT character_1_giver_fk
FOREIGN KEY (GiverID) REFERENCES Character_1(CharacterID);

ALTER TABLE Receiver 
ADD CONSTRAINT character_1_receiver_fk
FOREIGN KEY (ReceiverID) REFERENCES Character_1(CharacterID);

ALTER TABLE Transaction 
ADD CONSTRAINT receiver_transaction_fk
FOREIGN KEY (ReceiverID) REFERENCES Receiver(ReceiverID);

ALTER TABLE Transaction 
ADD CONSTRAINT giver_transaction_fk
FOREIGN KEY (GiverID) REFERENCES Giver(GiverID);