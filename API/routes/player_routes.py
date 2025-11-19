from flask import Blueprint, request, jsonify,make_response
from services.player_services import get_all_players,create_player,update_player,delete_player
from schemas.player_schema import PlayerSchema
from models import Player


player_bp=Blueprint('player_bp',__name__)

#Get all the players
@player_bp.get('/')
def players_route():
    get_players=get_all_players()
    players_schema=PlayerSchema(many=True)
    players=players_schema.dump(get_players)
    return make_response(jsonify({"players":players}))

#Get player by ID
@player_bp.get('/<int:PlayerID>')
def get_player_route(PlayerID):
    player=Player.query.get(PlayerID)
    if not player:
        return {"error": "Player not found"}, 404
    
    player_schema=PlayerSchema()
    player_json=player_schema.dump(player)
    return jsonify(player_json),200

#Create player
@player_bp.post('/')
def create_player_route():
    player_data=request.json
   
    try:
        new_player_data=PlayerSchema().load(player_data)
    except Exception as e:
        return jsonify({'error':str(e)}),400 
    #Add the new player to the data base
    new_player=create_player(new_player_data)
    #Serialize the created player schema and return the response
    player_schema=PlayerSchema()
    player_json=player_schema.dump(new_player)
    return jsonify(player_json),201

#Update player
@player_bp.put('/<int:PlayerID>')
def update_player_route(PlayerID):
    player=Player.query.get(PlayerID)
    if not player:
        return jsonify({'message':'player not found'}),404
    data=request.get_json()
    new_player=update_player(PlayerID,data)
    if not new_player:
        return jsonify({'message':'Player not found'}),404
    return jsonify({'message':'Player updated succesfully'}),200

#Delete Player
@player_bp.delete('/<int:PlayerID>')
def delete_player_route(PlayerID):
    new_player=delete_player(PlayerID)
    if not new_player:
        return jsonify({'error':'Player not found'}),404
    return jsonify({'message':'Player deleted succesfully'}),200