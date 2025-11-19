from .player_routes import player_bp
from .item_routes import item_bp


def register_routes(app):
    app.register_blueprint(player_bp, url_prefix="/players")
    app.register_blueprint(item_bp, url_prefix="/items")
    
    
