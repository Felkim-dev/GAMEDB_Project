from marshmallow import Schema, fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.player import Player
from app.extensions import db

class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Player
        sqla_session=db.session
    player_id=fields.Integer(dump_only=True)
    username=fields.String(required=True)
    email=fields.String(required=True)
    registration_date=fields.Date(required=True)