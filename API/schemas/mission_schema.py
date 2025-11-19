from marshmallow import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.mission import Mission
from app.extensions import db

class MissionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Mission
        sqla_session=db.session
    MissionID=fields.Integer(dump_only=True)
    Title=fields.String(required=True)
    Description=fields.String(required=True)
    Difficulty=fields.Integer(required=True)