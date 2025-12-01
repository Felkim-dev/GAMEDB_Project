from marshmallow import fields,validate
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
    Difficulty=fields.String(required=True,
                             validate=validate.OneOf(['Easy', 'Medium', 'Hard']))
