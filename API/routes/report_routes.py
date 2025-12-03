from models import (Character, Player, 
                    Item, Inventory,
                    Mission, Transaction,
                    CharacterMission)
from flask import Blueprint, request, jsonify,make_response

report_bp=Blueprint('report_bp',__name__)

#Available reports:
@report_bp.get('/')
def available_reports():
    reports = [
        {"id": 1, "name": "Character Report",   "endpoint": "/reports/characters-with-players"},
        {"id": 2, "name": "Player Inventory",   "endpoint": "/reports/inventory-details"},
        {"id": 3, "name": "Missions Progress",  "endpoint": "/reports/missions-progress"},
        {"id": 4, "name": "Transactions",       "endpoint": "/reports/transactions-details"},
        {"id": 5, "name": "Character Profile",  "endpoint": "/reports/character-profile/<int:CharacterID>"},
    ]
    return make_response(jsonify({"available_reports":reports}))

#Character Profile Report
@report_bp.get("/characters-with-players")
def characters_with_players_report():
    characters=Character.query.all()
    character_list=[]
    for char in characters:
        character_list.append({
            'CharacterID': char.CharacterID,
            'PlayerUsername': char.player.UserName,
            'Name': char.Name,
            'Level': char.Level,
            'Experience': char.Experience,
            'PlayerID': char.PlayerID,
            'PlayerEmail': char.player.Email
        })
    return jsonify({'report':character_list}),200

#Inventory Details Report
@report_bp.get("/inventory-details")
def inventory_details_report():
    inventories=Inventory.query.all()
    inventory_list=[]
    for inv in inventories:
        inventory_list.append({
            'CharacterID': inv.character.CharacterID,
            'CharacterName': inv.character.player.UserName,
            'ItemID': inv.item.ItemID,
            'ItemName': inv.item.Name,
            'Quantity': inv.Quantity
        })
    return jsonify({'report':inventory_list}),200

#Missions Progress Report
@report_bp.get("/missions-progress")
def missions_progress_report():
    character_missions=CharacterMission.query.all()
    mission_progress_list=[]
    for cm in character_missions:
        mission_progress_list.append({
            'CharacterID': cm.char_mission.CharacterID,
            'CharacterName': cm.char_mission.Name,
            'MissionID': cm.MissionID,
            'MissionTitle': cm.mission.Title,
            'Status': cm.Status
        })
    return jsonify({'report':mission_progress_list}),200

#Transactions Details Report
@report_bp.get("/transactions-details")
def transactions_details_report():
    transactions=Transaction.query.all()
    transaction_list=[]
    for tx in transactions:
        transaction_list.append({
            'TransactionID': tx.TransactionID,
            'GiverID': tx.giver.CharacterID,
            'GiverUsername': tx.giver.player.UserName,
            'ReceiverID': tx.receiver.CharacterID,
            'ReceiverUsername': tx.receiver.player.UserName,
            'ItemID': tx.item_changed.ItemID,
            'ItemName': tx.item_changed.Name,
            'TransactionType': tx.TransactionType,
            'Date': tx.TransactionDate.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({'report':transaction_list}),200


#Todo respecto a un personaje en particular
@report_bp.get("/character-profile/<int:CharacterID>")
def character_report(CharacterID):
    character=Character.query \
    .filter_by(CharacterID=CharacterID) \
    .first()
    if not character:
        return jsonify({'error':'Character not found'}),404
    return jsonify({
        'profile':{
        'character_info':{'CharacterID': character.CharacterID,
        'Name': character.Name,
        'Level': character.Level,
        'PlayerID': character.player.PlayerID,
        'Experience': character.Experience,
        "PlayerName": character.player.UserName,
        "PlayerEmail": character.player.Email},
        
        'inventory': [
            {
                'ItemID': inv.item.ItemID,
                'ItemName': inv.item.Name,
                'Quantity': inv.Quantity
            } for inv in character.inventory_holders
        ],
        'missions': [
            {
                'MissionID': cm.mission.MissionID,
                'Title': cm.mission.Title,
                'Description': cm.mission.Description,
                'Status': cm.Status
            } for cm in character.missions_link
        ],
        'transactions_given': [
            {
                'TransactionID': tx.TransactionID,
                'ReceiverUsername': tx.receiver.player.UserName,
                'ItemName': tx.item_changed.Name,
                'Type': tx.TransactionType,
                'Date': tx.TransactionDate.strftime("%Y-%m-%d %H:%M:%S")
            } for tx in character.given_transactions
        ],
        'transactions_received': [
            {
                'TransactionID': tx.TransactionID,
                'GiverUsername': tx.giver.player.UserName,
                'ItemName': tx.item_changed.Name,
                'Type': tx.TransactionType,
                'Date': tx.TransactionDate.strftime("%Y-%m-%d %H:%M:%S")
            } for tx in character.received_transactions
        ]
    }}),200
#Todo respecto a un jugador en particular
@report_bp.get("/player/<int:PlayerID>")
def player_report(PlayerID):
    player=Player.query \
    .filter_by(PlayerID=PlayerID) \
    .first()
    if not player:
        return jsonify({'error':'Player not found'}),404
    return jsonify({
        'report':{
            'PlayerID': player.PlayerID,
            'Username': player.UserName,
            'Email': player.Email,
            'Characters': [
                {
                    'CharacterID': char.CharacterID,
                    'Name': char.player.UserName,
                    'Level': char.Level,
                    'Experience': char.Experience
                } for char in player.characters
            ]
        }
    }),200

