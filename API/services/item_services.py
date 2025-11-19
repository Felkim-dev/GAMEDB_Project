from models.item import Item
from app.extensions import db

def get_all_items():
    return Item.query.all()

def create_item(data):
    try: 
        item = Item(**data)
        db.session.add(item)
        db.session.commit()
        return item
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  # <-- imprime el error real
        return None 

def update_item(ItemID, data):
    item=Item.query.get(ItemID)
    if not item:
        return None
    item.Name=data.get("Name",item.Name)
    item.Type=data.get("Type",item.Type)
    item.Rarity=data.get("Rarity",item.Rarity)
    db.session.commit()
    return item

def delete_item(ItemID):
    item=Item.query.get(ItemID)
    if not item:
        return None
    db.session.delete(item)
    db.session.commit()
    return item
    