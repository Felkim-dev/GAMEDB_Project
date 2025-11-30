from app.extensions import db

class Transaction(db.Model):
    __tablename__="Transaction"
    TransactionID=db.Column(db.Integer, primary_key=True)
    GiverID=db.Column(db.Integer, db.ForeignKey('Character.CharacterID'), nullable=False)
    ReceiverID=db.Column(db.Integer, db.ForeignKey('Character.CharacterID'), nullable=False)
    ItemID=db.Column(db.Integer, db.ForeignKey('Item.ItemID'), nullable=False)
    TransactionDate=db.Column(db.Date, nullable=False)
    TransactionType=db.Column(db.Integer, nullable=False)

    #Relaciones
    giver = db.relationship("Character", foreign_keys=[GiverID], back_populates="given_transactions")
    receiver = db.relationship("Character", foreign_keys=[ReceiverID], back_populates="received_transactions")
    item_changed = db.relationship("Item", back_populates="transactions")


    #metodo para instanciar un objeto de tipo Transaction
    def __init__(self,GiverID,ReceiverID,ItemID,TransactionDate,TransactionType):
        self.GiverID=GiverID 
        self.ReceiverID=ReceiverID
        self.ItemID=ItemID
        self.TransactionDate=TransactionDate
        self.TransactionType=TransactionType
        