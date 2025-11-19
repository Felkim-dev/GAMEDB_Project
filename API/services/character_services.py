from models.character import Character
from app.extensions import db

def get_all_characters():
    return Character.query.all()

def create_character(data):
    #TODO: Definir un create(aun no se como)
    pass
    