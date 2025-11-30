from marshmallow import fields, validate
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from models.transaction import Transaction
from app.extensions import db

class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model=Transaction
        include_fk=True
        sqla_session=db.session
    TransactionID=fields.Integer(dump_only=True)
    GiverID=fields.Integer(required=True)
    ReceiverID=fields.Integer(required=True)
    ItemID=fields.Integer(required=True)
    TransactionDate=fields.Date(required=True)
    TransactionType=fields.String(required=True,
                                  validate=validate.OneOf(['Trade', 'Purchase', 'Donation']))