from app.extensions import db

class Inventory(db.Model):
    __tablename__ = "Inventory"
    CharacterID = db.Column(db.Integer,db.ForeignKey("Character.CharacterID"), primary_key=True)
    ItemID = db.Column(db.Integer, db.ForeignKey("Item.ItemID"), primary_key=True)
    Quantity = db.Column(db.Integer, nullable=False)

    #Relaciones
    character = db.relationship("Character", back_populates="inventory_holders")
    item= db.relationship("Item", back_populates="inventory_items")

    def __init__(self,CharacterID, ItemID, Quantity):
        self.CharacterID = CharacterID
        self.ItemID = ItemID
        self.Quantity = Quantity
        