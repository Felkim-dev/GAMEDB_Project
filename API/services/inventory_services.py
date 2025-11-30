from models.inventory import Inventory
from app.extensions import db

def get_all_inventory():
    return Inventory.query.all()

def create_inventory(data):
    try: 
        inventory = Inventory(**data)
        db.session.add(inventory)
        db.session.commit()
        return inventory
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  # <-- imprime el error real
        return e

def update_inventory(CharacterID, ItemID, data):
    inventory=Inventory.query.get((CharacterID, ItemID))
    if not inventory:
        return None
    inventory.Quantity=data.get("Quantity",inventory.Quantity)
    db.session.commit()
    return inventory

def delete_inventory(CharacterID, ItemID):
    inventory=Inventory.query.get((CharacterID, ItemID))
    if not inventory:
        return None
    db.session.delete(inventory)
    db.session.commit()
    return inventory
