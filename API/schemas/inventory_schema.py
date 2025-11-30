from marshmallow import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.inventory import Inventory
from app.extensions import db

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Inventory
        include_fk=True
        sqla_session=db.session
    CharacterID=fields.Integer(required=True)
    ItemID=fields.Integer(required=True)
    Quantity=fields.Integer(required=True)