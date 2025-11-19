from marshmallow import Schema, fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.item import Item
from app.extensions import db

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Item
        sqla_session=db.session
    ItemID=fields.Integer(dump_only=True)
    Name=fields.String(required=True)
    Type=fields.Integer(required=True)
    Rarity=fields.Integer(required=True)