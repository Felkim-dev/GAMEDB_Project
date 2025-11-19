from flask import Blueprint, request, jsonify,make_response
from services.character_services import get_all_characters,create_character,update_character,delete_character
from schemas.character_schema import CharacterSchema
from models import Character

character_bp=Blueprint('character_bp',__name__)

#Get all the characters
@character_bp.get('/')
def characters_route():
    get_characters=get_all_characters()
    characters_schema=CharacterSchema(many=True)
    characters=characters_schema.dump(get_characters)
    return make_response(jsonify({"characters":characters}))

#Get character by ID
@character_bp.get('/<int:CharacterID>')
def get_character_route(CharacterID):
    character=Character.query.get(CharacterID)
    if not character:
        return {"error": "Character not found"}, 404
    
    character_schema=CharacterSchema()
    character_json=character_schema.dump(character)
    return jsonify(character_json),200

#Create character
@character_bp.post('/')
def create_character_route():
    character_data=request.json
   
    try:
        new_character_data=CharacterSchema().load(character_data)
    except Exception as e:
        return jsonify({'error':str(e)}),400 
    #Add the new character to the data base
    new_character=create_character(new_character_data)
    #Serialize the created character schema and return the response
    if isinstance(new_character,Character):
        character_schema=CharacterSchema()
        character_json=character_schema.dump(new_character)
        return jsonify(character_json),201
    #Mejorar la forma en la que se imprime el error cuando la foreign Key no existe
    return jsonify({'error':str(new_character)}),404

#Update character
@character_bp.put('/<int:CharacterID>')
def update_character_route(CharacterID):
    character=Character.query.get(CharacterID)
    if not character:
        return jsonify({'message':'character not found'}),404
    data=request.get_json()
    new_character=update_character(CharacterID,data)
    if not new_character:
        return jsonify({'message':'Character not found'}),404
    return jsonify({'message':'Character updated succesfully'}),200

#Delete Character
@character_bp.delete('/<int:CharacterID>')
def delete_character_route(CharacterID):
    new_character=delete_character(CharacterID)
    if not new_character:
        return jsonify({'error':'Character not found'}),404
    return jsonify({'message':'Character deleted succesfully'}),200

