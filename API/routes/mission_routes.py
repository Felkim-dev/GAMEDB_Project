from flask import Blueprint, request, jsonify,make_response
from services.mission_services import get_all_missions,create_mission,update_mission,delete_mission
from schemas.mission_schema import MissionSchema
from models import Mission

mission_bp=Blueprint('mission_bp',__name__)

#Get all the missions
@mission_bp.get('/')
def missions_route():
    get_missions=get_all_missions()
    missions_schema=MissionSchema(many=True)
    missions=missions_schema.dump(get_missions)
    return make_response(jsonify({"missions":missions}))

#Get mission by ID
@mission_bp.get('/<int:MissionID>')
def get_mission_route(MissionID):
    mission=Mission.query.get(MissionID)
    if not mission:
        return {"error": "Mission not found"}, 404
    
    mission_schema=MissionSchema()
    mission_json=mission_schema.dump(mission)
    return jsonify(mission_json),200

#Create mission
@mission_bp.post('/')
def create_mission_route():
    mission_data=request.json
   
    try:
        new_mission_data=MissionSchema().load(mission_data)
    except Exception as e:
        return jsonify({'error':str(e)}),400 
    #Add the new mission to the data base
    new_mission=create_mission(new_mission_data)
    #Serialize the created mission schema and return the response
    if isinstance(new_mission,Mission):
        mission_schema=MissionSchema()
        mission_json=mission_schema.dump(new_mission)
        return jsonify(mission_json),201
    #Mejorar la forma en la que se imprime el error cuando la foreign Key no existe
    return jsonify({'error':str(new_mission)}),404

#Update mission
@mission_bp.put('/<int:MissionID>')
def update_mission_route(MissionID):
    mission=Mission.query.get(MissionID)
    if not mission:
        return jsonify({'message':'mission not found'}),404
    data=request.get_json()
    new_mission=update_mission(MissionID,data)
    if not new_mission:
        return jsonify({'message':'Mission not found'}),404
    return jsonify({'message':'Mission updated succesfully'}),200

#Delete Mission
@mission_bp.delete('/<int:MissionID>')
def delete_mission_route(MissionID):
    new_mission=delete_mission(MissionID)
    if not new_mission:
        return jsonify({'error':'Mission not found'}),404
    return jsonify({'message':'Mission deleted succesfully'}),200

