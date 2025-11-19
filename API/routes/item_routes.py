from flask import Blueprint, request, jsonify,make_response
from services.item_services import get_all_items,create_item,update_item,delete_item
from schemas.item_schema import ItemSchema
from models import Item


item_bp=Blueprint('item_bp',__name__)

#Get all the items
@item_bp.get('/')
def items_route():
    get_items=get_all_items()
    items_schema=ItemSchema(many=True)
    items=items_schema.dump(get_items)
    return make_response(jsonify({"items":items}))

#Get item by ID
@item_bp.get('/<int:ItemID>')
def get_item_route(ItemID):
    item=Item.query.get(ItemID)
    if not item:
        return {"error": "Item not found"}, 404
    
    item_schema=ItemSchema()
    item_json=item_schema.dump(item)
    return jsonify(item_json),200

#Create item
@item_bp.post('/')
def create_item_route():
    item_data=request.json
   
    try:
        new_item_data=ItemSchema().load(item_data)
    except Exception as e:
        return jsonify({'error':str(e)}),400 
    #Add the new item to the data base
    new_item=create_item(new_item_data)
    #Serialize the created item schema and return the response
    if  not new_item:
        return {"error": "Option invalid"}, 200
    item_schema=ItemSchema()
    item_json=item_schema.dump(new_item)
    return jsonify(item_json),201

#Update item
@item_bp.put('/<int:ItemID>')
def update_item_route(ItemID):
    item=Item.query.get(ItemID)
    if not item:
        return jsonify({'message':'Item not found'}),404
    data=request.get_json()
    new_item=update_item(ItemID,data)
    if not new_item:
        return jsonify({'message':'Item not found'}),404
    return jsonify({'message':'Item updated succesfully'}),200

#Delete Item
@item_bp.delete('/<int:ItemID>')
def delete_item_route(ItemID):
    new_item=delete_item(ItemID)
    if not new_item:
        return jsonify({'error':'Item not found'}),404
    return jsonify({'message':'Item deleted succesfully'}),200