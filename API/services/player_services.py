from models.player import Player
from app.extensions import db

def get_all_players():
    return Player.query.all()

def create_player(data):
    try: 
        player = Player(**data)
        db.session.add(player)
        db.session.commit()
        return player
    except Exception as e:
        db.session.rollback()   
        return e 

def update_player(PlayerID, data):
    player=Player.query.get(PlayerID)
    if not player:
        return None
    player.UserName=data.get("UserName",player.UserName)
    player.Email=data.get("Email",player.Email)
    player.RegistrationDate=data.get("RegistrationDate",player.RegistrationDate)
    db.session.commit()
    return player

def delete_player(PlayerID):
    player=Player.query.get(PlayerID)
    if not player:
        return None
    db.session.delete(player)
    db.session.commit()
    return player
    