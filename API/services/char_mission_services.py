from models.char_mission import CharacterMission
from app.extensions import db

def get_all_character_missions():
    return CharacterMission.query.all()
def create_character_mission(data):
    try: 
        char_mission = CharacterMission(**data)
        db.session.add(char_mission)
        db.session.commit()
        return char_mission
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  # <-- imprime el error real
        return e
def update_character_mission(CharacterID, MissionID, data):
    char_mission=CharacterMission.query.get((CharacterID, MissionID))
    if not char_mission:
        return None
    char_mission.Status=data.get("Status",char_mission.Status)
    db.session.commit()
    return char_mission

def delete_character_mission(CharacterID, MissionID):
    char_mission=CharacterMission.query.get((CharacterID, MissionID))
    if not char_mission:
        return None
    db.session.delete(char_mission)
    db.session.commit()
    return char_mission

