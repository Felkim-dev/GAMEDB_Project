from flask import Flask
from .extensions import db,ma
from routes import register_routes
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    import models
    register_routes(app)

    return app