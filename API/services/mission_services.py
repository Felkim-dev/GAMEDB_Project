from models.mission import Mission
from app.extensions import db

def get_all_missions():
    return Mission.query.all()

def create_mission(data):
    try: 
        mission = Mission(**data)
        db.session.add(mission)
        db.session.commit()
        return mission
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  # <-- imprime el error real
        return e

def update_mission(MissionID, data):
    mission=Mission.query.get(MissionID)
    if not mission:
        return None
    mission.Title=data.get("Title",mission.Title)
    mission.Description=data.get("Description",mission.Description)
    mission.Difficulty=data.get("Difficulty",mission.Difficulty)
    db.session.commit()
    return mission

def delete_mission(MissionID):
    mission=Mission.query.get(MissionID)
    if not mission:
        return None
    db.session.delete(mission)
    db.session.commit()
    return mission
    