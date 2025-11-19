from models.item import Item
from app.extensions import db

def get_all_items():
    return Item.query.all()

def create_item(data):
    #TODO: Definir un create(aun no se como)
    pass
    