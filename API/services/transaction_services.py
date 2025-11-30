from models.transaction import Transaction
from app.extensions import db

def get_all_transactions():
    return Transaction.query.all()
def create_transaction(data):
    try: 
        transaction = Transaction(**data)
        db.session.add(transaction)
        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)  # <-- imprime el error real
        return e

def update_transaction(TransactionID, data):
    transaction=Transaction.query.get(TransactionID)
    if not transaction:
        return None
    transaction.GiverID=data.get("GiverID",transaction.GiverID)
    transaction.ReceiverID=data.get("ReceiverID",transaction.ReceiverID)
    transaction.ItemID=data.get("ItemID",transaction.ItemID)
    transaction.TransactionDate=data.get("TransactionDate",transaction.TransactionDate)
    transaction.TransactionType=data.get("TransactionType",transaction.TransactionType)
    db.session.commit()
    return transaction

def delete_transaction(TransactionID):
    transaction=Transaction.query.get(TransactionID)
    if not transaction:
        return None
    db.session.delete(transaction)
    db.session.commit()
    return transaction
