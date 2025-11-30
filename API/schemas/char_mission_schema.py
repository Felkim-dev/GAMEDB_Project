from marshmallow import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.char_mission import CharacterMission
from app.extensions import db

class CharacterMissionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = CharacterMission
        include_fk = True
        sqla_session = db.session

    CharacterID = fields.Integer(required=True)
    MissionID = fields.Integer(required=True)
    Status = fields.Integer(required=True)