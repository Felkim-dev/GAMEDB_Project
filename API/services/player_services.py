from models.player import Player
from app.extensions import db

def get_all_players():
    return Player.query.all()

def create_player(data):
    #TODO: Definir un create(aun no se como)
    pass
    