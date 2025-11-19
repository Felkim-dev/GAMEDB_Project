from app.extensions import db

class Item(db.Model):
    #TODO: definir la clase
    __tablename__="Item"
    item_id=db.Column(db.Integer, primary_key=True)
    item_name=db.Column(db.String(50), nullable=False)
    item_type=db.Column(db.Integer, nullable=False)
    item_rarity=db.Column(db.Integer, nullable=False)

    #metodo para instanciar un objeto de tipo Item
    def __init__(self,item_name,item_type,item_rarity):
        self.item_name=item_name
        self.item_type=item_type
        self.item_rarity=item_rarity
    #TODO: definir el def create en la carpeta services para estructura mas limpia