from marshmallow import fields, validate
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.item import Item
from app.extensions import db

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Item
        sqla_session=db.session
    ItemID=fields.Integer(dump_only=True)
    Name=fields.String(required=True)
    Type=fields.String(required=True,
                       validate=validate.OneOf(['Arma', 'Armadura', 'Comestible', 'Coleccionables']))
    Rarity=fields.String(required=True,
                        validate=validate.OneOf(['Common', 'Special', 'Epic', 'Legendary']))