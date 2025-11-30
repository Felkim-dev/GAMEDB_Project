from flask import Blueprint, request, jsonify, make_response
from services.inventory_services import (get_all_inventory, create_inventory, update_inventory, delete_inventory)
from schemas.inventory_schema import InventorySchema
from models import Inventory

inventory_bp = Blueprint('inventory_bp', __name__)

# Get all the inventory items
@inventory_bp.get('/')
def inventory_route():
    get_inventory = get_all_inventory()
    inventory_schema = InventorySchema(many=True)
    inventory = inventory_schema.dump(get_inventory)
    return make_response(jsonify({"inventory": inventory}))

# Get inventory item by ID
@inventory_bp.get('/<int:CharacterID>/<int:ItemID>')
def get_inventory_route(CharacterID, ItemID):
    inventory_item = Inventory.query.get((CharacterID, ItemID))
    if not inventory_item:
        return {"error": "Inventory item not found"}, 404
    
    inventory_schema = InventorySchema()
    inventory_json = inventory_schema.dump(inventory_item)
    return jsonify(inventory_json), 200

# Create inventory item
@inventory_bp.post('/')
def create_inventory_route():
    inventory_data = request.json
   
    try:
        new_inventory_data = InventorySchema().load(inventory_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400 
    # Add the new inventory item to the database
    new_inventory = create_inventory(new_inventory_data)
    # Serialize the created inventory schema and return the response
    if isinstance(new_inventory, Inventory):
        inventory_schema = InventorySchema()
        inventory_json = inventory_schema.dump(new_inventory)
        return jsonify(inventory_json), 201
    # Improve error handling for foreign key issues
    return jsonify({'error': str(new_inventory)}), 404

# Update inventory item
@inventory_bp.put('/<int:CharacterID>/<int:ItemID>')
def update_inventory_route(CharacterID, ItemID):
    inventory_item = Inventory.query.get((CharacterID, ItemID))
    if not inventory_item:
        return jsonify({'message': 'Inventory item not found'}), 404
    data = request.get_json()
    new_inventory = update_inventory(CharacterID, ItemID, data)
    if not new_inventory:
        return jsonify({'message': 'Inventory item not found'}), 404
    return jsonify({'message': 'Inventory item updated successfully'}), 200

# Delete inventory item
@inventory_bp.delete('/<int:CharacterID>/<int:ItemID>')
def delete_inventory_route(CharacterID, ItemID):
    inventory_item = Inventory.query.get((CharacterID, ItemID))
    if not inventory_item:
        return jsonify({'message': 'Inventory item not found'}), 404
    delete_inventory(CharacterID, ItemID)
    return jsonify({'message': 'Inventory item deleted successfully'}), 200

