from .player_routes import player_bp
from .item_routes import item_bp
from .character_routes import character_bp
from .mission_routes import mission_bp
from .inventory_routes import inventory_bp
from .char_mission_routes import char_mission_bp
from .transaction_routes import transaction_bp

def register_routes(app):
    app.register_blueprint(player_bp, url_prefix="/players")
    app.register_blueprint(item_bp, url_prefix="/items")
    app.register_blueprint(character_bp, url_prefix="/characters")
    app.register_blueprint(mission_bp, url_prefix="/missions")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(char_mission_bp, url_prefix="/char_missions")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    
