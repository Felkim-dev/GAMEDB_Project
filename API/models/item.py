from app.extensions import db

class Item(db.Model):
    #TODO: definir la clase
    __tablename__="Item"
    ItemID=db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(50), nullable=False)
    Type=db.Column(db.Integer, nullable=False)
    Rarity=db.Column(db.Integer, nullable=False)

    #Relaciones
    inventory_items = db.relationship("Inventory", back_populates="item")
    transactions = db.relationship("Transaction", back_populates="item_changed")
    
    #metodo para instanciar un objeto de tipo Item
    def __init__(self,Name,Type,Rarity):
        self.Name=Name
        self.Type=Type
        self.Rarity=Rarity
    #TODO: definir el def create en la carpeta services para estructura mas limpia