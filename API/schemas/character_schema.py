from marshmallow import Schema, fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.character import Character
from app.extensions import db

class CharacterSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Character
        sqla_session=db.session
    CharacterID=fields.Integer(dump_only=True)
    PlayerID=fields.Integer(required=True)
    Name=fields.String(required=True)
    Level=fields.Integer(required=True)
    Experience=fields.Integer(required=True)