from flask import Blueprint, request, jsonify,make_response
from services.player_services import get_all_players,create_player
from schemas.player_schema import PlayerSchema
player_bp=Blueprint('player_bp',__name__)


@player_bp.get('/')
def players():
    get_players=get_all_players()
    players_schema=PlayerSchema(many=True)
    players=players_schema.dump(get_players)
    return make_response(jsonify({"players":players}))