from marshmallow import Schema, fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.player import Player
from app.extensions import db

class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Player
        sqla_session=db.session
    PlayerID=fields.Integer(dump_only=True)
    UserName=fields.String(required=True)
    Email=fields.String(required=True)
    RegistrationDate=fields.Date(required=True)