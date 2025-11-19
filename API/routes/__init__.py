from .player_routes import player_bp


def register_routes(app):
    app.register_blueprint(player_bp, url_prefix="/players")
    
