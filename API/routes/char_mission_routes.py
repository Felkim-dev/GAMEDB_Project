from flask import Blueprint, request, jsonify, make_response
from services.char_mission_services import get_all_character_missions,delete_character_mission,create_character_mission,update_character_mission
from schemas.char_mission_schema import CharacterMissionSchema
from models import CharacterMission

char_mission_bp=Blueprint('char_mission_bp',__name__)
#Get all the character missions
@char_mission_bp.get('/')
def char_missions_route():
    get_char_missions=get_all_character_missions()
    char_missions_schema=CharacterMissionSchema(many=True)
    char_missions=char_missions_schema.dump(get_char_missions)
    return make_response(jsonify({"character_missions":char_missions}))

#Get character mission by ID
@char_mission_bp.get('/<int:CharacterID>/<int:MissionID>')
def get_char_mission_route(CharacterID,MissionID):
    char_mission_item=CharacterMission.query.get((CharacterID,MissionID))
    if not char_mission_item:
        return {"error":"Character Mission not found"},404
    
    char_mission_schema=CharacterMissionSchema()
    char_mission_json=char_mission_schema.dump(char_mission_item)
    return jsonify(char_mission_json),200

#Create character mission
@char_mission_bp.post('/')
def create_char_mission_route():
    char_mission_data=request.json
   
    try:
        new_char_mission_data=CharacterMissionSchema().load(char_mission_data)
    except Exception as e:
        return jsonify({'error':str(e)}),400 
    #Add the new character mission to the data base
    new_char_mission=create_character_mission(new_char_mission_data)
    #Serialize the created character mission schema and return the response
    if isinstance(new_char_mission,CharacterMission):
        char_mission_schema=CharacterMissionSchema()
        char_mission_json=char_mission_schema.dump(new_char_mission)
        return jsonify(char_mission_json),201
    #Mejorar la forma en la que se imprime el error cuando la foreign Key no existe
    return jsonify({'error':str(new_char_mission)}),404

#Update character mission
@char_mission_bp.put('/<int:CharacterID>/<int:MissionID>')
def update_char_mission_route(CharacterID,MissionID):
    char_mission=CharacterMission.query.get((CharacterID,MissionID))
    if not char_mission:
        return jsonify({'message':'character mission not found'}),404
    data=request.get_json()
    new_char_mission=update_character_mission(CharacterID,MissionID,data)
    if not new_char_mission:
        return jsonify({'message':'Character Mission not found'}),404
    return jsonify({'message':'Character Mission updated succesfully'}),200
#Delete character mission
@char_mission_bp.delete('/<int:CharacterID>/<int:MissionID>')
def delete_char_mission_route(CharacterID,MissionID):
    char_mission=CharacterMission.query.get((CharacterID,MissionID))
    if not char_mission:
        return jsonify({'message':'character mission not found'}),404
    delete_character_mission(CharacterID,MissionID)
    return jsonify({'message':'Character Mission deleted succesfully'}),200

