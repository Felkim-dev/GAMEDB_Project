from .player_routes import player_bp
from .item_routes import item_bp
from .character_routes import character_bp


def register_routes(app):
    app.register_blueprint(player_bp, url_prefix="/players")
    app.register_blueprint(item_bp, url_prefix="/items")
    app.register_blueprint(character_bp, url_prefix="/characters")
    
    
    
