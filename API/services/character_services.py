from models.character import Character
from app.extensions import db

def get_all_characters():
    return Character.query.all()

def create_character(data):
    try: 
        character = Character(**data)
        db.session.add(character)
        db.session.commit()
        return character
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  # <-- imprime el error real
        return e

def update_character(CharacterID, data):
    character=Character.query.get(CharacterID)
    if not character:
        return None
    character.Name=data.get("Name",character.Name)
    character.PlayerID=data.get("PlayerID",character.PlayerID)
    character.Level=data.get("Level",character.Level)
    character.Experience=data.get("Experience",character.Experience)
    db.session.commit()
    return character

def delete_character(CharacterID):
    character=Character.query.get(CharacterID)
    if not character:
        return None
    db.session.delete(character)
    db.session.commit()
    return character
    