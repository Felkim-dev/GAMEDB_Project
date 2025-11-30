from flask import Blueprint, request, jsonify, make_response
from services.transaction_services import (get_all_transactions,
                                           create_transaction,update_transaction,
                                           delete_transaction)
from schemas.transaction_schema import TransactionSchema
from models import Transaction

transaction_bp = Blueprint('transaction_bp', __name__)

# Get all the transactions
@transaction_bp.get('/')
def transactions_route():
    get_transactions = get_all_transactions()
    transactions_schema = TransactionSchema(many=True)
    transactions = transactions_schema.dump(get_transactions)
    return make_response(jsonify({"transactions": transactions}))

# Get transaction by ID
@transaction_bp.get('/<int:TransactionID>')
def get_transaction_route(TransactionID):
    transaction = Transaction.query.get(TransactionID)
    if not transaction:
        return {"error": "Transaction not found"}, 404

    transaction_schema = TransactionSchema()
    transaction_json = transaction_schema.dump(transaction)
    return jsonify(transaction_json), 200

# Create transaction
@transaction_bp.post('/')
def create_transaction_route():
    transaction_data = request.json

    try:
        new_transaction_data = TransactionSchema().load(transaction_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    # Add the new transaction to the data base
    new_transaction = create_transaction(new_transaction_data)
    # Serialize the created transaction schema and return the response
    if isinstance(new_transaction, Transaction):
        transaction_schema = TransactionSchema()
        transaction_json = transaction_schema.dump(new_transaction)
        return jsonify(transaction_json), 201
    # Mejorar la forma en la que se imprime el error cuando la foreign Key no existe
    return jsonify({'error': str(new_transaction)}), 404

# Update transaction
@transaction_bp.put('/<int:TransactionID>')
def update_transaction_route(TransactionID):
    transaction = Transaction.query.get(TransactionID)
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    data = request.get_json()
    new_transaction = update_transaction(TransactionID, data)
    if not new_transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    return jsonify({'message': 'Transaction updated successfully'}), 200

# Delete Transaction
@transaction_bp.delete('/<int:TransactionID>')
def delete_transaction_route(TransactionID):
    new_transaction = delete_transaction(TransactionID)
    if not new_transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    return jsonify({'message': 'Transaction deleted successfully'}), 200

